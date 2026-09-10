"""
Phase 22 Model Observability: Latency Telemetry Calculator
----------------------------------------------------------
Calculates latency distribution percentiles (avg, p50, p90, p95, p99) across model and MCP invocations.
"""

from typing import List, Dict, Any
import numpy as np

class LatencyTracker:
    """Aggregates latency observations and computes distribution metrics."""

    def __init__(self):
        self._latencies_ms: List[float] = []

    def record_latency(self, latency_ms: float) -> None:
        if latency_ms >= 0:
            self._latencies_ms.append(latency_ms)

    def get_metrics(self) -> Dict[str, Any]:
        if not self._latencies_ms:
            return {
                "count": 0,
                "avg_ms": 0.0,
                "p50_ms": 0.0,
                "p90_ms": 0.0,
                "p95_ms": 0.0,
                "p99_ms": 0.0,
                "min_ms": 0.0,
                "max_ms": 0.0,
            }

        sorted_vals = sorted(self._latencies_ms)
        arr = np.array(sorted_vals)
        return {
            "count": len(sorted_vals),
            "avg_ms": round(float(np.mean(arr)), 2),
            "p50_ms": round(float(np.percentile(arr, 50)), 2),
            "p90_ms": round(float(np.percentile(arr, 90)), 2),
            "p95_ms": round(float(np.percentile(arr, 95)), 2),
            "p99_ms": round(float(np.percentile(arr, 99)), 2),
            "min_ms": round(float(sorted_vals[0]), 2),
            "max_ms": round(float(sorted_vals[-1]), 2),
        }
