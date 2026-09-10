"""
Phase 18 Continuous Studio Optimizer.

Orchestrates candidate selection, sandbox benchmarking, promotion,
rejection, and deterministic strategy rollback under strict security invariance.
"""

from typing import Dict, Any, Optional
import uuid

from src.studio_intelligence.outcome_models import (
    LearningSignal,
    CandidateStrategy,
    StrategyExperiment,
    PromotionRecord,
    IntelligenceKnowledgeItem,
    ExperimentStatus,
)
from src.studio_intelligence.experiment import StrategyExperimentEngine
from src.studio_intelligence.promotion import StrategyPromotionController
from src.studio_intelligence.intelligence_memory import StudioIntelligenceMemory
from src.studio_intelligence.exceptions import (
    OptimizationRejectedError,
    CrossClientIntelligenceViolation,
)


class ContinuousStudioOptimizer:
    """Coordinates continuous strategy candidate evaluation, benchmarking, and adoption."""

    def __init__(
        self,
        experiment_engine: Optional[StrategyExperimentEngine] = None,
        promotion_controller: Optional[StrategyPromotionController] = None,
        memory: Optional[StudioIntelligenceMemory] = None,
    ):
        self.experiment_engine = experiment_engine or StrategyExperimentEngine()
        self.promotion_controller = promotion_controller or StrategyPromotionController()
        self.memory = memory or StudioIntelligenceMemory()
        self.active_strategies: Dict[str, Dict[str, Any]] = {}

    def run_optimization_cycle(
        self,
        requesting_client_id: str,
        learning_signal: LearningSignal,
        baseline_metrics: Dict[str, float],
        candidate_metrics: Dict[str, float],
    ) -> Dict[str, Any]:
        """Executes a full optimization cycle: candidate creation, experiment, promotion or rejection."""
        if requesting_client_id != learning_signal.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot run optimization cycle for '{learning_signal.client_id}'."
            )

        client_id = learning_signal.client_id

        # Step 1: Propose candidate strategy
        candidate = self.experiment_engine.create_candidate_strategy(
            requesting_client_id=client_id,
            learning_signal=learning_signal,
            baseline_metrics=baseline_metrics,
        )

        # Step 2: Launch experiment
        experiment = self.experiment_engine.launch_experiment(
            requesting_client_id=client_id, candidate=candidate
        )

        # Step 3: Record candidate benchmarking metrics
        experiment = self.experiment_engine.record_experiment_metrics(
            requesting_client_id=client_id,
            experiment_id=experiment.experiment_id,
            candidate_metrics=candidate_metrics,
        )

        # Step 4: Attempt promotion
        try:
            promotion = self.promotion_controller.evaluate_and_promote(
                requesting_client_id=client_id,
                experiment=experiment,
                candidate=candidate,
            )

            # Store adopted strategy in client memory
            item_id = f"item_{uuid.uuid4().hex[:10]}"
            kitem = IntelligenceKnowledgeItem(
                item_id=item_id,
                client_id=client_id,
                category=learning_signal.category,
                title=f"Adopted Strategy: {candidate.name}",
                content=f"Strategy variables: {candidate.strategy_variables}",
                confidence_score=0.92,
                source_signal_ids=[learning_signal.signal_id],
            )
            self.memory.store_knowledge_item(requesting_client_id=client_id, item=kitem)

            self.active_strategies[client_id] = candidate.strategy_variables

            return {
                "status": "PROMOTED",
                "candidate_id": candidate.strategy_id,
                "promotion_id": promotion.promotion_id,
                "active_strategy": candidate.strategy_variables,
                "improvement_delta": promotion.benchmark_summary.get("improvement_delta", 0.0),
            }

        except OptimizationRejectedError as exc:
            # Deterministic Rollback: baseline remains active
            return {
                "status": "REJECTED_ROLLED_BACK",
                "candidate_id": candidate.strategy_id,
                "rejection_reason": str(exc),
                "active_strategy": self.active_strategies.get(client_id, {}),
            }
