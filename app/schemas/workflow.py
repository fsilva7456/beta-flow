from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class WorkflowStepBase(BaseModel):
    step_name: str
    action: str
    parameters: Dict = Field(default_factory=dict)

class WorkflowStepCreate(WorkflowStepBase):
    pass

class WorkflowStepResponse(WorkflowStepBase):
    id: int
    workflow_id: int
    order: int

    class Config:
        from_attributes = True

class WorkflowBase(BaseModel):
    workflow_name: str

class WorkflowCreate(WorkflowBase):
    steps: List[WorkflowStepCreate]

class WorkflowResponse(WorkflowBase):
    id: int
    workflow_name: str
    created_at: datetime
    steps: List[WorkflowStepResponse]

    class Config:
        from_attributes = True

class WorkflowExecutionResult(BaseModel):
    workflow_id: int
    workflow_name: str
    results: List[Dict[str, str]]
