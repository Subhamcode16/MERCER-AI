"""
Unit tests for StrategyExperimentEngine.
"""

import pytest
from src.studio_intelligence.outcome_models import LearningSignal, LearningStage
from src.studio_intelligence.experiment import StrategyExperimentEngine
from src.studio_intelligence.exceptions import (
    ExperimentRaceError,
    CrossClientIntelligenceViolation,
)


def test_strategy_experiment_engine_lifecycle_and_race_prevention():
    engine = StrategyExperimentEngine()
    signal = LearningSignal(
        signal_id="sig_exp_1",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="CREATIVE_OPTIMIZATION",
        observation_summary="Good performance",
        proposed_hypothesis="Test new tone",
        strategy_variables={"copy_tone": "BOLD_MODERN"},
    )

    baseline = {"overall_score": 0.75, "publishing_errors": 0.0}

    with pytest.raises(CrossClientIntelligenceViolation):
        engine.create_candidate_strategy(
            requesting_client_id="client_other",
            learning_signal=signal,
            baseline_metrics=baseline,
        )

    candidate = engine.create_candidate_strategy(
        requesting_client_id="client_nocap",
        learning_signal=signal,
        baseline_metrics=baseline,
    )
    assert candidate.strategy_id.startswith("cand_")

    exp = engine.launch_experiment(requesting_client_id="client_nocap", candidate=candidate)
    assert exp.experiment_id.startswith("exp_")

    # Race condition check: second concurrent launch for same client must fail
    with pytest.raises(ExperimentRaceError):
        engine.launch_experiment(requesting_client_id="client_nocap", candidate=candidate)

    updated_exp = engine.record_experiment_metrics(
        requesting_client_id="client_nocap",
        experiment_id=exp.experiment_id,
        candidate_metrics={"overall_score": 0.88, "publishing_errors": 0.0},
    )
    assert updated_exp.candidate_metrics["overall_score"] == 0.88
