"""
Tests for Phase 27 Creative Intelligence & Direction Management.
"""
import pytest
from src.campaign_studio.creative_intelligence import CreativeIntelligenceEngine
from src.campaign_studio.direction_management import DirectionManager


def test_creative_intelligence_synthesis():
    engine = CreativeIntelligenceEngine()
    campaign_id = "camp_intel_01"
    intel = engine.synthesize_intelligence(campaign_id, "Aethelgard Paris", {})
    
    assert intel["campaign_id"] == campaign_id
    assert intel["brand_name"] == "Aethelgard Paris"
    assert len(intel["market_signals"]) >= 2
    assert len(intel["audience_tensions"]) >= 1
    assert len(intel["hypotheses"]) >= 2


def test_direction_selection_and_refinement():
    mgr = DirectionManager()
    campaign_id = "camp_dir_01"
    cards = mgr.generate_candidate_directions(campaign_id)
    assert len(cards) == 3
    assert not any(c.is_selected for c in cards)

    # Select direction 1
    target_id = cards[0].direction_id
    selected = mgr.select_direction(campaign_id, target_id)
    assert selected.is_selected
    assert selected.direction_id == target_id

    # Refine direction
    refined = mgr.refine_direction(campaign_id, target_id, "Emphasize architectural limestone textures")
    assert "Emphasize architectural limestone textures" in refined.core_idea
    assert len(refined.refinement_history) == 1
