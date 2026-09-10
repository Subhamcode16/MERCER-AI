"""
Phase 18 Strategy Promotion Controller.

Evaluates candidate strategy metrics against baseline, promoting proven candidates
and throwing OptimizationRejectedError on degraded performance.
"""

from typing import Dict, Any
import uuid

from src.studio_intelligence.outcome_models import (
    CandidateStrategy,
    StrategyExperiment,
    PromotionRecord,
    ExperimentStatus,
)
from src.studio_intelligence.exceptions import (
    OptimizationRejectedError,
    CrossClientIntelligenceViolation,
    LearningBoundaryViolation,
)


class StrategyPromotionController:
    """Controls candidate strategy promotion and rejection based on empirical evidence."""

    def evaluate_and_promote(
        self,
        requesting_client_id: str,
        experiment: StrategyExperiment,
        candidate: CandidateStrategy,
        approved_by: str = "auto_evaluator",
    ) -> PromotionRecord:
        """Promotes candidate if benchmark criteria pass; rejects with rollback on degradation."""
        if requesting_client_id != experiment.client_id or requesting_client_id != candidate.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot evaluate promotion for target client context."
            )

        baseline = experiment.baseline_metrics
        cand_metrics = experiment.candidate_metrics

        base_score = float(baseline.get("overall_score", 0.70))
        cand_score = float(cand_metrics.get("overall_score", 0.0))

        base_errors = float(baseline.get("publishing_errors", 0.0))
        cand_errors = float(cand_metrics.get("publishing_errors", 0.0))

        base_revisions = float(baseline.get("revision_count", 2.0))
        cand_revisions = float(cand_metrics.get("revision_count", 2.0))

        # Check 1: Security Policy Mutation Prohibition
        prohibited_keys = {"authorization_required", "security_policy", "roles", "execution_authority"}
        if any(k in prohibited_keys for k in candidate.strategy_variables.keys()):
            raise LearningBoundaryViolation("Promotion rejected: Strategy mutates security policy.")

        # Check 2: Performance & Reliability Benchmarks
        is_degraded = (
            cand_score < base_score
            or cand_errors > base_errors
            or cand_revisions > base_revisions
        )

        if is_degraded:
            raise OptimizationRejectedError(
                f"Candidate strategy '{candidate.strategy_id}' demonstrated degraded performance: "
                f"cand_score={cand_score} vs base_score={base_score}, "
                f"cand_revisions={cand_revisions} vs base_revisions={base_revisions}. Candidate REJECTED."
            )

        # Promotion Successful
        prom_id = f"prom_{uuid.uuid4().hex[:10]}"
        return PromotionRecord(
            promotion_id=prom_id,
            candidate_id=candidate.strategy_id,
            client_id=candidate.client_id,
            approved_by=approved_by,
            benchmark_summary={
                "base_score": base_score,
                "cand_score": cand_score,
                "improvement_delta": round(cand_score - base_score, 4),
                "base_revisions": base_revisions,
                "cand_revisions": cand_revisions,
            },
            policy_compliance_checked=True,
        )
