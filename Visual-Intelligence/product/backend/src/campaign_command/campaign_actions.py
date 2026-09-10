"""
Phase 25 Governed Campaign Mutating Actions with Optimistic Concurrency Protection.
"""
from typing import Dict, Any, Optional
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability, ControlPlaneAuditEvent
from src.control_plane.permissions import PermissionGuard
from src.control_plane.exceptions import StaleActionConflictError
from src.control_plane.audit import ControlPlaneAuditLogger
from src.campaign_command.campaign_projection import DetailedCampaignState, CampaignDetailedProjection

class CampaignActionService:
    """Handles governed operator actions with strict optimistic locking."""

    def __init__(self, audit_logger: Optional[ControlPlaneAuditLogger] = None):
        self.audit_logger = audit_logger or ControlPlaneAuditLogger()
        self._campaigns: Dict[str, CampaignDetailedProjection] = {}

    def register_campaign(self, campaign: CampaignDetailedProjection) -> None:
        self._campaigns[campaign.campaign_id] = campaign

    def transition_campaign_state(
        self,
        context: OperatorContext,
        campaign_id: str,
        target_state: DetailedCampaignState,
        expected_version: int,
        reason: str = ""
    ) -> CampaignDetailedProjection:
        """Transitions campaign state with strict optimistic concurrency validation."""
        PermissionGuard.enforce_capability(context, OperatorCapability.OPERATE_CAMPAIGN)

        if campaign_id not in self._campaigns:
            raise KeyError(f"Campaign '{campaign_id}' not found.")

        cmp = self._campaigns[campaign_id]
        PermissionGuard.enforce_tenant_boundary(context, cmp.tenant_id, cmp.client_id)

        if cmp.version != expected_version:
            raise StaleActionConflictError(
                f"Stale action rejected for campaign '{campaign_id}'. "
                f"Expected version {expected_version}, but current server version is {cmp.version}."
            )

        cmp.state = target_state
        cmp.version += 1

        self.audit_logger.record_event(ControlPlaneAuditEvent(
            operator_id=context.operator_id,
            tenant_id=cmp.tenant_id,
            client_id=cmp.client_id,
            action="TRANSITION_CAMPAIGN_STATE",
            target_resource=campaign_id,
            correlation_id=context.correlation_id,
            details={"new_state": target_state.value, "version": cmp.version, "reason": reason}
        ))

        return cmp
