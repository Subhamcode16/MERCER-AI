"""
Phase 16 Workforce Activity View.
Exposes workforce assignments and task status projections without leaking internal reasoning.
"""

from typing import List, Any
from src.client_experience.workspace_models import WorkforceActivityDTO
from src.client_experience.access_models import UserIdentity

class WorkforceActivityView:
    """View provider projecting high-level workforce staff activity."""

    def list_workforce_activity(self, user: UserIdentity, studio_orchestrator: Any) -> List[WorkforceActivityDTO]:
        """Lists high-level staff activities for a client."""
        user.verify_capability("view_timeline") if not user.has_capability("view_workforce") else user.verify_capability("view_workforce")
        client_id = user.assigned_client_id

        registry = studio_orchestrator.workforce_orchestrator.staff_registry
        staff_members = list(registry._staff.values()) if hasattr(registry, "_staff") else []

        dtos = []
        for staff in staff_members:
            dtos.append(WorkforceActivityDTO(
                staff_id=staff.staff_id,
                role=staff.role.value if hasattr(staff.role, "value") else str(staff.role),
                department=staff.department.value if hasattr(staff.department, "value") else str(staff.department),
                current_task=f"Assigned under {client_id} scope",
                status="ACTIVE",
                revision_count=0
            ))
        return dtos
