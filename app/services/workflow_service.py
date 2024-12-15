from sqlalchemy.orm import Session
from app.models.workflow import Workflow, WorkflowStep
from app.schemas.workflow import WorkflowCreate, StepResult, ConditionType
from app.services.llm_service import LLMService
from typing import List, Dict, Optional
import logging
import asyncio
from collections import defaultdict

logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self):
        self.llm_service = LLMService()
        self.action_handlers = {
            "llm-call": self._handle_llm_call
        }

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

    def get_workflow(self, db: Session, workflow_id: int) -> Optional[Workflow]:
        return db.query(Workflow).filter(Workflow.id == workflow_id).first()

    def get_workflows(self, db: Session, skip: int = 0, limit: int = 100) -> List[Workflow]:
        return db.query(Workflow).offset(skip).limit(limit).all()

    def _evaluate_condition(self, condition: Dict, step_results: List[StepResult]) -> bool:
        if not condition:
            return True

        target_step = next(
            (r for r in step_results if r.step_name == condition["step_name"]),
            None
        )
        if not target_step:
            return False

        value = getattr(target_step, condition["key"])
        condition_type = ConditionType(condition["type"])

        if condition_type == ConditionType.EQUALS:
            return value == condition["value"]
        elif condition_type == ConditionType.NOT_EQUALS:
            return value != condition["value"]
        elif condition_type == ConditionType.CONTAINS:
            return condition["value"] in value
        return False

    def _process_output_references(self, parameters: Dict, step_results: List[StepResult]) -> Dict:
        processed_params = parameters.copy()
        for key, value in parameters.items():
            if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'): 
                ref_parts = value[2:-2].strip().split('.')
                if len(ref_parts) == 2:
                    step_name, param = ref_parts
                    referenced_step = next(
                        (r for r in step_results if r.step_name == step_name),
                        None
                    )
                    if referenced_step and hasattr(referenced_step, param):
                        processed_params[key] = getattr(referenced_step, param)
        return processed_params

    async def _execute_step(self, step: WorkflowStep, step_results: List[StepResult]) -> StepResult:
        try:
            if step.condition and not self._evaluate_condition(step.condition, step_results):
                return StepResult(
                    step_name=step.step_name,
                    result="",
                    skipped=True
                )

            handler = self.action_handlers.get(step.action)
            if not handler:
                raise ValueError(f"Unsupported action: {step.action}")

            # Process parameters for output references
            processed_params = self._process_output_references(step.parameters, step_results)
            
            result = await handler(processed_params)
            return StepResult(
                step_name=step.step_name,
                result=result
            )
        except Exception as e:
            logger.error(f"Error executing step {step.step_name}: {str(e)}")
            return StepResult(
                step_name=step.step_name,
                result="",
                error=str(e)
            )

    async def execute_workflow(self, db: Session, workflow_id: int) -> Dict:
        workflow = self.get_workflow(db, workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        steps = sorted(workflow.steps, key=lambda x: x.order)
        results: List[StepResult] = []
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