"""
Phase 22 Model Observability: Model Health Aggregator
-----------------------------------------------------
Aggregates real-time health telemetry across providers and models.
"""

from typing import Dict, Any, List
from src.model_observability.invocation_trace import InvocationTrace

class ModelHealthAggregator:
    """Tracks per-model availability, success rates, and decay signals."""

    def __init__(self):
        self._model_stats: Dict[str, Dict[str, int]] = {}

    def ingest_trace(self, trace: InvocationTrace) -> None:
        model_key = f"{trace.provider}:{trace.model}"
        if model_key not in self._model_stats:
            self._model_stats[model_key] = {"success": 0, "fail": 0, "timeout": 0, "policy_rejected": 0}
        
        if trace.status == "SUCCESS":
            self._model_stats[model_key]["success"] += 1
        elif trace.timeout_occurred:
            self._model_stats[model_key]["timeout"] += 1
        elif trace.policy_rejected:
            self._model_stats[model_key]["policy_rejected"] += 1
        else:
            self._model_stats[model_key]["fail"] += 1

    def get_health_report(self) -> Dict[str, Any]:
        report = {}
        for model_key, counts in self._model_stats.items():
            total = sum(counts.values())
            success_rate = (counts["success"] / total) if total > 0 else 0.0
            report[model_key] = {
                "total_calls": total,
                "success_rate": round(success_rate, 4),
                "breakdown": counts,
                "status": "HEALTHY" if success_rate >= 0.95 else ("DEGRADED" if success_rate >= 0.8 else "UNHEALTHY"),
            }
        return report
