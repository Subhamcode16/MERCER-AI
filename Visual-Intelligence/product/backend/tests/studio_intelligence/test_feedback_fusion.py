"""
Unit tests for FeedbackFusionEngine.
"""

import pytest
from src.studio_intelligence.outcome_models import OutcomeEvaluation
from src.studio_intelligence.feedback_fusion import FeedbackFusionEngine
from src.studio_intelligence.exceptions import (
    CrossClientIntelligenceViolation,
    LearningBoundaryViolation,
)


def test_feedback_fusion_engine():
    fusion = FeedbackFusionEngine()
    evaluation = OutcomeEvaluation(
        evaluation_id="eval_1",
        observation_id="obs_1",
        client_id="client_nocap",
        objective_attainment_score=0.9,
        engagement_efficiency_score=0.85,
        revision_efficiency_score=0.60,
        approval_latency_sec=7200.0,
        reliability_score=1.0,
        overall_score=0.82,
    )

    with pytest.raises(CrossClientIntelligenceViolation):
        fusion.fuse_feedback_and_evaluation(
            requesting_client_id="client_other", evaluation=evaluation
        )

    signal = fusion.fuse_feedback_and_evaluation(
        requesting_client_id="client_nocap",
        evaluation=evaluation,
        client_feedback_text="Visuals were great, but copy needed 3 revisions.",
        human_review_score=0.90,
        observed_defect="Excessive revision cycles causing approval latency.",
    )
    assert signal.signal_id.startswith("sig_")
    assert signal.category == "WORKFLOW_EFFICIENCY"
    assert "critique_rounds" in signal.strategy_variables
