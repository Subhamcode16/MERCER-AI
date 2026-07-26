import json
import os
from app.models.campaign import Campaign

class LocalStore:
    """
    JSON-file based local storage for the MVP.
    TODO (Production): Swap storage to MongoDB (using Motor or PyMongo) when launching to real users, 
    and migrate local asset saving to cloud storage like AWS S3.
    """
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    def _get_path(self, campaign_id: str) -> str:
        return os.path.join(self.data_dir, f"{campaign_id}.json")

    def save_campaign(self, campaign: Campaign):
        path = self._get_path(campaign.id)
        with open(path, "w") as f:
            f.write(campaign.model_dump_json(indent=2))
            
    def get_campaign(self, campaign_id: str) -> Campaign:
        path = self._get_path(campaign_id)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)
            return Campaign(**data)
            
    def list_campaigns(self) -> list[Campaign]:
        campaigns = []
        for filename in os.listdir(self.data_dir):
            if filename.startswith("campaign_") and filename.endswith(".json"):
                path = os.path.join(self.data_dir, filename)
                with open(path, "r") as f:
                    data = json.load(f)
                    campaigns.append(Campaign(**data))
        return campaigns
