"""
Phase 24 Availability and Success Ratio SLO Evaluator.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AvailabilitySLOEvaluator:
    """Tracks successful vs failed operational events against 99.9% availability targets."""

    def __init__(self, target_availability: float = 0.999):
        self.target_availability = target_availability
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0

    def record_event(self, success: bool) -> None:
        self._total_requests += 1
        if success:
            self._successful_requests += 1
        else:
            self._failed_requests += 1

    def get_availability_ratio(self) -> float:
        if self._total_requests == 0:
            return 1.0
        return self._successful_requests / self._total_requests

    def evaluate_slo(self) -> Dict[str, Any]:
        ratio = self.get_availability_ratio()
        passed = ratio >= self.target_availability

        return {
            "passed": passed,
            "actual_availability": round(ratio, 5),
            "target_availability": self.target_availability,
            "total_requests": self._total_requests,
            "failed_requests": self._failed_requests
        }
