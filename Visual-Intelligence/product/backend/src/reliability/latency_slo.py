"""
Phase 24 Latency Distribution and Percentile SLO Evaluator.
"""
import math
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class LatencySLOEvaluator:
    """Computes p50, p90, p95, p99 percentiles and enforces latency SLOs."""

    def __init__(self, target_p95_ms: float = 2500.0, target_p99_ms: float = 5000.0):
        self.target_p95_ms = target_p95_ms
        self.target_p99_ms = target_p99_ms
        self._latencies: List[float] = []

    def record_latency(self, latency_ms: float) -> None:
        self._latencies.append(latency_ms)

    def calculate_percentiles(self) -> Dict[str, float]:
        if not self._latencies:
            return {"p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0, "count": 0}

        sorted_lat = sorted(self._latencies)
        n = len(sorted_lat)

        def get_percentile(p: float) -> float:
            idx = int(math.ceil(p * n)) - 1
            return sorted_lat[max(0, min(idx, n - 1))]

        return {
            "p50": round(get_percentile(0.50), 2),
            "p90": round(get_percentile(0.90), 2),
            "p95": round(get_percentile(0.95), 2),
            "p99": round(get_percentile(0.99), 2),
            "count": n
        }

    def evaluate_slo(self) -> Dict[str, Any]:
        p = self.calculate_percentiles()
        p95_passed = p["p95"] <= self.target_p95_ms
        p99_passed = p["p99"] <= self.target_p99_ms

        return {
            "passed": p95_passed and p99_passed,
            "p95_actual_ms": p["p95"],
            "p95_target_ms": self.target_p95_ms,
            "p99_actual_ms": p["p99"],
            "p99_target_ms": self.target_p99_ms,
            "percentiles": p
        }
