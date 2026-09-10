"""
Phase 27 Campaign Command Center & Studio Campaign Lifecycle.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


class StudioCampaignStatus(str, Enum):
    INTAKE_DISCOVERY = "INTAKE_DISCOVERY"
    CREATIVE_INTELLIGENCE = "CREATIVE_INTELLIGENCE"
    DIRECTION_PROPOSALS = "DIRECTION_PROPOSALS"
    VISUAL_EXPLORATION = "VISUAL_EXPLORATION"
    CRITIQUE_AND_REVIEW = "CRITIQUE_AND_REVIEW"
    READY_FOR_LAUNCH = "READY_FOR_LAUNCH"
    LAUNCHED = "LAUNCHED"
    COMPLETED = "COMPLETED"
    # Aliases
    DRAFT = "DRAFT"
    DISCOVERY = "DISCOVERY"
    INTELLIGENCE = "INTELLIGENCE"
    DIRECTION_SELECTION = "DIRECTION_SELECTION"
    VISUAL_DEVELOPMENT = "VISUAL_DEVELOPMENT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PRODUCTION = "PRODUCTION"


class CampaignStudioError(RuntimeError):
    pass


@dataclass
class StudioCampaign:
    campaign_id: str
    tenant_id: str
    client_id: str
    brand_id: str
    product_id: str
    title: str
    name: str
    objective: str
    description: str
    created_by: str
    status: StudioCampaignStatus = StudioCampaignStatus.INTAKE_DISCOVERY
    version: int = 1
    creative_room_id: Optional[str] = None
    selected_direction_id: Optional[str] = None
    missions: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CampaignWorkspaceManager:
    """Manages Studio Campaigns and ensures optimistic locking across stage transitions."""

    def __init__(self):
        self._campaigns: Dict[str, StudioCampaign] = {}

    def create_campaign(
        self,
        campaign_id: Optional[str] = None,
        tenant_id: str = "tenant_default",
        client_id: str = "cli_default",
        brand_id: str = "brd_default",
        product_id: str = "prd_default",
        title: Optional[str] = None,
        name: Optional[str] = None,
        objective: str = "",
        description: str = "",
        created_by: str = "system",
        creative_room_id: Optional[str] = None,
    ) -> StudioCampaign:
        camp_id = campaign_id or f"camp_{uuid.uuid4().hex[:10]}"
        camp_title = title or name or "Untitled Campaign"
        campaign = StudioCampaign(
            campaign_id=camp_id,
            tenant_id=tenant_id,
            client_id=client_id,
            brand_id=brand_id,
            product_id=product_id,
            title=camp_title,
            name=camp_title,
            objective=objective or description,
            description=description or objective,
            created_by=created_by,
            creative_room_id=creative_room_id,
        )
        self._campaigns[camp_id] = campaign
        return campaign

    def get_campaign(self, campaign_id: str, tenant_id: str = "*") -> Optional[StudioCampaign]:
        camp = self._campaigns.get(campaign_id)
        if camp and (camp.tenant_id == tenant_id or tenant_id == "*"):
            return camp
        return None

    def list_campaigns(self, tenant_id: str = "*", client_id: Optional[str] = None) -> List[StudioCampaign]:
        results = []
        for camp in self._campaigns.values():
            if camp.tenant_id != tenant_id and tenant_id != "*":
                continue
            if client_id and camp.client_id != client_id and client_id != "*":
                continue
            results.append(camp)
        return results

    def transition_status(
        self,
        campaign_id: str,
        target_status: StudioCampaignStatus,
        operator_id: str = "system",
        expected_version: int = 1,
        tenant_id: str = "*",
    ) -> StudioCampaign:
        camp = self.get_campaign(campaign_id, tenant_id)
        if not camp:
            raise CampaignStudioError(f"Campaign '{campaign_id}' not found")
        if camp.version != expected_version:
            raise CampaignStudioError(
                f"Optimistic locking conflict: Expected version {expected_version}, but current version is {camp.version}"
            )
        
        camp.status = target_status
        camp.version += 1
        camp.updated_at = datetime.now(timezone.utc).isoformat()
        return camp
