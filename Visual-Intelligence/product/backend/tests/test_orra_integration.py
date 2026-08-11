import pytest
import os
import asyncio
import unittest.mock as mock
from dotenv import load_dotenv

# Load environment variables from .env on startup
load_dotenv()
if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"

from app.database import connect_db, get_db, close_db
from app.storage.campaign_store import CampaignStore
from app.services.orra_loop import OrraLoop
from app.adapters.vision_adapter import VisionAdapter
from app.adapters.knowledge_adapter import KnowledgeAdapter
from app.adapters.honcho_adapter import HonchoAdapter
from app.models.campaign import Campaign, CreativeState, CreativeStrategy

@pytest.mark.asyncio
async def test_e2e_orra_loop_integration():
    # Set test environment DB settings
    os.environ["MONGODB_URI"] = "mongodb://localhost:27017"
    os.environ["MONGODB_DB_NAME"] = "mercer_integration_test_db"
    
    await connect_db()
    db = get_db()
    
    try:
        store = CampaignStore()
        
        # Initialize real adapters
        vision = VisionAdapter()
        knowledge = KnowledgeAdapter()
        honcho = HonchoAdapter()
        
        loop = OrraLoop(db=db, vision_adapter=vision, knowledge_adapter=knowledge, honcho_adapter=honcho)
        
        # Create and save a new Campaign
        campaign = Campaign(name="Integration Saree Campaign", user_id="user_test_999")
        await store.save_campaign(campaign)
        
        # 1. OBSERVE Phase
        obs_res = await loop.observe("mock_saree_photo.jpg", "user_test_999")
        assert obs_res["status"] == "verified"
        assert obs_res["dna"] is not None
        assert obs_res["dna"]["material"]["value"] == "Silk"
        
        # Save the DNA back to the campaign
        campaign.identity.product_dna = obs_res["dna"]
        await store.save_campaign(campaign)
        
        # 2. REASON Phase
        from app.adapters.prompt_engine import PromptEngine
        with mock.patch.object(PromptEngine, 'generate_recommendations') as mock_recommend:
            mock_recommend.return_value = {
                "background": {"value": "Heritage Fort / Palace Corridor", "reason": "Traditional setting."},
                "pose": {"value": "The Saree Column", "reason": "Traditional drape."},
                "lighting": {"value": "Golden Hour (2700K-3200K)", "reason": "Highlight zari."}
            }
            creative_state_dict = await loop.reason(obs_res["dna"], "Luxury Heritage Launch")
            assert creative_state_dict["status"] == "pending_green_signal"
            assert "strategy" in creative_state_dict
        
        # Populate the campaign v3 creative state
        campaign.v3_creative_state = CreativeState(
            product=creative_state_dict["product"],
            objective=creative_state_dict["objective"],
            strategy=CreativeStrategy(
                background=creative_state_dict["strategy"]["background"],
                lighting=creative_state_dict["strategy"]["lighting"],
                pose=creative_state_dict["strategy"]["pose"]
            ),
            status=creative_state_dict["status"]
        )
        await store.save_campaign(campaign)
        
        # 3. ACT Phase (Should fail before user approval)
        with pytest.raises(ValueError, match="Creative state must be approved"):
            await loop.act(campaign)
            
        # Simulate user approval (Green Signal)
        campaign.v3_creative_state.status = "approved"
        await store.save_campaign(campaign)
        
        # Verify campaign status is approved in the database
        updated_campaign = await store.get_campaign(campaign.id)
        assert updated_campaign.v3_creative_state.status == "approved"
        
        # 4. ACT Phase (Approved)
        with mock.patch.object(PromptEngine, 'generate_campaign_assets') as mock_gen:
            mock_gen.return_value = {
                "moodboard_brief": "Cinematic campaign brief details.",
                "prompts": {
                    "hero_image": "Shot of red silk saree.",
                    "product_closeup": "Shot of heavy gold zari border."
                }
            }
            act_result = await loop.act(campaign)
            assert act_result["status"] == "rendering"
            assert "job_id" in act_result
        
        # 5. REMEMBER Phase
        await loop.remember(campaign.id, {"feedback": "Dim the moonlight shadows."})
        
        print("End-to-End ORRA Loop Integration Test Verified successfully.")
    finally:
        # Clean up test database
        await db.client.drop_database("mercer_integration_test_db")
        await close_db()
