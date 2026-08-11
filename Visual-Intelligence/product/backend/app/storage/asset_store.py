import os
import shutil
import asyncio
import logging
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class AssetStore:
    """
    Supabase Storage for campaign assets.
    If Supabase credentials are not configured, it falls back to local disk storage.
    """

    def __init__(self, base_dir: str = "data"):
        # Check if Supabase URL and anon key are present and not default dummy values
        self.use_supabase = bool(
            settings.supabase_url and 
            settings.supabase_anon_key and 
            "your-supabase" not in settings.supabase_url
        )
        
        self.assets_dir = os.path.join(base_dir, "assets")
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
            
        if self.use_supabase:
            try:
                from supabase import create_client, Client
                self.supabase_client: Client = create_client(settings.supabase_url, settings.supabase_anon_key)
                self.bucket_name = "campaign-assets"
                logger.info("[AssetStore] Supabase Storage client initialized.")
            except Exception as e:
                logger.error(f"[AssetStore] Failed to initialize Supabase client: {e}. Falling back to local storage.")
                self.use_supabase = False

    def _campaign_dir(self, campaign_id: str) -> str:
        path = os.path.join(self.assets_dir, campaign_id)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    async def save_material(self, campaign_id: str, file_bytes: bytes, filename: str) -> str:
        """
        Saves the uploaded material image.
        Returns the public URL (if Supabase) or local relative path (if local).
        """
        ext = os.path.splitext(filename)[-1].lower() or ".jpg"
        save_name = f"material{ext}"
        content_type = f"image/{ext.strip('.')}"
        if content_type == "image/jpg":
            content_type = "image/jpeg"
        
        if self.use_supabase:
            object_name = f"assets/{campaign_id}/{save_name}"
            try:
                # Execute in thread executor to avoid blocking async loop if supabase client blocks
                def _upload():
                    # Check if file already exists by trying to remove it first to allow overwrites
                    try:
                        self.supabase_client.storage.from_(self.bucket_name).remove([object_name])
                    except Exception:
                        pass
                    return self.supabase_client.storage.from_(self.bucket_name).upload(
                        path=object_name,
                        file=file_bytes,
                        file_options={"content-type": content_type}
                    )
                await asyncio.to_thread(_upload)
                
                # Get the public URL
                public_url = self.supabase_client.storage.from_(self.bucket_name).get_public_url(object_name)
                logger.info(f"[AssetStore] Uploaded {object_name} to Supabase. URL: {public_url}")
                return public_url
            except Exception as e:
                logger.error(f"[AssetStore] Supabase upload failed: {e}. Falling back to local storage.")
        
        # Fallback to local
        save_path = os.path.join(self._campaign_dir(campaign_id), save_name)
        def _write():
            with open(save_path, "wb") as f:
                f.write(file_bytes)
        await asyncio.to_thread(_write)
        return save_path

    async def save_asset(self, file_bytes: bytes, filename: str) -> str:
        """
        Saves a generated asset image.
        """
        # Save assets under the 'generated' folder in Supabase or local assets dir
        ext = os.path.splitext(filename)[-1].lower() or ".png"
        content_type = f"image/{ext.strip('.')}"
        
        if self.use_supabase:
            object_name = f"generated/{filename}"
            try:
                def _upload():
                    try:
                        self.supabase_client.storage.from_(self.bucket_name).remove([object_name])
                    except Exception:
                        pass
                    return self.supabase_client.storage.from_(self.bucket_name).upload(
                        path=object_name,
                        file=file_bytes,
                        file_options={"content-type": content_type}
                    )
                await asyncio.to_thread(_upload)
                public_url = self.supabase_client.storage.from_(self.bucket_name).get_public_url(object_name)
                logger.info(f"[AssetStore] Saved generated asset {object_name} to Supabase. URL: {public_url}")
                return public_url
            except Exception as e:
                logger.error(f"[AssetStore] Supabase asset upload failed: {e}. Falling back to local.")
                
        # Fallback to local
        save_path = os.path.join(self._campaign_dir("generated"), filename)
        def _write():
            with open(save_path, "wb") as f:
                f.write(file_bytes)
        await asyncio.to_thread(_write)
        return save_path

    async def delete_campaign_assets(self, campaign_id: str):
        """
        Deletes all assets for a campaign.
        """
        if self.use_supabase:
            prefix = f"assets/{campaign_id}"
            try:
                def _delete():
                    # List files in the folder
                    files = self.supabase_client.storage.from_(self.bucket_name).list(prefix)
                    if files:
                        paths = [f"{prefix}/{f['name']}" for f in files]
                        self.supabase_client.storage.from_(self.bucket_name).remove(paths)
                await asyncio.to_thread(_delete)
                logger.info(f"[AssetStore] Deleted Supabase assets under prefix {prefix}")
                return
            except Exception as e:
                logger.error(f"[AssetStore] Supabase delete failed: {e}. Falling back to local.")

        # Fallback to local
        campaign_dir = os.path.join(self.assets_dir, campaign_id)
        if os.path.exists(campaign_dir):
            def _rm():
                shutil.rmtree(campaign_dir)
            await asyncio.to_thread(_rm)
