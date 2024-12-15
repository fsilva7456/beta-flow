from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.workflow import WorkflowCreate, Workflow, WorkflowExecutionResult
from app.services.workflow_service import WorkflowService
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
workflow_service = WorkflowService()

@router.post("/workflows", response_model=Workflow)
async def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating workflow: {workflow.workflow_name}")
        return await workflow_service.create_workflow(db, workflow)
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/workflows", response_model=List[Workflow])
def list_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return workflow_service.get_workflows(db, skip, limit)
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflows/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = workflow_service.get_workflow(db, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecutionResult)
async def execute_workflow(workflow_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Executing workflow: {workflow_id}")
        return await workflow_service.execute_workflow(db, workflow_id)
    except ValueError as e:
        logger.error(f"Error executing workflow: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error executing workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
