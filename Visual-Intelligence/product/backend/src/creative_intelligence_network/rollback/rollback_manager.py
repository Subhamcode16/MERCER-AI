"""
Strategic Rollback & Invalidation Manager for Phase 29.
"""
from typing import Optional
from ..recommendations.recommendation_models import StrategicRecommendation, RecommendationStatus
from ..signals.signal_types import StrategicSignal, SignalLifecycle
from ..hypotheses.hypothesis_types import StrategicHypothesis, HypothesisStatus
from ..observability.telemetry import StrategicTelemetryEngine


class StrategicRollbackManager:
    def __init__(self, telemetry: Optional[StrategicTelemetryEngine] = None):
        self.telemetry = telemetry or StrategicTelemetryEngine()

    def withdraw_recommendation(
        self,
        recommendation: StrategicRecommendation,
        operator_id: str,
        reason: str,
    ) -> StrategicRecommendation:
        prev = recommendation.status.value
        recommendation.status = RecommendationStatus.WITHDRAWN
        recommendation.is_active = False

        self.telemetry.record_event(
            tenant_id=recommendation.tenant_id,
            actor=operator_id,
            actor_type="OPERATOR",
            object_id=recommendation.recommendation_id,
            object_type="RECOMMENDATION",
            previous_state=prev,
            new_state="WITHDRAWN",
            reason=reason,
        )
        return recommendation

    def invalidate_signal(
        self,
        signal: StrategicSignal,
        operator_id: str,
        reason: str,
    ) -> StrategicSignal:
        prev = signal.lifecycle_state.value
        signal.lifecycle_state = SignalLifecycle.EXPIRED
        signal.is_active = False

        self.telemetry.record_event(
            tenant_id=signal.tenant_id,
            actor=operator_id,
            actor_type="OPERATOR",
            object_id=signal.signal_id,
            object_type="SIGNAL",
            previous_state=prev,
            new_state="EXPIRED",
            reason=reason,
        )
        return signal

    def reject_hypothesis(
        self,
        hypothesis: StrategicHypothesis,
        operator_id: str,
        reason: str,
    ) -> StrategicHypothesis:
        prev = hypothesis.status.value
        hypothesis.status = HypothesisStatus.REJECTED
        hypothesis.is_active = False

        self.telemetry.record_event(
            tenant_id=hypothesis.tenant_id,
            actor=operator_id,
            actor_type="OPERATOR",
            object_id=hypothesis.hypothesis_id,
            object_type="HYPOTHESIS",
            previous_state=prev,
            new_state="REJECTED",
            reason=reason,
        )
        return hypothesis
