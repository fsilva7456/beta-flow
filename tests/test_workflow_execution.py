import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_execution.db"

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

def test_workflow_execution(client):
    # Create a test workflow
    workflow_data = {
        "workflow_name": "Test Execution Workflow",
        "steps": [
            {
                "step_name": "Step 1",
                "action": "llm-call",
                "parameters": {
                    "prompt": "Tell me a joke",
                    "model": "gpt-4-turbo",
                    "temperature": 0.7
                }
            },
            {
                "step_name": "Step 2",
                "action": "llm-call",
                "parameters": {
                    "prompt": "What is 2+2?",
                    "model": "gpt-4-turbo",
                    "temperature": 0.7
                }
            }
        ]
    }
    
    # Create workflow
    create_response = client.post("/api/v1/workflows", json=workflow_data)
    assert create_response.status_code == 200
    workflow_id = create_response.json()["id"]
    
    # Execute workflow
    execute_response = client.post(f"/api/v1/workflows/{workflow_id}/execute")
    assert execute_response.status_code == 200
    
    # Check execution results
    results = execute_response.json()
    assert results["workflow_id"] == workflow_id
    assert results["workflow_name"] == "Test Execution Workflow"
    assert len(results["results"]) == 2

def test_invalid_workflow_execution(client):
    # Try to execute non-existent workflow
    response = client.post("/api/v1/workflows/999/execute")
    assert response.status_code == 404

def test_list_workflows(client):
    # Create multiple workflows
    workflow_names = ["Workflow 1", "Workflow 2", "Workflow 3"]
    
    for name in workflow_names:
        workflow_data = {
            "workflow_name": name,
            "steps": [
                {
                    "step_name": "Step 1",
                    "action": "llm-call",
                    "parameters": {
                        "prompt": "Test prompt",
                        "model": "gpt-4-turbo"
                    }
                }
            ]
        }
        client.post("/api/v1/workflows", json=workflow_data)
    
    # List workflows
    response = client.get("/api/v1/workflows")
    assert response.status_code == 200
    workflows = response.json()
    
    # Check if all workflows are listed
    assert len(workflows) == len(workflow_names)
    listed_names = [w["workflow_name"] for w in workflows]
    for name in workflow_names:
        assert name in listed_names
