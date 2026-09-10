"""
Phase 18 Studio Learning Engine.

Enforces the explicit closed-loop learning progression contract:
OBSERVED -> ATTRIBUTED -> EVALUATED -> LEARNING_SIGNAL -> HYPOTHESIS -> CANDIDATE_STRATEGY -> BENCHMARKED -> ADOPTED/REJECTED.
"""

from typing import Dict, Any, Optional
import uuid

from src.studio_intelligence.outcome_models import (
    OutcomeObservation,
    LearningStage,
)
from src.studio_intelligence.attribution import CreativeOutcomeAttributionEngine, AttributionRecord
from src.studio_intelligence.evaluation import CreativePerformanceEvaluator, OutcomeEvaluation
from src.studio_intelligence.feedback_fusion import FeedbackFusionEngine, LearningSignal
from src.studio_intelligence.experiment import StrategyExperimentEngine, CandidateStrategy
from src.studio_intelligence.exceptions import (
    LearningBoundaryViolation,
    CrossClientIntelligenceViolation,
)


class StudioLearningEngine:
    """Orchestrates closed-loop learning progression enforcing provenance integrity."""

    def __init__(
        self,
        attribution_engine: Optional[CreativeOutcomeAttributionEngine] = None,
        evaluator: Optional[CreativePerformanceEvaluator] = None,
        feedback_fusion: Optional[FeedbackFusionEngine] = None,
        experiment_engine: Optional[StrategyExperimentEngine] = None,
    ):
        self.attribution_engine = attribution_engine or CreativeOutcomeAttributionEngine()
        self.evaluator = evaluator or CreativePerformanceEvaluator()
        self.feedback_fusion = feedback_fusion or FeedbackFusionEngine()
        self.experiment_engine = experiment_engine or StrategyExperimentEngine()

    def process_observation_to_learning_signal(
        self,
        requesting_client_id: str,
        observation: OutcomeObservation,
        client_feedback_text: Optional[str] = None,
        human_review_score: float = 0.85,
        observed_defect: Optional[str] = None,
        revision_count: int = 1,
    ) -> Dict[str, Any]:
        """Executes explicit progression: OBSERVED -> ATTRIBUTED -> EVALUATED -> LEARNING_SIGNAL."""
        if requesting_client_id != observation.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot process learning for '{observation.client_id}'."
            )

        # Step 1: Attribute
        attribution = self.attribution_engine.attribute_outcome(
            requesting_client_id=requesting_client_id,
            observation=observation,
        )

        # Step 2: Evaluate
        evaluation = self.evaluator.evaluate_observation(
            requesting_client_id=requesting_client_id,
            observation=observation,
            revision_count=revision_count,
        )

        # Step 3: Fuse into Learning Signal
        signal = self.feedback_fusion.fuse_feedback_and_evaluation(
            requesting_client_id=requesting_client_id,
            evaluation=evaluation,
            client_feedback_text=client_feedback_text,
            human_review_score=human_review_score,
            observed_defect=observed_defect,
        )

        return {
            "stage": LearningStage.LEARNING_SIGNAL,
            "attribution": attribution,
            "evaluation": evaluation,
            "signal": signal,
        }
