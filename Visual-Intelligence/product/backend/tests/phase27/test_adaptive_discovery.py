"""
Tests for Phase 27 Adaptive Epistemic Discovery Engine.
"""
import pytest
from src.campaign_studio.discovery import (
    AdaptiveDiscoveryEngine,
    DiscoveryEpistemicState,
)


def test_discovery_engine_epistemic_analysis():
    engine = AdaptiveDiscoveryEngine()
    campaign_id = "camp_disc_01"

    # Incomplete intake
    items = engine.analyze_intake(campaign_id, {
        "season": "Spring/Summer 2027",
    })
    
    item_map = {item.dimension: item for item in items}
    assert item_map["season"].state == DiscoveryEpistemicState.KNOWN
    assert item_map["season"].value == "Spring/Summer 2027"

    assert item_map["target_audience"].state == DiscoveryEpistemicState.MISSING
    assert item_map["visual_tone"].state == DiscoveryEpistemicState.MISSING

    questions = engine.get_pending_questions(campaign_id)
    assert len(questions) == 2

    # Answer a question
    q_aud = next(q for q in questions if q.dimension == "target_audience")
    resolved = engine.answer_question(campaign_id, q_aud.question_id, "Affluent Minimalists")
    assert resolved.state == DiscoveryEpistemicState.KNOWN
    assert resolved.value == "Affluent Minimalists"

    # Verify remaining questions
    rem_questions = engine.get_pending_questions(campaign_id)
    assert len(rem_questions) == 1
    assert rem_questions[0].dimension == "visual_tone"
