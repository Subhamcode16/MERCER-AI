"""
Phase 27 State Projection & Materialized Read Models.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from src.control_plane.dto import DTOSanitizer


@dataclass
class StudioOverviewProjection:
    campaign_id: str
    client_name: str
    brand_name: str
    title: str
    status: str
    version: int
    asset_count: int
    pending_approvals_count: int
    readiness_score: float
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class StateProjectionEngine:
    """Projects high-performance, sanitized read-models for UI surfaces. Invariant: Projection ≠ Source of Authority."""

    def __init__(self):
        self._projections: Dict[str, StudioOverviewProjection] = {}

    def project_campaign_overview(
        self,
        campaign_id: str,
        client_name: str,
        brand_name: str,
        title: str,
        status: str,
        version: int,
        asset_count: int,
        pending_approvals_count: int,
        readiness_score: float = 0.95,
    ) -> Dict[str, Any]:
        proj = StudioOverviewProjection(
            campaign_id=campaign_id,
            client_name=client_name,
            brand_name=brand_name,
            title=title,
            status=status,
            version=version,
            asset_count=asset_count,
            pending_approvals_count=pending_approvals_count,
            readiness_score=readiness_score,
        )
        self._projections[campaign_id] = proj
        raw_dict = {
            "campaign_id": proj.campaign_id,
            "client_name": proj.client_name,
            "brand_name": proj.brand_name,
            "title": proj.title,
            "status": proj.status,
            "version": proj.version,
            "asset_count": proj.asset_count,
            "pending_approvals_count": proj.pending_approvals_count,
            "readiness_score": proj.readiness_score,
            "last_updated": proj.last_updated.isoformat(),
            "_projection_notice": "Projection is a read-only materialized view. Projection ≠ Source of Authority.",
        }
        return DTOSanitizer.sanitize(raw_dict)

    def get_projection(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        proj = self._projections.get(campaign_id)
        if not proj:
            return None
        return DTOSanitizer.sanitize({
            "campaign_id": proj.campaign_id,
            "client_name": proj.client_name,
            "brand_name": proj.brand_name,
            "title": proj.title,
            "status": proj.status,
            "version": proj.version,
            "asset_count": proj.asset_count,
            "pending_approvals_count": proj.pending_approvals_count,
            "readiness_score": proj.readiness_score,
            "last_updated": proj.last_updated.isoformat(),
        })
