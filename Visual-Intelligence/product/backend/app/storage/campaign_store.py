import logging
from typing import List, Optional

from app.database import get_db
from app.models.campaign import Campaign

logger = logging.getLogger(__name__)

class CampaignStore:
    """
    MongoDB storage for Campaigns.
    Replaces the local JSON file storage (LocalStore).
    """
    
    @property
    def collection(self):
        return get_db()["campaigns"]
        
    async def save_campaign(self, campaign: Campaign):
        """Upsert a campaign document into MongoDB."""
        data = campaign.model_dump(by_alias=True)
        await self.collection.update_one(
            {"id": campaign.id},
            {"$set": data},
            upsert=True
        )
        
    async def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Retrieve a campaign by ID."""
        data = await self.collection.find_one({"id": campaign_id})
        if data:
            return Campaign(**data)
        return None
        
    async def list_campaigns(self, user_id: str = None) -> List[Campaign]:
        """List all campaigns (sorted by created_at). Filters by user_id if provided."""
        query = {}
        if user_id:
            query["user_id"] = user_id
        cursor = self.collection.find(query).sort("created_at", 1)
        campaigns = []
        async for doc in cursor:
            campaigns.append(Campaign(**doc))
        return campaigns
        
    async def delete_campaign(self, campaign_id: str):
        """Delete a campaign."""
        await self.collection.delete_one({"id": campaign_id})
