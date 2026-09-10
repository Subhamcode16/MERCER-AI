"""
Phase 18 Feedback Fusion Engine.

Fuses client feedback, human review ratings, performance evaluations, and revision metrics
into provenance-preserving LearningSignals without mutating security policy.
"""

from typing import Dict, Any, List, Optional
import uuid

from src.studio_intelligence.outcome_models import (
    OutcomeEvaluation,
    LearningSignal,
    LearningStage,
)
from src.studio_intelligence.exceptions import (
    LearningBoundaryViolation,
    CrossClientIntelligenceViolation,
)


class FeedbackFusionEngine:
    """Combines qualitative review feedback with quantitative evaluations into learning signals."""

    def fuse_feedback_and_evaluation(
        self,
        requesting_client_id: str,
        evaluation: OutcomeEvaluation,
        client_feedback_text: Optional[str] = None,
        human_review_score: float = 0.85,
        observed_defect: Optional[str] = None,
    ) -> LearningSignal:
        """Synthesizes structured learning signal from evaluation and human feedback."""
        if requesting_client_id != evaluation.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot fuse feedback for '{evaluation.client_id}'."
            )

        signal_id = f"sig_{uuid.uuid4().hex[:12]}"
        
        # Identify hypothesis and strategy variables to test
        if observed_defect or evaluation.revision_efficiency_score < 0.7:
            defect = observed_defect or "High revision count / approval latency detected."
            hypothesis = "Streamlining early self-critique parameters will reduce revision cycles by 30%."
            strategy_vars = {
                "critique_rounds": 2,
                "research_depth": "EXTENDED",
                "copy_tone": "HIGH_CONVERTING_ENGAGING",
            }
            category = "WORKFLOW_EFFICIENCY"
        else:
            defect = "Normal operational performance."
            hypothesis = "Incremental optimization of copy tone and visual composition."
            strategy_vars = {
                "critique_rounds": 1,
                "research_depth": "STANDARD",
                "copy_tone": "BALANCED_BRAND",
            }
            category = "CREATIVE_OPTIMIZATION"

        # Explicit Security Check: ensure strategy variables contain zero security policy keys
        prohibited_policy_keys = {"authorization_required", "roles", "bypass_security", "permissions"}
        if any(k in prohibited_policy_keys for k in strategy_vars.keys()):
            raise LearningBoundaryViolation("Learning signal attempts to mutate security policy variables.")

        summary = (
            f"Evaluation overall_score={evaluation.overall_score}, "
            f"attainment={evaluation.objective_attainment_score}, "
            f"human_review_score={human_review_score}. Defect: {defect}"
        )

        return LearningSignal(
            signal_id=signal_id,
            evaluation_id=evaluation.evaluation_id,
            client_id=evaluation.client_id,
            stage=LearningStage.LEARNING_SIGNAL,
            category=category,
            observation_summary=summary,
            proposed_hypothesis=hypothesis,
            strategy_variables=strategy_vars,
            confidence_score=0.85,
        )
