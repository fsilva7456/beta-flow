import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

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

def test_create_workflow(client):
    workflow_data = {
        "workflow_name": "Test Workflow",
        "steps": [
            {
                "step_name": "Test Step 1",
                "action": "llm-call",
                "parameters": {
                    "prompt": "Tell me a joke",
                    "model": "gpt-4-turbo",
                    "temperature": 0.7
                }
            }
        ]
    }
    
    response = client.post("/api/v1/workflows", json=workflow_data)
    assert response.status_code == 200
    data = response.json()
    assert data["workflow_name"] == "Test Workflow"
    assert len(data["steps"]) == 1

def test_get_workflow(client):
    # First create a workflow
    workflow_data = {
        "workflow_name": "Test Workflow",
        "steps": [
            {
                "step_name": "Test Step 1",
                "action": "llm-call",
                "parameters": {
                    "prompt": "Tell me a joke",
                    "model": "gpt-4-turbo",
                    "temperature": 0.7
                }
            }
        ]
    }
    
    create_response = client.post("/api/v1/workflows", json=workflow_data)
    workflow_id = create_response.json()["id"]
    
    # Now get the workflow
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["workflow_name"] == "Test Workflow"
