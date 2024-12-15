from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowExecutionResult
from app.services.workflow_service import WorkflowService
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
workflow_service = WorkflowService()

@router.post("/workflows", response_model=WorkflowResponse)
async def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating workflow: {workflow.workflow_name}")
        db_workflow = await workflow_service.create_workflow(db, workflow)
        return WorkflowResponse(
            id=db_workflow.id,
            workflow_name=db_workflow.workflow_name,
            created_at=db_workflow.created_at,
            steps=db_workflow.steps
        )
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/workflows", response_model=List[WorkflowResponse])
def list_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        workflows = workflow_service.get_workflows(db, skip, limit)
        return [WorkflowResponse(
            id=w.id,
            workflow_name=w.workflow_name,
            created_at=w.created_at,
            steps=w.steps
        ) for w in workflows]
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = workflow_service.get_workflow(db, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WorkflowResponse(
        id=workflow.id,
        workflow_name=workflow.workflow_name,
        created_at=workflow.created_at,
        steps=workflow.steps
    )

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
