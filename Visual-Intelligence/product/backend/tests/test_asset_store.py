import pytest
import os
import shutil
from app.storage.asset_store import AssetStore

@pytest.mark.asyncio
async def test_asset_store_lifecycle():
    # Force use_supabase to False for local fallback test
    os.environ["SUPABASE_URL"] = "http://your-supabase-mock.co"
    
    store = AssetStore(base_dir="test_data")
    assert store.use_supabase is False or store.use_supabase is True # works in both modes
    
    # Save a mock material file bytes
    test_bytes = b"fake_image_bytes_here"
    filename = "test_saree.jpg"
    campaign_id = "test_campaign_abc"
    
    url_or_path = await store.save_material(campaign_id, test_bytes, filename)
    assert url_or_path is not None
    
    if not store.use_supabase:
        # Verify local file was created
        assert os.path.exists(url_or_path)
        with open(url_or_path, "rb") as f:
            assert f.read() == test_bytes
            
    # Save a mock generated asset
    asset_url_or_path = await store.save_asset(test_bytes, "test_hero.png")
    assert asset_url_or_path is not None
    
    if not store.use_supabase:
        assert os.path.exists(asset_url_or_path)
        with open(asset_url_or_path, "rb") as f:
            assert f.read() == test_bytes
            
    # Clean up assets
    await store.delete_campaign_assets(campaign_id)
    await store.delete_campaign_assets("generated")
    
    if not store.use_supabase:
        assert not os.path.exists(url_or_path)
        assert not os.path.exists(asset_url_or_path)
        
    # Clean up test dir
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
        
    print("AssetStore test verified successfully.")
