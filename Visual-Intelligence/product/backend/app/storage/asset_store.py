import os
import shutil
from typing import Optional

class AssetStore:
    """
    Binary file storage for campaign assets (uploaded images, generated outputs).
    Saves files to data/assets/{campaign_id}/ on the local filesystem.

    TODO (Production): Replace with an S3 client (boto3) that uploads to
    s3://bucket/assets/{campaign_id}/ and returns a signed CDN URL.
    """

    def __init__(self, base_dir: str = "data"):
        self.assets_dir = os.path.join(base_dir, "assets")
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

    def _campaign_dir(self, campaign_id: str) -> str:
        path = os.path.join(self.assets_dir, campaign_id)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def save_material(self, campaign_id: str, file_bytes: bytes, filename: str) -> str:
        """
        Saves the uploaded material image for a campaign.
        Returns the relative file path for storage in the Campaign JSON.
        """
        ext = os.path.splitext(filename)[-1].lower() or ".jpg"
        save_name = f"material{ext}"
        save_path = os.path.join(self._campaign_dir(campaign_id), save_name)
        with open(save_path, "wb") as f:
            f.write(file_bytes)
        return save_path

    def get_material_path(self, campaign_id: str) -> Optional[str]:
        """
        Returns the path to the campaign's uploaded material image, or None if not uploaded yet.
        """
        campaign_dir = os.path.join(self.assets_dir, campaign_id)
        if not os.path.exists(campaign_dir):
            return None
        for fname in os.listdir(campaign_dir):
            if fname.startswith("material"):
                return os.path.join(campaign_dir, fname)
        return None

    def delete_campaign_assets(self, campaign_id: str):
        """
        Deletes all assets for a campaign (called when a campaign folder is deleted from the UI).
        """
        campaign_dir = os.path.join(self.assets_dir, campaign_id)
        if os.path.exists(campaign_dir):
            shutil.rmtree(campaign_dir)
