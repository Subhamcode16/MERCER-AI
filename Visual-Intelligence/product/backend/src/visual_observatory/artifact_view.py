"""
Phase 25 Visual Artifact Inspector and Metadata Projection.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

@dataclass
class VisualArtifactProjection:
    artifact_id: str
    campaign_id: str
    tenant_id: str
    client_id: str
    model_provider: str
    model_version: str
    dimensions: str # e.g. "1024x1024"
    aspect_ratio: str # e.g. "1:1", "16:9"
    artifact_hash: str
    lineage_hash: str
    quality_score: float
    ssim_drift_score: float
    status: str # ACTIVE, QUARANTINED, RETIRED
    quarantine_reason: Optional[str] = None
    created_at: float = field(default_factory=time.time)
