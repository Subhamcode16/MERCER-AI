import pytest
import unittest.mock as mock
from app.services.orra_loop import OrraLoop
from app.models.campaign import Campaign, ProductDNA, ConfidenceField, CreativeState, CreativeStrategy

class MockVisionAdapter:
    def analyze_product(self, image_url: str):
        dna = ProductDNA(
            material=ConfidenceField(value="Silk", confidence=0.99),
            weaving_technique=ConfidenceField(value="Banarasi", confidence=0.95),
            primary_features=ConfidenceField(value=["Gold Zari Brocade"], confidence=0.97),
            cultural_context=ConfidenceField(value="Varanasi", confidence=0.90),
            raw_claims=[]
        )
        return dna, {"title": "Festive Palace", "body": "Intricate saree campaign"}, False

class MockKnowledgeAdapter:
    def retrieve_context(self, dna):
        return "Banarasi silk drape rules"

class MockHonchoAdapter:
    def get_context(self):
        return "Brand preferences"

@pytest.mark.asyncio
async def test_orra_loop_lifecycle():
    vision = MockVisionAdapter()
    knowledge = MockKnowledgeAdapter()
    honcho = MockHonchoAdapter()
    
    loop = OrraLoop(db=None, vision_adapter=vision, knowledge_adapter=knowledge, honcho_adapter=honcho)
    
    # 1. OBSERVE
    obs_res = await loop.observe("https://image.url/saree.jpg", "user_123")
    assert obs_res["status"] == "verified"
    assert obs_res["dna"]["material"]["value"] == "Silk"
    assert obs_res["is_mock"] is False

    # 2. REASON
    # We mock the PromptEngine.generate_recommendations to isolate unit test
    from app.adapters.prompt_engine import PromptEngine
    with mock.patch.object(PromptEngine, 'generate_recommendations') as mock_recommend:
        mock_recommend.return_value = {
            "background": {"value": "Heritage Fort / Palace Corridor", "reason": "Traditional setting."},
            "pose": {"value": "The Saree Column", "reason": "Traditional drape."},
            "lighting": {"value": "Golden Hour (2700K-3200K)", "reason": "Highlight zari."}
        }
        reason_res = await loop.reason(obs_res["dna"], "Luxury Campaign")
        assert reason_res["status"] == "pending_green_signal"
        assert reason_res["strategy"]["background"] == "Heritage Fort / Palace Corridor"

    # 3. ACT (should fail if not approved)
    campaign = Campaign(name="Test Campaign", user_id="user_123")
    campaign.v3_creative_state = CreativeState(
        product=obs_res["dna"],
        objective="luxury_campaign",
        strategy=CreativeStrategy(
            background=reason_res["strategy"]["background"],
            lighting=reason_res["strategy"]["lighting"],
            pose=reason_res["strategy"]["pose"]
        ),
        status=reason_res["status"]
    )
    
    with pytest.raises(ValueError, match="Creative state must be approved"):
        await loop.act(campaign)

    # Simulate user approval (Green Signal)
    campaign.v3_creative_state.status = "approved"

    # 4. ACT (approved)
    with mock.patch.object(PromptEngine, 'generate_campaign_assets') as mock_gen:
        mock_gen.return_value = {
            "moodboard_brief": "Cinematic shoot in nocturnal palace.",
            "prompts": {
                "hero_image": "Shot of red saree model.",
                "product_closeup": "Shot of zari border."
            }
        }
        act_res = await loop.act(campaign)
        assert act_res["status"] == "rendering"
        assert act_res["moodboard_brief"] == "Cinematic shoot in nocturnal palace."

    # 5. REMEMBER
    await loop.remember("campaign_123", {"feedback": "Good lighting"})
