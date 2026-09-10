"""
Phase 9 — Persistent Improvement Engine & Rollback Controls

Governs evaluation-first strategy updates, benchmark score comparisons,
harmful candidate rejection, and deterministic rollback to previous approved versions.
"""

import json
from typing import Dict, Optional, Tuple

from src.agentic_work.adaptive_strategy import (
    AdaptiveStrategy,
    AdaptiveStrategyStore,
    StrategyStatus,
)
from src.agentic_work.benchmark_suite import BenchmarkSuiteResult, BenchmarkSuiteRunner


class DegradationRejectedError(ValueError):
    """Raised when a candidate strategy scores lower than the currently active strategy."""

    pass


class PersistentImprovementEngine:
    """Manages strategy candidate lifecycle, evaluation, activation, and rollback."""

    def __init__(
        self,
        strategy_store: Optional[AdaptiveStrategyStore] = None,
        benchmark_runner: Optional[BenchmarkSuiteRunner] = None,
    ):
        self.strategy_store = strategy_store or AdaptiveStrategyStore()
        self.benchmark_runner = benchmark_runner or BenchmarkSuiteRunner()

    def propose_candidate(
        self,
        candidate_version_id: str,
        parent_version_id: str,
        parameters: Dict,
        rationale: str,
    ) -> AdaptiveStrategy:
        """Creates and validates a new CANDIDATE strategy."""
        parent = self.strategy_store.get_strategy(parent_version_id)

        candidate = AdaptiveStrategy(
            strategy_version_id=candidate_version_id,
            parent_version_id=parent.strategy_version_id,
            parameters=parameters,
            status=StrategyStatus.CANDIDATE,
            rationale=rationale,
            benchmark_score=0.0,
        )

        # Validate security allowlist immediately
        candidate.validate_allowlist()

        self.strategy_store.save_strategy(candidate)
        return candidate

    def evaluate_candidate(
        self, candidate_version_id: str
    ) -> Tuple[AdaptiveStrategy, BenchmarkSuiteResult]:
        """Evaluates a candidate strategy against the 5-category benchmark suite."""
        candidate = self.strategy_store.get_strategy(candidate_version_id)
        active = self.strategy_store.get_active_strategy()

        bench_result = self.benchmark_runner.evaluate_strategy(candidate)

        # Reject if score degrades compared to currently active strategy
        if bench_result.overall_score < active.benchmark_score:
            rejected_candidate = AdaptiveStrategy(
                strategy_version_id=candidate.strategy_version_id,
                parent_version_id=candidate.parent_version_id,
                parameters=candidate.parameters,
                status=StrategyStatus.REJECTED,
                rationale=f"Rejected: Benchmark score {bench_result.overall_score} lower than active {active.benchmark_score}",
                benchmark_score=bench_result.overall_score,
            )
            self.strategy_store.save_strategy(rejected_candidate)
            raise DegradationRejectedError(
                f"Candidate '{candidate_version_id}' score ({bench_result.overall_score}) degraded baseline ({active.benchmark_score})."
            )

        # Mark as APPROVED
        approved_candidate = AdaptiveStrategy(
            strategy_version_id=candidate.strategy_version_id,
            parent_version_id=candidate.parent_version_id,
            parameters=candidate.parameters,
            status=StrategyStatus.APPROVED,
            rationale=f"Approved: Benchmark score {bench_result.overall_score} >= baseline {active.benchmark_score}",
            benchmark_score=bench_result.overall_score,
        )
        self.strategy_store.save_strategy(approved_candidate)

        return approved_candidate, bench_result

    def activate_strategy(self, strategy_version_id: str) -> AdaptiveStrategy:
        """Activates an approved strategy and demotes previous active strategy."""
        target = self.strategy_store.get_strategy(strategy_version_id)
        if target.status not in [StrategyStatus.APPROVED, StrategyStatus.CANDIDATE]:
            raise ValueError(
                f"Cannot activate strategy '{strategy_version_id}' with status {target.status}"
            )

        # Demote current active strategy
        curr_active = self.strategy_store.get_active_strategy()
        if curr_active.strategy_version_id != strategy_version_id:
            demoted = AdaptiveStrategy(
                strategy_version_id=curr_active.strategy_version_id,
                parent_version_id=curr_active.parent_version_id,
                parameters=curr_active.parameters,
                status=StrategyStatus.APPROVED,
                rationale=curr_active.rationale,
                benchmark_score=curr_active.benchmark_score,
            )
            self.strategy_store.save_strategy(demoted)

        # Activate target
        activated = AdaptiveStrategy(
            strategy_version_id=target.strategy_version_id,
            parent_version_id=target.parent_version_id,
            parameters=target.parameters,
            status=StrategyStatus.ACTIVE,
            rationale=target.rationale,
            benchmark_score=target.benchmark_score,
        )
        self.strategy_store.save_strategy(activated)
        return activated

    def rollback_active_strategy(self) -> AdaptiveStrategy:
        """Rolls back currently active strategy to its parent version."""
        curr_active = self.strategy_store.get_active_strategy()
        if not curr_active.parent_version_id:
            raise ValueError("Current active strategy has no parent version to roll back to.")

        # Mark current active as ROLLED_BACK
        rolled_back = AdaptiveStrategy(
            strategy_version_id=curr_active.strategy_version_id,
            parent_version_id=curr_active.parent_version_id,
            parameters=curr_active.parameters,
            status=StrategyStatus.ROLLED_BACK,
            rationale=f"Rolled back manually or due to regression.",
            benchmark_score=curr_active.benchmark_score,
        )
        self.strategy_store.save_strategy(rolled_back)

        # Activate parent
        parent = self.strategy_store.get_strategy(curr_active.parent_version_id)
        activated_parent = AdaptiveStrategy(
            strategy_version_id=parent.strategy_version_id,
            parent_version_id=parent.parent_version_id,
            parameters=parent.parameters,
            status=StrategyStatus.ACTIVE,
            rationale=f"Re-activated as rollback target from {curr_active.strategy_version_id}",
            benchmark_score=parent.benchmark_score,
        )
        self.strategy_store.save_strategy(activated_parent)
        return activated_parent
