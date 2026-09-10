"""
Unit tests for ContinuousStudioOptimizer cycle and rollback behavior.
"""

import pytest
from src.studio_intelligence.outcome_models import LearningSignal, LearningStage
from src.studio_intelligence.continuous_optimizer import ContinuousStudioOptimizer
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


def test_continuous_studio_optimizer_promotes_and_rolls_back():
    optimizer = ContinuousStudioOptimizer()

    signal = LearningSignal(
        signal_id="sig_opt_1",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="WORKFLOW_EFFICIENCY",
        observation_summary="High revision count",
        proposed_hypothesis="Streamline self-critique rounds",
        strategy_variables={"critique_rounds": 2, "research_depth": "EXTENDED"},
    )

    baseline = {"overall_score": 0.70, "publishing_errors": 0.0, "revision_count": 3.0}

    # Case 1: Proven improvement -> PROMOTED
    cand_better = {"overall_score": 0.88, "publishing_errors": 0.0, "revision_count": 1.0}
    res_promoted = optimizer.run_optimization_cycle(
        requesting_client_id="client_nocap",
        learning_signal=signal,
        baseline_metrics=baseline,
        candidate_metrics=cand_better,
    )
    assert res_promoted["status"] == "PROMOTED"
    assert res_promoted["improvement_delta"] == 0.18

    # Case 2: Degraded metrics -> REJECTED_ROLLED_BACK
    cand_worse = {"overall_score": 0.55, "publishing_errors": 1.0, "revision_count": 5.0}
    res_rejected = optimizer.run_optimization_cycle(
        requesting_client_id="client_nocap",
        learning_signal=signal,
        baseline_metrics=baseline,
        candidate_metrics=cand_worse,
    )
    assert res_rejected["status"] == "REJECTED_ROLLED_BACK"
    assert "degraded performance" in res_rejected["rejection_reason"]
