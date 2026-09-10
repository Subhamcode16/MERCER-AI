"""
Phase 18 Studio Intelligence Orchestrator.

Primary facade integrating closed-loop intelligence, outcome observations,
creative attributions, performance evaluations, learning signals, controlled strategy experiments,
strategy promotions/rejections, provider operations, and hash-linked audit logging.
"""

from typing import Dict, Any, List, Optional

from src.studio_intelligence.outcome_models import (
    OutcomeObservation,
    OutcomeEvaluation,
    LearningSignal,
    CandidateStrategy,
    StrategyExperiment,
    PromotionRecord,
    OutcomeProvenance,
)
from src.studio_intelligence.outcome_store import OutcomeStore
from src.studio_intelligence.attribution import CreativeOutcomeAttributionEngine, AttributionRecord
from src.studio_intelligence.evaluation import CreativePerformanceEvaluator
from src.studio_intelligence.feedback_fusion import FeedbackFusionEngine
from src.studio_intelligence.experiment import StrategyExperimentEngine
from src.studio_intelligence.promotion import StrategyPromotionController
from src.studio_intelligence.intelligence_memory import StudioIntelligenceMemory
from src.studio_intelligence.studio_learning import StudioLearningEngine
from src.studio_intelligence.continuous_optimizer import ContinuousStudioOptimizer
from src.studio_intelligence.provider_runtime import StudioProviderRuntime
from src.studio_intelligence.intelligence_dashboard import StudioIntelligenceDashboard
from src.studio_intelligence.intelligence_ledger import StudioIntelligenceLedger
from src.studio_intelligence.exceptions import (
    CrossClientIntelligenceViolation,
    LearningBoundaryViolation,
    OptimizationRejectedError,
)
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability


