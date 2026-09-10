"""
Phase 18 Creative Performance Evaluator.

Evaluates observed external outcomes against explicit objective criteria,
scoring engagement, revision efficiency, approval latency, reliability, and cost efficiency.
"""

from typing import Dict, Any, Optional
import uuid

from src.studio_intelligence.outcome_models import OutcomeObservation, OutcomeEvaluation
from src.studio_intelligence.exceptions import (
    EvaluationError,
    CrossClientIntelligenceViolation,
)


class CreativePerformanceEvaluator:
    """Evaluates creative performance and operational efficiency from raw observations."""

    def evaluate_observation(
        self,
        requesting_client_id: str,
        observation: OutcomeObservation,
        target_impressions: float = 10000.0,
        target_engagement_rate: float = 0.05,
        max_acceptable_approval_latency_sec: float = 86400.0,
        revision_count: int = 1,
    ) -> OutcomeEvaluation:
        """Calculates normalized performance evaluation scores from outcome metrics."""
        if requesting_client_id != observation.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot evaluate observation for '{observation.client_id}'."
            )

        metrics = observation.metrics or {}
        impressions = float(metrics.get("impressions", 0.0))
        engagements = float(metrics.get("engagements", 0.0))
        clicks = float(metrics.get("clicks", 0.0))
        approval_latency = float(metrics.get("approval_latency_sec", 3600.0))
        publishing_errors = float(metrics.get("publishing_errors", 0.0))

        # Objective Attainment (Impressions & Clicks vs Target)
        attainment = min(1.0, impressions / target_impressions) if target_impressions > 0 else 0.5

        # Engagement Efficiency
        actual_rate = (engagements / impressions) if impressions > 0 else 0.0
        engagement_efficiency = min(1.0, actual_rate / target_engagement_rate) if target_engagement_rate > 0 else 0.5

        # Revision Efficiency (1.0 = 0-1 revisions, decreasing as revisions increase)
        revision_efficiency = max(0.1, 1.0 - (revision_count - 1) * 0.25)

        # Reliability Score (1.0 = zero publishing errors)
        reliability = max(0.0, 1.0 - publishing_errors * 0.5)

        # Overall Aggregate Score
        overall = round(
            (attainment * 0.3)
            + (engagement_efficiency * 0.3)
            + (revision_efficiency * 0.2)
            + (reliability * 0.2),
            4,
        )

        eval_id = f"eval_{uuid.uuid4().hex[:12]}"
        return OutcomeEvaluation(
            evaluation_id=eval_id,
            observation_id=observation.observation_id,
            client_id=observation.client_id,
            objective_attainment_score=round(attainment, 4),
            engagement_efficiency_score=round(engagement_efficiency, 4),
            revision_efficiency_score=round(revision_efficiency, 4),
            approval_latency_sec=approval_latency,
            reliability_score=round(reliability, 4),
            overall_score=overall,
            metrics_breakdown={
                "impressions": impressions,
                "engagements": engagements,
                "clicks": clicks,
                "actual_engagement_rate": round(actual_rate, 4),
                "revision_count": float(revision_count),
            },
        )
