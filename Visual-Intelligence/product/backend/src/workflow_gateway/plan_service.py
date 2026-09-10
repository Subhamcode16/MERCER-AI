"""
Phase 14 Plan Service
---------------------
Transforms mission objectives, constraints, and task graphs into a user-reviewable
execution plan. Guarantees side-effect freedom during plan generation and review.
"""

from typing import List, Dict, Any, Optional
import uuid
import time

from src.workflow_gateway.models import (
    WorkflowRequest,
    WorkflowPlan,
    WorkflowPlanStep,
    WorkflowStatus,
)
from src.workflow_gateway.exceptions import (
    InvalidWorkflowRequestError,
    WorkflowStateError,
)

class PlanService:
    """Service for constructing and managing reviewable workflow execution plans."""

    def __init__(self):
        self._plans: Dict[str, WorkflowPlan] = {}

    def generate_plan(
        self,
        workflow_request: WorkflowRequest,
        mission_id: str,
        task_specs: List[Dict[str, Any]],
    ) -> WorkflowPlan:
        """Constructs a reviewable WorkflowPlan from task specifications without executing side effects."""
        plan_id = f"plan-{uuid.uuid4().hex[:8]}"
        steps: List[WorkflowPlanStep] = []

        for idx, spec in enumerate(task_specs):
            step_id = f"step-{idx + 1}"
            task_name = spec.get("name", f"Task {idx + 1}")
            assigned_role = spec.get("role", "AI_Specialist")
            capability = spec.get("capability", "CREATE_DRAFT")
            target_platform = spec.get("platform", "sandbox_social")
            requires_auth = spec.get("requires_auth", capability in ["PUBLISH_CONTENT", "DELETE_CONTENT", "CREATE_DRAFT"])
            cost = float(spec.get("estimated_cost", 10.0))

            step = WorkflowPlanStep(
                step_id=step_id,
                task_name=task_name,
                assigned_role=assigned_role,
                capability_required=capability,
                target_platform=target_platform,
                requires_authorization=requires_auth,
                status="PROPOSED",
                estimated_cost=cost,
            )
            steps.append(step)

        plan = WorkflowPlan(
            plan_id=plan_id,
            workflow_id=workflow_request.workflow_id,
            mission_id=mission_id,
            steps=steps,
            created_at=time.time(),
            review_notes=[
                "Plan generated successfully.",
                f"Objective: {workflow_request.objective.title}",
                f"Target platforms: {', '.join(workflow_request.objective.target_platforms)}",
            ],
        )

        self._plans[workflow_request.workflow_id] = plan
        return plan

    def get_plan(self, workflow_id: str) -> Optional[WorkflowPlan]:
        """Retrieves an existing plan by workflow ID. Strictly side-effect free."""
        return self._plans.get(workflow_id)

    def update_step_status(
        self, workflow_id: str, step_id: str, new_status: str
    ) -> WorkflowPlan:
        """Updates the status of a specific step in an existing plan."""
        plan = self._plans.get(workflow_id)
        if not plan:
            raise WorkflowStateError(f"No plan found for workflow {workflow_id}")

        new_steps = []
        found = False
        for step in plan.steps:
            if step.step_id == step_id:
                new_steps.append(
                    WorkflowPlanStep(
                        step_id=step.step_id,
                        task_name=step.task_name,
                        assigned_role=step.assigned_role,
                        capability_required=step.capability_required,
                        target_platform=step.target_platform,
                        requires_authorization=step.requires_authorization,
                        status=new_status,
                        estimated_cost=step.estimated_cost,
                    )
                )
                found = True
            else:
                new_steps.append(step)

        if not found:
            raise InvalidWorkflowRequestError(f"Step {step_id} not found in plan {plan.plan_id}")

        updated_plan = WorkflowPlan(
            plan_id=plan.plan_id,
            workflow_id=plan.workflow_id,
            mission_id=plan.mission_id,
            steps=new_steps,
            created_at=plan.created_at,
            review_notes=plan.review_notes,
        )
        self._plans[workflow_id] = updated_plan
        return updated_plan
