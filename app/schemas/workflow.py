from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class ConditionType(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"

class OutputReference(BaseModel):
    step_name: str
    key: str = "result"

class Condition(BaseModel):
    type: ConditionType
    step_name: str
    key: str = "result"
    value: str

class WorkflowStepBase(BaseModel):
    step_name: str
    action: str
    parameters: Dict = Field(default_factory=dict)
    condition: Optional[Condition] = None
    group: Optional[str] = None
    use_output_from: Optional[OutputReference] = None

class WorkflowStepCreate(WorkflowStepBase):
    pass

class WorkflowStep(WorkflowStepBase):
    id: int
    workflow_id: int
    order: int

    class Config:
        from_attributes = True

class WorkflowBase(BaseModel):
    workflow_name: str

class WorkflowCreate(WorkflowBase):
    steps: List[WorkflowStepCreate]

class Workflow(WorkflowBase):
    id: int
    workflow_name: str
    created_at: datetime
    steps: List[WorkflowStep]

    class Config:
        from_attributes = True

class StepResult(BaseModel):
    step_name: str
    result: str
    skipped: bool = False
    error: Optional[str] = None

class WorkflowExecutionResult(BaseModel):
    workflow_id: int
    workflow_name: str
    results: List[StepResult]