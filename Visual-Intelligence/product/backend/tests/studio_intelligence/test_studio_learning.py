"""
Unit tests for StudioLearningEngine contract progression.
"""

import pytest
from src.studio_intelligence.outcome_models import OutcomeObservation
from src.studio_intelligence.studio_learning import StudioLearningEngine
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


def test_studio_learning_engine_contract_progression():
    engine = StudioLearningEngine()
    obs = OutcomeObservation(
        observation_id="obs_learn_1",
        client_id="client_nocap",
        campaign_id="camp_1",
        deliverable_id="deliv_1",
        work_item_id="item_1",
        platform="instagram",
        metrics={
            "impressions": 15000.0,
            "engagements": 1000.0,
            "clicks": 450.0,
            "approval_latency_sec": 3600.0,
            "publishing_errors": 0.0,
        },
        raw_payload={},
    )

    with pytest.raises(CrossClientIntelligenceViolation):
        engine.process_observation_to_learning_signal(
            requesting_client_id="client_other", observation=obs
        )

    res = engine.process_observation_to_learning_signal(
        requesting_client_id="client_nocap",
        observation=obs,
        client_feedback_text="Great work",
        human_review_score=0.9,
    )
    assert res["attribution"].observation_id == "obs_learn_1"
    assert res["evaluation"].overall_score > 0.8
    assert res["signal"].signal_id.startswith("sig_")
