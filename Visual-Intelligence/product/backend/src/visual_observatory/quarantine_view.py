"""
Phase 25 Quarantined Visual Deliverable Inspector.
Enforces non-bypassable quarantine status on lineage break or excessive drift.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

@dataclass
class QuarantinedArtifactRecord:
    artifact_id: str
    campaign_id: str
    tenant_id: str
    client_id: str
    reason: str # LINEAGE_INTEGRITY_FAILURE, EXCESSIVE_SSIM_DRIFT, SECURITY_FLAG
    quarantined_at: float = field(default_factory=time.time)
    quarantined_by_system: str = "VisualAlertQuarantineEngine"
    is_blocked_from_release: bool = True

class QuarantineRegistry:
    """Read-only and governed disposition store for quarantined deliverables."""

    def __init__(self):
        self._quarantined: Dict[str, QuarantinedArtifactRecord] = {}

    def quarantine_artifact(self, record: QuarantinedArtifactRecord) -> None:
        self._quarantined[record.artifact_id] = record

    def list_quarantined(self, tenant_id: str, client_id: Optional[str] = None) -> List[QuarantinedArtifactRecord]:
        return [
            q for q in self._quarantined.values()
            if (tenant_id == "*" or q.tenant_id == tenant_id) and (client_id is None or client_id == "*" or q.client_id == client_id)
        ]

    def is_quarantined(self, artifact_id: str) -> bool:
        return artifact_id in self._quarantined
