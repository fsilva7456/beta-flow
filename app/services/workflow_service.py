from sqlalchemy.orm import Session
from app.models.workflow import Workflow, WorkflowStep
from app.schemas.workflow import WorkflowCreate
from app.services.llm_service import LLMService
from typing import List, Dict, Optional
import logging
import asyncio
from collections import defaultdict
import re

logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self):
        self.llm_service = LLMService()
        self.action_handlers = {
            "llm-call": self._handle_llm_call
        }

    def _replace_step_references(self, text: str, step_results: List[Dict]) -> str:
        """Replace {{Step X}} references with actual results"""
        for step in step_results:
            pattern = f"{{{{\s*{step['step_name']}\s*}}}}"
            text = re.sub(pattern, step.get('result', ''), text)
        return text

    async def create_workflow(self, db: Session, workflow_data: WorkflowCreate) -> Workflow:
        workflow = Workflow(workflow_name=workflow_data.workflow_name)
        db.add(workflow)
        db.flush()

        for idx, step in enumerate(workflow_data.steps):
            db_step = WorkflowStep(
                workflow_id=workflow.id,
                step_name=step.step_name,
                action=step.action,
                parameters=step.parameters,
                condition=step.condition.dict() if step.condition else None,
                group=step.group,
                order=idx
            )
            db.add(db_step)

        db.commit()
        db.refresh(workflow)
        return workflow

    async def update_workflow(self, db: Session, workflow_id: int, workflow_data: WorkflowCreate) -> Workflow:
        # Get existing workflow
        workflow = self.get_workflow(db, workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Update workflow name
        workflow.workflow_name = workflow_data.workflow_name

        # Delete existing steps
        db.query(WorkflowStep).filter(WorkflowStep.workflow_id == workflow_id).delete()

        # Add new steps
        for idx, step in enumerate(workflow_data.steps):
            db_step = WorkflowStep(
                workflow_id=workflow.id,
                step_name=step.step_name,
                action=step.action,
                parameters=step.parameters,
                condition=step.condition.dict() if step.condition else None,
                group=step.group,
                order=idx
            )
            db.add(db_step)

        db.commit()
        db.refresh(workflow)
        return workflow

    def get_workflow(self, db: Session, workflow_id: int) -> Optional[Workflow]:
        return db.query(Workflow).filter(Workflow.id == workflow_id).first()

    def get_workflows(self, db: Session, skip: int = 0, limit: int = 100) -> List[Workflow]:
        return db.query(Workflow).offset(skip).limit(limit).all()

    def _evaluate_condition(self, condition: Dict, step_results: List[Dict]) -> bool:
        if not condition:
            return True

        target_step = next(
            (r for r in step_results if r.get('step_name') == condition["step_name"]),
            None
        )
        if not target_step:
            return False

        value = target_step.get('result', '')
        condition_type = condition["type"]

        if condition_type == "equals":
            return value == condition["value"]
        elif condition_type == "not_equals":
            return value != condition["value"]
        elif condition_type == "contains":
            return condition["value"] in value
        return False

    async def _execute_step(self, step: WorkflowStep, step_results: List[Dict]) -> Dict:
        try:
            if step.condition and not self._evaluate_condition(step.condition, step_results):
                return {
                    "step_name": step.step_name,
                    "result": "",
                    "skipped": True
                }

            handler = self.action_handlers.get(step.action)
            if not handler:
                raise ValueError(f"Unsupported action: {step.action}")

            # Process any references in the parameters
            processed_params = {}
            for key, value in step.parameters.items():
                if isinstance(value, str):
                    processed_params[key] = self._replace_step_references(value, step_results)
                else:
                    processed_params[key] = value

            result = await handler(processed_params)
            return {
                "step_name": step.step_name,
                "result": result,
                "skipped": False
            }

        except Exception as e:
            logger.error(f"Error executing step {step.step_name}: {str(e)}")
            return {
                "step_name": step.step_name,
                "result": "",
                "error": str(e)
            }

    async def execute_workflow(self, db: Session, workflow_id: int) -> Dict:
        workflow = self.get_workflow(db, workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        steps = sorted(workflow.steps, key=lambda x: x.order)
        results: List[Dict] = []
        grouped_steps = defaultdict(list)

        # Organize steps by group
        for step in steps:
            if step.group:
                grouped_steps[step.group].append(step)
            else:
                grouped_steps[f"sequential_{step.order}"].append(step)

        # Execute steps group by group
        for group_name, group_steps in grouped_steps.items():
            if group_name.startswith("sequential_"):
                # Execute sequential step
                step = group_steps[0]
                result = await self._execute_step(step, results)
                results.append(result)
            else:
                # Execute parallel steps
                parallel_tasks = [
                    self._execute_step(step, results)
                    for step in group_steps
                ]
                parallel_results = await asyncio.gather(*parallel_tasks)
                results.extend(parallel_results)

        return {
            "workflow_id": workflow.id,
            "workflow_name": workflow.workflow_name,
            "results": results
        }

    async def _handle_llm_call(self, parameters: Dict) -> str:
        prompt = parameters.pop("prompt")
        model = parameters.pop("model", "gpt-4-turbo")
        return await self.llm_service.execute(prompt, model, parameters)