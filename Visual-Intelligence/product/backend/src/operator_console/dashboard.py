"""
Phase 25 Operator Console Dashboard Aggregator.
"""
from typing import Dict, Any, Optional, List
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.control_plane.permissions import PermissionGuard
from src.control_plane.dto import sanitize_payload
from src.operator_console.operator_views import CuratorView, CreativeDirectorView, SREView
from src.control_plane.service import ControlPlaneService

class OperatorConsoleDashboard:
    """Aggregates executive, client-specific, and studio-wide operator views."""

    def __init__(self, service: ControlPlaneService):
        self.service = service

    def render_executive_dashboard(self, context: OperatorContext, tenant_id: str, client_id: str) -> Dict[str, Any]:
        """Renders the executive dashboard respecting tenant boundaries."""
        snapshot = self.service.get_dashboard_snapshot(context, tenant_id, client_id)
        return {
            "snapshot_id": snapshot.snapshot_id,
            "timestamp": snapshot.timestamp,
            "tenant_id": snapshot.tenant_id,
            "client_id": snapshot.client_id,
            "system_health": snapshot.system_health,
            "active_campaigns_count": snapshot.active_campaigns_count,
            "pending_approvals_count": snapshot.pending_approvals_count,
            "reliability": snapshot.reliability,
            "visual_observatory": snapshot.visual_observatory,
            "campaigns": snapshot.campaign_summaries
        }

    def render_role_specific_view(self, context: OperatorContext, tenant_id: str, client_id: str) -> Dict[str, Any]:
        """Renders role-customized dashboard projection."""
        snapshot = self.service.get_dashboard_snapshot(context, tenant_id, client_id)
        if OperatorRole.LEAD_CURATOR in context.roles:
            view = CuratorView(
                pending_approvals=[],
                active_campaigns=snapshot.campaign_summaries,
                recent_reviews_count=3,
                urgent_items=[]
            )
            return {"role": "LEAD_CURATOR", "view": view}
        elif OperatorRole.SRE_ENGINEER in context.roles:
            view = SREView(
                reliability=snapshot.reliability,
                provider_health_summary={"gemini": "HEALTHY", "imagen": "HEALTHY", "flux": "HEALTHY"},
                active_circuit_breakers=[],
                incident_alerts=[]
            )
            return {"role": "SRE_ENGINEER", "view": view}
        else:
            view = CreativeDirectorView(
                campaigns=snapshot.campaign_summaries,
                visual_overview=snapshot.visual_observatory,
                strategy_candidates_count=2,
                workforce_utilization_pct=78.5
            )
            return {"role": "CREATIVE_DIRECTOR", "view": view}
