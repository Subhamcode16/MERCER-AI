"""
Phase 18 Strategy Experiment Engine.

Manages controlled candidate strategy experiments, comparing candidate metrics
against active baseline performance under strict client isolation and race defense.
"""

from typing import Dict, Any, Optional
import threading
import uuid

from src.studio_intelligence.outcome_models import (
    LearningSignal,
    CandidateStrategy,
    StrategyExperiment,
    ExperimentStatus,
)
from src.studio_intelligence.exceptions import (
    ExperimentRaceError,
    CrossClientIntelligenceViolation,
    LearningBoundaryViolation,
)


class StrategyExperimentEngine:
    """Manages creation, execution, and metric tracking for strategy experiments."""

    def __init__(self):
        self._lock = threading.RLock()
        self._active_experiments: Dict[str, StrategyExperiment] = {}
        self._candidates: Dict[str, CandidateStrategy] = {}

    def create_candidate_strategy(
        self, requesting_client_id: str, learning_signal: LearningSignal, baseline_metrics: Dict[str, float]
    ) -> CandidateStrategy:
        """Constructs a CandidateStrategy from a LearningSignal."""
        if requesting_client_id != learning_signal.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot create candidate strategy for '{learning_signal.client_id}'."
            )

        # Security check: candidate strategy must not touch security policy
        prohibited_keys = {"authorization_required", "security_policy", "roles", "execution_authority"}
        if any(k in prohibited_keys for k in learning_signal.strategy_variables.keys()):
            raise LearningBoundaryViolation("Candidate strategy contains prohibited security policy keys.")

        cand_id = f"cand_{uuid.uuid4().hex[:10]}"
        cand = CandidateStrategy(
            strategy_id=cand_id,
            client_id=learning_signal.client_id,
            version=1,
            name=f"Strategy from Signal {learning_signal.signal_id[:8]}",
            hypothesis=learning_signal.proposed_hypothesis,
            strategy_variables=learning_signal.strategy_variables,
            baseline_metrics=baseline_metrics,
            status=ExperimentStatus.CREATED,
        )

        with self._lock:
            self._candidates[cand_id] = cand
            return cand

    def launch_experiment(
        self, requesting_client_id: str, candidate: CandidateStrategy
    ) -> StrategyExperiment:
        """Launches a controlled strategy experiment with race protection."""
        if requesting_client_id != candidate.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot launch experiment for '{candidate.client_id}'."
            )

        with self._lock:
            # Check for existing running experiment for this client
            for exp in self._active_experiments.values():
                if exp.client_id == candidate.client_id and exp.status == ExperimentStatus.RUNNING:
                    raise ExperimentRaceError(
                        f"Concurrent experiment '{exp.experiment_id}' is already active for client '{candidate.client_id}'."
                    )

            exp_id = f"exp_{uuid.uuid4().hex[:10]}"
            exp = StrategyExperiment(
                experiment_id=exp_id,
                candidate_id=candidate.strategy_id,
                client_id=candidate.client_id,
                baseline_metrics=candidate.baseline_metrics,
                candidate_metrics={},
                status=ExperimentStatus.RUNNING,
                evidence_window_days=7,
            )
            self._active_experiments[exp_id] = exp
            return exp

    def record_experiment_metrics(
        self, requesting_client_id: str, experiment_id: str, candidate_metrics: Dict[str, float]
    ) -> StrategyExperiment:
        """Updates experiment candidate metrics during benchmarking window."""
        with self._lock:
            exp = self._active_experiments.get(experiment_id)
            if not exp:
                raise ExperimentRaceError(f"Experiment '{experiment_id}' not found.")

            if requesting_client_id != exp.client_id:
                raise CrossClientIntelligenceViolation(
                    f"Client '{requesting_client_id}' cannot update experiment owned by '{exp.client_id}'."
                )

            updated_exp = StrategyExperiment(
                experiment_id=exp.experiment_id,
                candidate_id=exp.candidate_id,
                client_id=exp.client_id,
                baseline_metrics=exp.baseline_metrics,
                candidate_metrics=candidate_metrics,
                status=ExperimentStatus.BENCHMARKING,
                evidence_window_days=exp.evidence_window_days,
            )
            self._active_experiments[experiment_id] = updated_exp
            return updated_exp
