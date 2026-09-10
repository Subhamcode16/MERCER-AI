"""
Phase 16 Client Dashboard Projection Engine.
Synthesizes unified client workspace dashboard projections.
"""

from typing import Dict, Any, Optional
from src.client_experience.workspace_models import ClientWorkspaceDTO
from src.client_experience.presentation_policy import PresentationPolicyEngine
from src.client_experience.access_models import UserIdentity

class ClientDashboardProjectionEngine:
    """Engine projecting high-level client workspace dashboards."""

    def __init__(self, presentation_policy: Optional[PresentationPolicyEngine] = None):
        self.presentation_policy = presentation_policy or PresentationPolicyEngine()

    def get_dashboard(self, user: UserIdentity, studio_orchestrator: Any) -> ClientWorkspaceDTO:
        """Retrieves and projects client workspace dashboard."""
        client_id = user.assigned_client_id
        summary = studio_orchestrator.client_manager.get_client_summary(client_id)
        campaigns = studio_orchestrator.campaign_manager.list_campaigns(client_id)
        approvals = studio_orchestrator.approval_queue.list_pending_approvals(client_id)
        health = studio_orchestrator.get_studio_health(client_id)

        return ClientWorkspaceDTO(
            client_id=client_id,
            name=summary.get("name", "Studio Client"),
            industry=summary.get("industry", "General"),
            active_campaigns_count=len(campaigns),
            pending_approvals_count=len(approvals),
            overall_health=health.overall_health
        )
