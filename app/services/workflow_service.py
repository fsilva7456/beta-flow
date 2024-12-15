from sqlalchemy.orm import Session
from app.models.workflow import Workflow, WorkflowStep
from app.schemas.workflow import WorkflowCreate
from app.services.llm_service import LLMService
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self):
        self.llm_service = LLMService()
        self.action_handlers = {
            "llm-call": self._handle_llm_call
        }

    async def create_workflow(self, db: Session, workflow_data: WorkflowCreate) -> Workflow:
        workflow = Workflow(workflow_name=workflow_data.workflow_name)  # Match the column name
        db.add(workflow)
        db.flush()

        for idx, step in enumerate(workflow_data.steps):
            db_step = WorkflowStep(
                workflow_id=workflow.id,
                step_name=step.step_name,
                action=step.action,
                parameters=step.parameters,
                order=idx
            )
            db.add(db_step)

        db.commit()
        db.refresh(workflow)
        return workflow

    def get_workflow(self, db: Session, workflow_id: int) -> Workflow:
        return db.query(Workflow).filter(Workflow.id == workflow_id).first()

    def get_workflows(self, db: Session, skip: int = 0, limit: int = 100) -> List[Workflow]:
        return db.query(Workflow).offset(skip).limit(limit).all()

    async def execute_workflow(self, db: Session, workflow_id: int) -> Dict:
        workflow = self.get_workflow(db, workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        results = []
        for step in sorted(workflow.steps, key=lambda x: x.order):
            try:
                handler = self.action_handlers.get(step.action)
                if not handler:
                    raise ValueError(f"Unsupported action: {step.action}")
                
                result = await handler(step.parameters)
                results.append({
                    "step_name": step.step_name,
                    "result": result
                })
            except Exception as e:
                logger.error(f"Error executing step {step.step_name}: {str(e)}")
                results.append({
                    "step_name": step.step_name,
                    "error": str(e)
                })

        return {
            "workflow_id": workflow.id,
            "workflow_name": workflow.workflow_name,
            "results": results
        }

    async def _handle_llm_call(self, parameters: Dict) -> str:
        prompt = parameters.pop("prompt")
        model = parameters.pop("model", "gpt-4-turbo")
        return await self.llm_service.execute(prompt, model, parameters)
