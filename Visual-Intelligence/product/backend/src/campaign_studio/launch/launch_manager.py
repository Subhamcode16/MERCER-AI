"""
Phase 27 Campaign Launch & Distribution Manager.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


class LaunchState(str, Enum):
    DRAFT = "DRAFT"
    READY = "READY"
    STAGED = "STAGED"
    LAUNCHED = "LAUNCHED"
    PAUSED = "PAUSED"


@dataclass
class ChannelPackage:
    channel_name: str  # "E-commerce Hero", "Instagram", "Digital OOH", "Press Release"
    asset_ids: List[str]
    status: str = "PREPARED"


@dataclass
class LaunchManifest:
    launch_id: str
    campaign_id: str
    channels: List[ChannelPackage]
    state: LaunchState
    pre_launch_checks_passed: bool
    launched_by: Optional[str] = None
    launched_at: Optional[datetime] = None


class LaunchManager:
    """Manages multi-channel staging, release verification, and campaign launches."""

    def __init__(self):
        self._launches: Dict[str, LaunchManifest] = {}  # campaign_id -> manifest

    def stage_launch(self, campaign_id: str, channel_allocations: Dict[str, List[str]], verified_assets: List[str]) -> LaunchManifest:
        channels = [
            ChannelPackage(channel_name=ch, asset_ids=aids)
            for ch, aids in channel_allocations.items()
        ]
        manifest = LaunchManifest(
            launch_id=f"lnc_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            channels=channels,
            state=LaunchState.STAGED,
            pre_launch_checks_passed=len(verified_assets) > 0,
        )
        self._launches[campaign_id] = manifest
        return manifest

    def execute_launch(self, campaign_id: str, operator: OperatorContext) -> LaunchManifest:
        manifest = self._launches.get(campaign_id)
        if not manifest:
            raise KeyError(f"No launch manifest found for campaign '{campaign_id}'")

        if not manifest.pre_launch_checks_passed:
            raise ValueError(f"Campaign '{campaign_id}' has not passed pre-launch verification checks.")

        allowed_roles = {OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.SUPER_ADMIN}
        if operator.role not in allowed_roles:
            raise PermissionError(f"Operator '{operator.operator_id}' lacks permission to launch campaign.")

        manifest.state = LaunchState.LAUNCHED
        manifest.launched_by = operator.operator_id
        manifest.launched_at = datetime.now(timezone.utc)
        return manifest

    def get_manifest(self, campaign_id: str) -> Optional[LaunchManifest]:
        return self._launches.get(campaign_id)
