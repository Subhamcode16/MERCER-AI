"""
Phase 15 Campaign Lifecycle Manager.
Controls campaign state transitions (PLANNED, ACTIVE, PAUSED, COMPLETED, CANCELLED, RESUMED) with strict client isolation.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from src.studio_operations.exceptions import CampaignStateViolation, ClientContextViolation
from src.studio_operations.studio_models import Campaign, CampaignStatus, OperationalPriority, CampaignCadence

VALID_CAMPAIGN_TRANSITIONS = {
    CampaignStatus.PLANNED: {CampaignStatus.ACTIVE, CampaignStatus.CANCELLED},
    CampaignStatus.ACTIVE: {CampaignStatus.PAUSED, CampaignStatus.COMPLETED, CampaignStatus.CANCELLED},
    CampaignStatus.PAUSED: {CampaignStatus.RESUMED, CampaignStatus.ACTIVE, CampaignStatus.CANCELLED},
    CampaignStatus.RESUMED: {CampaignStatus.ACTIVE, CampaignStatus.PAUSED, CampaignStatus.COMPLETED, CampaignStatus.CANCELLED},
    CampaignStatus.COMPLETED: set(),
    CampaignStatus.CANCELLED: set(),
}

class CampaignLifecycleManager:
    """Manages creation, activation, pausing, completion, and health tracking of campaigns."""

    def __init__(self):
        self._campaigns: Dict[str, Campaign] = {}

    def create_campaign(
        self,
        requesting_client_id: str,
        campaign_id: str,
        client_id: str,
        brand_id: str,
        title: str,
        objective: str,
        cadence: CampaignCadence = CampaignCadence.WEEKLY,
        priority: OperationalPriority = OperationalPriority.MEDIUM
    ) -> Campaign:
        """Creates a campaign under explicit client isolation checks."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot create campaign for client '{client_id}' from requesting context '{requesting_client_id}'."
            )
        if campaign_id in self._campaigns:
            raise CampaignStateViolation(f"Campaign '{campaign_id}' already exists.")

        campaign = Campaign(
            campaign_id=campaign_id,
            client_id=client_id,
            brand_id=brand_id,
            title=title,
            objective=objective,
            cadence=cadence,
            priority=priority,
            status=CampaignStatus.PLANNED
        )
        self._campaigns[campaign_id] = campaign
        return campaign

    def transition_campaign(
        self,
        requesting_client_id: str,
        campaign_id: str,
        target_status: CampaignStatus
    ) -> Campaign:
        """Transitions campaign state with validation and isolation checks."""
        campaign = self.get_campaign(requesting_client_id, campaign_id)
        valid_next = VALID_CAMPAIGN_TRANSITIONS.get(campaign.status, set())
        
        if target_status not in valid_next:
            raise CampaignStateViolation(
                f"Invalid campaign transition from {campaign.status.value} to {target_status.value} for campaign '{campaign_id}'."
            )
        
        campaign.status = target_status
        campaign.updated_at = datetime.now(timezone.utc).isoformat()
        return campaign

    def get_campaign(self, requesting_client_id: str, campaign_id: str) -> Campaign:
        """Retrieves campaign with strict client isolation check."""
        if campaign_id not in self._campaigns:
            raise CampaignStateViolation(f"Campaign '{campaign_id}' not found.")
        campaign = self._campaigns[campaign_id]
        if requesting_client_id != campaign.client_id:
            raise ClientContextViolation(
                f"CROSS-CLIENT LEAKAGE: Client '{requesting_client_id}' cannot access campaign '{campaign_id}' owned by '{campaign.client_id}'."
            )
        return campaign

    def list_campaigns(self, requesting_client_id: str, status_filter: Optional[CampaignStatus] = None) -> List[Campaign]:
        """Lists all campaigns for a specific client."""
        client_campaigns = [
            c for c in self._campaigns.values()
            if c.client_id == requesting_client_id
        ]
        if status_filter:
            client_campaigns = [c for c in client_campaigns if c.status == status_filter]
        return client_campaigns
