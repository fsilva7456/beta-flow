import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
import asyncio
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_parallel.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_parallel_workflow_execution(client):
    workflow_data = {
        "workflow_name": "Parallel Test",
        "steps": [
            {
                "step_name": "Initial Step",
                "action": "llm-call",
                "parameters": {
                    "prompt": "Start",
                    "model": "gpt-4-turbo"
                }
            },
            {
                "step_name": "Parallel Step 1",
                "action": "llm-call",
                "parameters": {
                    "prompt": "What is 2+2?",
                    "model": "gpt-4-turbo"
                },
                "group": "math-questions"
            },
            {
                "step_name": "Parallel Step 2",
                "action": "llm-call",
                "parameters": {
                    "prompt": "What is 3+3?",
                    "model": "gpt-4-turbo"
                },
                "group": "math-questions"
            },
            {
                "step_name": "Final Step",
                "action": "llm-call",
                "parameters": {
                    "prompt": "End",
                    "model": "gpt-4-turbo"
                }
            }
        ]
    }

    with patch('app.services.workflow_service.LLMService.execute') as mock_execute:
        # Mock LLM responses
        mock_execute.side_effect = ["Started", "Four", "Six", "Ended"]
        
        # Create workflow
        response = client.post("/api/v1/workflows", json=workflow_data)
        assert response.status_code == 200
        workflow_id = response.json()["id"]
        
        # Execute workflow
        execute_response = client.post(f"/api/v1/workflows/{workflow_id}/execute")
        assert execute_response.status_code == 200
        
        results = execute_response.json()["results"]
        assert len(results) == 4
        
        # Verify parallel execution order is maintained within group
        parallel_results = [r for r in results if r["step_name"].startswith("Parallel")]
        assert len(parallel_results) == 2
        assert set([r["result"] for r in parallel_results]) == {"Four", "Six"}

def test_empty_parallel_group(client):
    workflow_data = {
        "workflow_name": "Empty Group Test",
        "steps": [
            {
                "step_name": "Single Step",
                "action": "llm-call",
                "parameters": {
                    "prompt": "Hello",
                    "model": "gpt-4-turbo"
                },
                "group": "empty-group"
            }
        ]
    }

    with patch('app.services.workflow_service.LLMService.execute') as mock_execute:
        mock_execute.return_value = "Hello!"
        
        response = client.post("/api/v1/workflows", json=workflow_data)
        assert response.status_code == 200
        workflow_id = response.json()["id"]
        
        execute_response = client.post(f"/api/v1/workflows/{workflow_id}/execute")
        assert execute_response.status_code == 200
        
        results = execute_response.json()["results"]
        assert len(results) == 1
        assert results[0]["result"] == "Hello!"
