"""
Phase 25 Deliverable Detail Projection with Lineage and Quality Scores.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class DeliverableDetailProjection:
    deliverable_id: str
    campaign_id: str
    title: str
    deliverable_type: str
    status: str # DRAFT, CRITIQUED, APPROVED, REJECTED, QUARANTINED
    artifact_id: Optional[str] = None
    artifact_hash: Optional[str] = None
    lineage_hash: Optional[str] = None
    quality_score: Optional[float] = None
    color_fidelity_delta: Optional[float] = None
    critique_verdict: Optional[str] = None
    quarantined: bool = False
    quarantine_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
