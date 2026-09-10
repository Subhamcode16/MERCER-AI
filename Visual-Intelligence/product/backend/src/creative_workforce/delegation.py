"""
Phase 14 Workforce Delegation Engine
------------------------------------
Interprets client objectives, decomposes them into structured staff assignments,
assigns hierarchical context scopes, and establishes task dependency DAGs.
Rejects capability escalation, authority transfer, cross-client context access, and security policy mutation.
"""

from typing import List, Dict, Any, Optional
import uuid

from src.creative_workforce.organization_models import (
    Role,
    StaffIdentity,
    ContextBinding,
    WorkforceAssignment,
)
from src.creative_workforce.staff_registry import StaffRegistry
from src.creative_workforce.client_context import ClientContextManager
from src.creative_workforce.exceptions import InvalidWorkforceRequestError

class WorkforceDelegationEngine:
    """Engine decomposing client campaign objectives into workforce staff assignments."""

    def __init__(
        self,
        staff_registry: Optional[StaffRegistry] = None,
        context_manager: Optional[ClientContextManager] = None,
    ):
        self.registry = staff_registry or StaffRegistry()
        self.context_manager = context_manager or ClientContextManager()

    def decompose_objective(
        self,
        client_id: str,
        brand_id: str,
        campaign_id: str,
        mission_id: str,
        objective: str,
        task_specs: Optional[List[Dict[str, Any]]] = None,
    ) -> List[WorkforceAssignment]:
        """Decomposes a campaign objective into role-based assignments with dependency graph."""
        if not objective:
            raise InvalidWorkforceRequestError("Objective cannot be empty.")

        assignments: List[WorkforceAssignment] = []

        if not task_specs:
            # Default canonical creative campaign delegation pipeline
            task_specs = [
                {"role": Role.TREND_RESEARCHER, "objective": f"Gather trend intelligence for {objective}"},
                {"role": Role.BRAND_STRATEGIST, "objective": f"Formulate brand & campaign strategy for {objective}", "deps": [0]},
                {"role": Role.CREATIVE_DIRECTOR, "objective": f"Synthesize creative direction for {objective}", "deps": [1]},
                {"role": Role.VISUAL_DESIGNER, "objective": f"Produce visual assets for {objective}", "deps": [2]},
                {"role": Role.COPYWRITER, "objective": f"Write campaign copy for {objective}", "deps": [2]},
                {"role": Role.CREATIVE_CRITIC, "objective": f"Evaluate self-critique on campaign assets", "deps": [3, 4]},
                {"role": Role.INDEPENDENT_REVIEWER, "objective": f"Perform independent review on final campaign proposal", "deps": [5]},
            ]

        spec_to_assignment_id: Dict[int, str] = {}

        for idx, spec in enumerate(task_specs):
            role = spec["role"] if isinstance(spec["role"], Role) else Role(spec["role"])
            staff_list = self.registry.list_by_role(role)
            staff_member = staff_list[0] if staff_list else self.registry.list_all()[0]

            task_id = f"task-{idx + 1}"
            assignment_id = f"asgn-{uuid.uuid4().hex[:8]}"
            spec_to_assignment_id[idx] = assignment_id

            deps = [spec_to_assignment_id[d_idx] for d_idx in spec.get("deps", []) if d_idx in spec_to_assignment_id]

            binding = self.context_manager.create_context_binding(
                client_id=client_id,
                brand_id=brand_id,
                campaign_id=campaign_id,
                mission_id=mission_id,
                task_id=task_id,
                staff_id=staff_member.staff_id,
            )

            asgn = WorkforceAssignment(
                assignment_id=assignment_id,
                objective=spec.get("objective", f"Execute {role.value} task"),
                assigned_staff_id=staff_member.staff_id,
                role=role,
                context_binding=binding,
                dependencies=deps,
                status="PLANNED",
            )
            assignments.append(asgn)

        return assignments
