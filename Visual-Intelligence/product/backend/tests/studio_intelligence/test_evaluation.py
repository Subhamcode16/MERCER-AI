"""
Unit tests for CreativePerformanceEvaluator.
"""

import pytest
from src.studio_intelligence.outcome_models import OutcomeObservation
from src.studio_intelligence.evaluation import CreativePerformanceEvaluator
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


def test_creative_performance_evaluator():
    evaluator = CreativePerformanceEvaluator()
    obs = OutcomeObservation(
        observation_id="obs_eval_1",
        client_id="client_nocap",
        campaign_id="camp_1",
        deliverable_id="deliv_1",
        work_item_id="item_1",
        platform="instagram",
        metrics={
            "impressions": 12000.0,
            "engagements": 900.0,
            "clicks": 400.0,
            "approval_latency_sec": 1800.0,
            "publishing_errors": 0.0,
        },
        raw_payload={},
    )

    with pytest.raises(CrossClientIntelligenceViolation):
        evaluator.evaluate_observation(requesting_client_id="client_other", observation=obs)

    res = evaluator.evaluate_observation(
        requesting_client_id="client_nocap",
        observation=obs,
        target_impressions=10000.0,
        target_engagement_rate=0.05,
        revision_count=1,
    )
    assert res.objective_attainment_score == 1.0
    assert res.overall_score > 0.8
    assert res.reliability_score == 1.0
