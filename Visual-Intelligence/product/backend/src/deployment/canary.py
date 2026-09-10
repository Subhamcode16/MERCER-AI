"""
Phase 23 Production Canary Evaluation Controller.
"""
import logging
from typing import Dict, Any
from src.deployment.deployment_models import CanaryEvaluationMetrics
from src.deployment.exceptions import CanaryDegradedError

logger = logging.getLogger(__name__)

class CanaryController:
    """Evaluates canary traffic health metrics against strict production SLAs."""

    def __init__(self, max_error_rate: float = 0.01, max_p95_latency_ms: float = 2500.0, min_visual_score: float = 0.85):
        self.max_error_rate = max_error_rate
        self.max_p95_latency_ms = max_p95_latency_ms
        self.min_visual_score = min_visual_score

    def evaluate_canary(
        self,
        total_requests: int,
        error_count: int,
        p95_latency_ms: float,
        visual_regression_score: float
    ) -> CanaryEvaluationMetrics:
        """Evaluates canary telemetry and triggers failure if any threshold is breached."""
        error_rate = error_count / total_requests if total_requests > 0 else 0.0
        sla_breached = False
        reasons = []

        if error_rate > self.max_error_rate:
            sla_breached = True
            reasons.append(f"Error rate {error_rate:.4f} exceeded max {self.max_error_rate}")

        if p95_latency_ms > self.max_p95_latency_ms:
            sla_breached = True
            reasons.append(f"p95 latency {p95_latency_ms}ms exceeded max {self.max_p95_latency_ms}ms")

        if visual_regression_score < self.min_visual_score:
            sla_breached = True
            reasons.append(f"Visual score {visual_regression_score} below minimum {self.min_visual_score}")

        metrics = CanaryEvaluationMetrics(
            total_requests=total_requests,
            error_count=error_count,
            error_rate=round(error_rate, 4),
            p95_latency_ms=p95_latency_ms,
            visual_regression_score=visual_regression_score,
            sla_breached=sla_breached,
            details={"breaches": reasons} if sla_breached else {}
        )

        if sla_breached:
            logger.error(f"Canary SLA breached! Reasons: {reasons}")
            raise CanaryDegradedError(f"Canary evaluation failed: {', '.join(reasons)}")

        logger.info(f"Canary evaluation passed successfully (Requests: {total_requests}, Error Rate: {error_rate:.4f})")
        return metrics
