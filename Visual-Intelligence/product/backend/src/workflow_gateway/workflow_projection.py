"""
Phase 14 Workflow Projection
----------------------------
Produces safe, secret-scrubbed read models (projections) for UI/API client callers.
Ensures secret leakage elimination and state separation.
"""

from typing import Dict, Any, Optional
import time

from src.workflow_gateway.models import WorkflowView, WorkflowStatus
from src.workflow_gateway.exceptions import SecretExposureError

class WorkflowProjectionEngine:
    """Engine responsible for building secret-sanitized workflow views."""

    @staticmethod
    def create_projection(
        workflow_id: str,
        mission_id: str,
        status: WorkflowStatus,
        objective_title: str,
        plan_step_count: int = 0,
        completed_steps: int = 0,
        pending_approvals: int = 0,
        artifacts_generated: int = 0,
        created_at: Optional[float] = None,
    ) -> WorkflowView:
        """Constructs a secret-sanitized WorkflowView projection."""
        now = time.time()
        view = WorkflowView(
            workflow_id=workflow_id,
            mission_id=mission_id,
            status=status,
            objective_title=objective_title,
            plan_step_count=plan_step_count,
            completed_steps=completed_steps,
            pending_approvals=pending_approvals,
            artifacts_generated=artifacts_generated,
            created_at=created_at or now,
            updated_at=now,
        )

        # Enforce secret leakage check
        view.sanitize_check()
        return view

    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Deeply scrubs a dictionary of sensitive key values."""
        sanitized = {}
        forbidden_keys = {"secret", "bearer", "private_key", "password", "auth_token", "credential"}
        for k, v in data.items():
            if any(fk in str(k).lower() for fk in forbidden_keys):
                sanitized[k] = "[REDACTED_SECRET]"
            elif isinstance(v, dict):
                sanitized[k] = WorkflowProjectionEngine.sanitize_dict(v)
            else:
                sanitized[k] = v
        return sanitized
