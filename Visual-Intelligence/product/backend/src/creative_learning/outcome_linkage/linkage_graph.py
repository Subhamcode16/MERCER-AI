"""
Phase 28 Version-Aware Outcome Linkage Graph.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


@dataclass
class OutcomeLinkageNode:
    linkage_id: str
    campaign_id: str
    direction_id: str
    asset_id: str
    asset_version: int
    channel: str
    metric_ids: List[str]
    production_release_version: int
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class OutcomeLinkageGraph:
    """Binds normalized outcome metrics to exact immutable production asset versions."""

    def __init__(self):
        self._links: Dict[str, OutcomeLinkageNode] = {}  # linkage_id -> node
        self._asset_outcomes: Dict[str, List[str]] = {}  # asset_id -> [linkage_id, ...]

    def link_outcome(
        self,
        campaign_id: str,
        direction_id: str,
        asset_id: str,
        asset_version: int,
        channel: str,
        metric_ids: List[str],
        production_release_version: int = 1,
    ) -> OutcomeLinkageNode:
        linkage_id = f"lnk_{uuid.uuid4().hex[:8]}"
        node = OutcomeLinkageNode(
            linkage_id=linkage_id,
            campaign_id=campaign_id,
            direction_id=direction_id,
            asset_id=asset_id,
            asset_version=asset_version,
            channel=channel,
            metric_ids=metric_ids,
            production_release_version=production_release_version,
        )
        self._links[linkage_id] = node
        if asset_id not in self._asset_outcomes:
            self._asset_outcomes[asset_id] = []
        self._asset_outcomes[asset_id].append(linkage_id)
        return node

    def get_linkage_for_asset(self, asset_id: str) -> List[OutcomeLinkageNode]:
        link_ids = self._asset_outcomes.get(asset_id, [])
        return [self._links[lid] for lid in link_ids]
