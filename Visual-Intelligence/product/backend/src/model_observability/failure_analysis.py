"""
Phase 22 Model Observability: Failure Analysis
----------------------------------------------
Classifies and analyzes failure distributions (429, timeouts, malformed output, circuit break, policy rejections).
"""

from typing import Dict, List, Any
from collections import Counter
from src.model_observability.invocation_trace import InvocationTrace

class FailureAnalyzer:
    """Analyzes failure rates and classifies errors across traces."""

    def __init__(self):
        self._error_classes: Counter = Counter()
        self._total_invocations = 0
        self._failed_invocations = 0

    def ingest_trace(self, trace: InvocationTrace) -> None:
        self._total_invocations += 1
        if trace.status != "SUCCESS":
            self._failed_invocations += 1
            error_cls = trace.error_class or trace.status
            self._error_classes[error_cls] += 1

    def get_analysis(self) -> Dict[str, Any]:
        failure_rate = (self._failed_invocations / self._total_invocations) if self._total_invocations > 0 else 0.0
        return {
            "total_invocations": self._total_invocations,
            "failed_invocations": self._failed_invocations,
            "failure_rate": round(failure_rate, 4),
            "failure_breakdown": dict(self._error_classes),
        }
