"""
Phase 25 Correlated Operational Snapshot Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import uuid
from src.control_plane.dto import ReliabilityStatusDTO, VisualObservatoryDTO, CampaignSummaryDTO

@dataclass
class OperationalSnapshot:
    snapshot_id: str = field(default_factory=lambda: f"snp-{uuid.uuid4().hex[:10]}")
    timestamp: float = field(default_factory=time.time)
    tenant_id: str = ""
    client_id: str = ""
    correlation_id: str = ""
    system_health: str = "HEALTHY"
    active_campaigns_count: int = 0
    pending_approvals_count: int = 0
    queue_depth: int = 0
    reliability: Optional[ReliabilityStatusDTO] = None
    visual_observatory: Optional[VisualObservatoryDTO] = None
    campaign_summaries: List[CampaignSummaryDTO] = field(default_factory=list)
    recent_incidents: List[Dict[str, Any]] = field(default_factory=list)
    evidence_ledger_intact: bool = True

class SnapshotManager:
    """Generates immutable, correlated operational snapshots for operator consoles."""

    @staticmethod
    def capture_snapshot(
        tenant_id: str,
        client_id: str,
        correlation_id: str,
        reliability_dto: ReliabilityStatusDTO,
        visual_dto: VisualObservatoryDTO,
        campaigns: List[CampaignSummaryDTO],
        pending_approvals: int,
        queue_depth: int,
        ledger_valid: bool
    ) -> OperationalSnapshot:
        return OperationalSnapshot(
            tenant_id=tenant_id,
            client_id=client_id,
            correlation_id=correlation_id,
            system_health=reliability_dto.overall_health,
            active_campaigns_count=len([c for c in campaigns if c.state in ["AUTHORIZED", "EXECUTING"]]),
            pending_approvals_count=pending_approvals,
            queue_depth=queue_depth,
            reliability=reliability_dto,
            visual_observatory=visual_dto,
            campaign_summaries=campaigns,
            evidence_ledger_intact=ledger_valid
        )
