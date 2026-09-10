"""
Unit tests for StrategyPromotionController evaluation and rollback triggers.
"""

import pytest
from src.studio_intelligence.outcome_models import CandidateStrategy, StrategyExperiment, ExperimentStatus
from src.studio_intelligence.promotion import StrategyPromotionController
from src.studio_intelligence.exceptions import OptimizationRejectedError, CrossClientIntelligenceViolation


def test_strategy_promotion_success_and_degradation_rejection():
    controller = StrategyPromotionController()

    candidate = CandidateStrategy(
        strategy_id="cand_1",
        client_id="client_nocap",
        version=1,
        name="Test Candidate",
        hypothesis="Hypothesis test",
        strategy_variables={"research_depth": "EXTENDED"},
        baseline_metrics={"overall_score": 0.70, "revision_count": 2.0},
    )

    # Scenario A: Proven Improvement -> Promoted
    exp_improved = StrategyExperiment(
        experiment_id="exp_pass",
        candidate_id="cand_1",
        client_id="client_nocap",
        baseline_metrics={"overall_score": 0.70, "revision_count": 2.0},
        candidate_metrics={"overall_score": 0.85, "revision_count": 1.0},
        status=ExperimentStatus.BENCHMARKING,
    )
    promotion = controller.evaluate_and_promote(
        requesting_client_id="client_nocap",
        experiment=exp_improved,
        candidate=candidate,
    )
    assert promotion.promotion_id.startswith("prom_")
    assert promotion.benchmark_summary["improvement_delta"] == 0.15

    # Scenario B: Degraded Performance -> OptimizationRejectedError
    exp_degraded = StrategyExperiment(
        experiment_id="exp_fail",
        candidate_id="cand_1",
        client_id="client_nocap",
        baseline_metrics={"overall_score": 0.70, "revision_count": 2.0},
        candidate_metrics={"overall_score": 0.60, "revision_count": 4.0},
        status=ExperimentStatus.BENCHMARKING,
    )
    with pytest.raises(OptimizationRejectedError, match="degraded performance"):
        controller.evaluate_and_promote(
            requesting_client_id="client_nocap",
            experiment=exp_degraded,
            candidate=candidate,
        )
