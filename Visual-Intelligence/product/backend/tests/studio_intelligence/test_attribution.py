"""
Unit tests for CreativeOutcomeAttributionEngine.
"""

import pytest
from src.studio_intelligence.outcome_models import OutcomeObservation
from src.studio_intelligence.attribution import CreativeOutcomeAttributionEngine
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


def test_creative_outcome_attribution():
    engine = CreativeOutcomeAttributionEngine()
    obs = OutcomeObservation(
        observation_id="obs_attr_1",
        client_id="client_nocap",
        campaign_id="camp_1",
        deliverable_id="deliv_1",
        work_item_id="item_1",
        platform="instagram",
        metrics={"impressions": 10000.0},
        raw_payload={},
    )

    with pytest.raises(CrossClientIntelligenceViolation):
        engine.attribute_outcome(requesting_client_id="client_other", observation=obs)

    attr = engine.attribute_outcome(
        requesting_client_id="client_nocap",
        observation=obs,
        staff_ids=["staff_cd_1"],
        creative_direction_id="cd_bold_urban",
    )
    assert attr.observation_id == "obs_attr_1"
    assert attr.creative_direction_id == "cd_bold_urban"
    assert "staff_cd_1" in attr.staff_ids
