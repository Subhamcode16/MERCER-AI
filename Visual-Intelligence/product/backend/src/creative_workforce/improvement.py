"""
Phase 14 Governed Self-Improvement Engine
-----------------------------------------
Executes evaluation-first controlled experimentation for workforce strategy optimization (INV-14-W007).
Compares candidate strategies against baseline benchmarks; deterministically rejects degraded candidates
and enforces versioned adoption with rollback capability.
Prohibits autonomous security policy mutation or authority escalation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import uuid

from src.creative_workforce.exceptions import StrategyDegradationError, UntrustedObservationInjectionError

@dataclass(frozen=True)
class WorkflowStrategy:
    """Versioned workflow strategy configuration."""
    strategy_id: str
    version: str
    parameters: Dict[str, Any]
    quality_baseline: float = 0.80
    created_at: float = field(default_factory=time.time)

@dataclass(frozen=True)
class ExperimentResult:
    """Result of a controlled workflow strategy benchmark experiment."""
    experiment_id: str
    baseline_score: float
    candidate_score: float
    is_adopted: bool
    rejection_reason: Optional[str] = None

class GovernedImprovementEngine:
    """Engine executing controlled experiments and versioned strategy rollbacks."""

    def __init__(self):
        self._strategies: Dict[str, WorkflowStrategy] = {
            "1.0.0": WorkflowStrategy("strat-v1", "1.0.0", {"max_revisions": 3, "critique_threshold": 0.70}, quality_baseline=0.80)
        }
        self._active_version: str = "1.0.0"

    def propose_candidate_strategy(
        self,
        new_version: str,
        parameters: Dict[str, Any],
    ) -> WorkflowStrategy:
        """Proposes a new candidate strategy version while rejecting security policy mutation attempts."""
        for k in parameters:
            if any(sk in k.lower() for sk in ["security", "auth", "gate", "capability", "permission"]):
                raise UntrustedObservationInjectionError(
                    f"Candidate strategy parameter '{k}' attempts forbidden security policy mutation."
                )

        strat_id = f"strat-{uuid.uuid4().hex[:8]}"
        strat = WorkflowStrategy(strategy_id=strat_id, version=new_version, parameters=parameters)
        self._strategies[new_version] = strat
        return strat

    def benchmark_candidate(
        self,
        candidate_version: str,
        simulated_candidate_quality: float,
    ) -> ExperimentResult:
        """Evaluates a candidate strategy against the baseline. Rejects if quality degrades."""
        exp_id = f"exp-{uuid.uuid4().hex[:8]}"
        current_strat = self._strategies[self._active_version]
        baseline = current_strat.quality_baseline

        if simulated_candidate_quality < baseline:
            rejection_reason = f"Candidate score {simulated_candidate_quality:.2f} degraded below baseline {baseline:.2f}."
            return ExperimentResult(
                experiment_id=exp_id,
                baseline_score=baseline,
                candidate_score=simulated_candidate_quality,
                is_adopted=False,
                rejection_reason=rejection_reason,
            )

        # Adopt candidate strategy
        self._active_version = candidate_version
        return ExperimentResult(
            experiment_id=exp_id,
            baseline_score=baseline,
            candidate_score=simulated_candidate_quality,
            is_adopted=True,
        )

    def rollback_to_version(self, version: str) -> None:
        """Rolls back active strategy to a previous version."""
        if version in self._strategies:
            self._active_version = version

    def get_active_strategy(self) -> WorkflowStrategy:
        """Returns the currently active workflow strategy."""
        return self._strategies[self._active_version]
