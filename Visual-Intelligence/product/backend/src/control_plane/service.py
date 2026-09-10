"""
Phase 25 Master Control Plane Service.
"""
import logging
from typing import Dict, Any, List, Optional
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability, ControlPlaneAuditEvent
from src.control_plane.permissions import PermissionGuard
from src.control_plane.event_stream import ControlPlaneEventStreamBus, ControlPlaneEvent
from src.control_plane.audit import ControlPlaneAuditLogger
from src.control_plane.snapshot import SnapshotManager, OperationalSnapshot
from src.control_plane.dto import (
    CampaignSummaryDTO,
    DeliverableSummaryDTO,
    ApprovalRequestDTO,
    ReliabilityStatusDTO,
    VisualObservatoryDTO
)

logger = logging.getLogger(__name__)

class ControlPlaneService:
    """Core service coordinating operator queries and governed actions."""

    def __init__(
        self,
        event_bus: Optional[ControlPlaneEventStreamBus] = None,
        audit_logger: Optional[ControlPlaneAuditLogger] = None
    ):
        self.event_bus = event_bus or ControlPlaneEventStreamBus()
        self.audit_logger = audit_logger or ControlPlaneAuditLogger()

    def get_dashboard_snapshot(
        self,
        context: OperatorContext,
        target_tenant: str,
        target_client: str
    ) -> OperationalSnapshot:
        """Retrieves an operational snapshot ensuring strict tenant boundary and permissions."""
        PermissionGuard.enforce_capability(context, OperatorCapability.VIEW_CLIENT)
        PermissionGuard.enforce_tenant_boundary(context, target_tenant, target_client)

        self.audit_logger.record_event(ControlPlaneAuditEvent(
            operator_id=context.operator_id,
            tenant_id=context.tenant_id,
            client_id=context.client_id,
            action="GET_DASHBOARD_SNAPSHOT",
            target_resource=f"{target_tenant}:{target_client}",
            correlation_id=context.correlation_id
        ))

        # Default sample DTO metrics for demonstration/testing
        rel_dto = ReliabilityStatusDTO(
            overall_health="HEALTHY",
            availability_slo_pct=99.9,
            observed_availability_pct=100.0,
            p95_latency_ms=450.0,
            error_budget_burn_pct=0.0,
            active_circuit_breakers=[],
            open_incidents_count=0
        )
        vis_dto = VisualObservatoryDTO(
            total_artifacts=12,
            lineage_valid_pct=100.0,
            average_quality_score=0.94,
            active_quarantined_count=0,
            latest_benchmark_version="v24.2",
            drift_status="STABLE"
        )
        campaigns = [
            CampaignSummaryDTO(
                campaign_id="cmp-autumn-equinox-2026",
                tenant_id=target_tenant,
                client_id=target_client,
                name="Autumn Equinox Capsule",
                state="AUTHORIZED",
                version=1,
                progress_pct=85.0,
                approval_required=False,
                budget_allocated_usd=500.00,
                budget_spent_usd=0.106,
                created_at=1770000000.0,
                updated_at=1770003600.0
            )
        ]

        return SnapshotManager.capture_snapshot(
            tenant_id=target_tenant,
            client_id=target_client,
            correlation_id=context.correlation_id,
            reliability_dto=rel_dto,
            visual_dto=vis_dto,
            campaigns=campaigns,
            pending_approvals=0,
            queue_depth=1,
            ledger_valid=True
        )