class StudioIntelligenceOrchestrator:
    """Primary Phase 18 facade orchestrating real-world provider operations and studio intelligence."""

    def __init__(
        self,
        ledger_dir: str = "data/phase18_intelligence_ledger",
        provider_runtime: Optional[StudioProviderRuntime] = None,
    ):
        self.ledger = StudioIntelligenceLedger(ledger_dir=ledger_dir)
        self.outcome_store = OutcomeStore()
        self.attribution_engine = CreativeOutcomeAttributionEngine()
        self.evaluator = CreativePerformanceEvaluator()
        self.feedback_fusion = FeedbackFusionEngine()
        self.experiment_engine = StrategyExperimentEngine()
        self.promotion_controller = StrategyPromotionController()
        self.memory = StudioIntelligenceMemory()
        self.learning_engine = StudioLearningEngine(
            attribution_engine=self.attribution_engine,
            evaluator=self.evaluator,
            feedback_fusion=self.feedback_fusion,
            experiment_engine=self.experiment_engine,
        )
        self.optimizer = ContinuousStudioOptimizer(
            experiment_engine=self.experiment_engine,
            promotion_controller=self.promotion_controller,
            memory=self.memory,
        )
        self.provider_runtime = provider_runtime or StudioProviderRuntime()
        self.dashboard = StudioIntelligenceDashboard(
            outcome_store=self.outcome_store,
            memory=self.memory,
        )

    def ingest_outcome(
        self, requesting_client_id: str, observation: OutcomeObservation
    ) -> OutcomeObservation:
        """Stores external outcome observation with anti-replay defense and client isolation."""
        stored_obs = self.outcome_store.store_observation(
            requesting_client_id=requesting_client_id, observation=observation
        )

        self.ledger.append_event(
            event_type="OUTCOME_RECEIVED",
            client_id=observation.client_id,
            payload={
                "observation_id": observation.observation_id,
                "deliverable_id": observation.deliverable_id,
                "provenance": observation.provenance.value,
                "metrics": observation.metrics,
            },
        )
        return stored_obs

    def process_closed_loop_learning(
        self,
        requesting_client_id: str,
        observation: OutcomeObservation,
        client_feedback_text: Optional[str] = None,
        human_review_score: float = 0.85,
        observed_defect: Optional[str] = None,
        revision_count: int = 1,
    ) -> Dict[str, Any]:
        """Runs the progression: OBSERVED -> ATTRIBUTED -> EVALUATED -> LEARNING_SIGNAL."""
        result = self.learning_engine.process_observation_to_learning_signal(
            requesting_client_id=requesting_client_id,
            observation=observation,
            client_feedback_text=client_feedback_text,
            human_review_score=human_review_score,
            observed_defect=observed_defect,
            revision_count=revision_count,
        )

        signal: LearningSignal = result["signal"]
        evaluation: OutcomeEvaluation = result["evaluation"]
        attribution: AttributionRecord = result["attribution"]

        self.ledger.append_event(
            event_type="OUTCOME_ATTRIBUTED",
            client_id=observation.client_id,
            payload={
                "attribution_id": attribution.attribution_id,
                "observation_id": observation.observation_id,
            },
        )

        self.ledger.append_event(
            event_type="OUTCOME_EVALUATED",
            client_id=observation.client_id,
            payload={
                "evaluation_id": evaluation.evaluation_id,
                "overall_score": evaluation.overall_score,
            },
        )

        self.ledger.append_event(
            event_type="LEARNING_SIGNAL_CREATED",
            client_id=observation.client_id,
            payload={
                "signal_id": signal.signal_id,
                "category": signal.category,
                "proposed_hypothesis": signal.proposed_hypothesis,
            },
        )

        return result

    def optimize_strategy(
        self,
        requesting_client_id: str,
        learning_signal: LearningSignal,
        baseline_metrics: Dict[str, float],
        candidate_metrics: Dict[str, float],
    ) -> Dict[str, Any]:
        """Runs continuous optimization: launches experiment, benchmarks, and promotes or rolls back."""
        self.ledger.append_event(
            event_type="STRATEGY_EXPERIMENT_STARTED",
            client_id=learning_signal.client_id,
            payload={
                "signal_id": learning_signal.signal_id,
                "baseline_metrics": baseline_metrics,
            },
        )

        result = self.optimizer.run_optimization_cycle(
            requesting_client_id=requesting_client_id,
            learning_signal=learning_signal,
            baseline_metrics=baseline_metrics,
            candidate_metrics=candidate_metrics,
        )

        status = result.get("status")
        if status == "PROMOTED":
            self.ledger.append_event(
                event_type="STRATEGY_PROMOTED",
                client_id=learning_signal.client_id,
                payload={
                    "candidate_id": result.get("candidate_id"),
                    "promotion_id": result.get("promotion_id"),
                    "improvement_delta": result.get("improvement_delta"),
                },
            )
        else:
            self.ledger.append_event(
                event_type="STRATEGY_REJECTED",
                client_id=learning_signal.client_id,
                payload={
                    "candidate_id": result.get("candidate_id"),
                    "rejection_reason": result.get("rejection_reason"),
                },
            )
            self.ledger.append_event(
                event_type="STRATEGY_ROLLED_BACK",
                client_id=learning_signal.client_id,
                payload={"candidate_id": result.get("candidate_id")},
            )

        return result

    def execute_provider_action(
        self,
        client_id: str,
        action_name: str,
        capability: ExecutionCapability,
        auth_record: AuthorizationRecord,
        payload: Dict[str, Any],
        idempotency_key: str,
    ) -> Any:
        """Executes external provider operation through Phase 13 subordinate controls."""
        try:
            res = self.provider_runtime.execute_provider_action(
                client_id=client_id,
                action_name=action_name,
                capability=capability,
                auth_record=auth_record,
                payload=payload,
                idempotency_key=idempotency_key,
            )
            self.ledger.append_event(
                event_type="PROVIDER_ACTION_EXECUTED",
                client_id=client_id,
                payload={"action_name": action_name, "idempotency_key": idempotency_key},
            )
            return res
        except Exception as exc:
            self.ledger.append_event(
                event_type="PROVIDER_FAILURE",
                client_id=client_id,
                payload={"action_name": action_name, "error": str(exc)},
            )
            raise

    def get_dashboard_summary(
        self, requesting_client_id: str, target_client_id: str
    ) -> Dict[str, Any]:
        """Retrieves safe client intelligence dashboard projections."""
        return self.dashboard.get_client_intelligence_summary(
            requesting_client_id=requesting_client_id, target_client_id=target_client_id
        )

    def verify_ledger(self) -> bool:
        """Verifies audit ledger hash integrity."""
        return self.ledger.verify_chain_integrity()
