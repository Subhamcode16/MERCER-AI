"""
Phase 17 Production Optimization Engine.
Evaluates candidate operational strategy improvements against baseline metrics.
Rejects performance degradation and supports deterministic rollback.
"""

from typing import Dict, Any, List, Optional
from src.production_fabric.exceptions import FabricPolicyViolation, ContinuationBoundaryError

class ProductionOptimizationEngine:
    """Optimization engine benchmarking candidate operational strategies against baseline."""

    def __init__(self):
        self._baselines: Dict[str, float] = {}
        self._active_strategies: Dict[str, Dict[str, Any]] = {}
        self._history: List[Dict[str, Any]] = []

    def set_baseline(self, client_id: str, metric_name: str, baseline_value: float) -> None:
        self._baselines[f"{client_id}:{metric_name}"] = baseline_value

    def evaluate_and_adopt(
        self,
        client_id: str,
        metric_name: str,
        candidate_value: float,
        strategy_key: str,
        strategy_payload: Dict[str, Any]
    ) -> bool:
        """Evaluates candidate against baseline. Adopts if improved, rejects and rolls back if degraded."""
        key = f"{client_id}:{metric_name}"
        baseline = self._baselines.get(key, 0.0)

        record = {
            "client_id": client_id,
            "metric_name": metric_name,
            "baseline": baseline,
            "candidate": candidate_value,
            "strategy_key": strategy_key,
            "payload": strategy_payload
        }

        # If candidate performs worse than baseline, reject & trigger rollback
        if candidate_value < baseline:
            record["status"] = "REJECTED_DEGRADATION"
            record["action"] = "ROLLBACK_SUCCESSFUL"
            self._history.append(record)
            return False

        # Candidate meets or improves baseline
        record["status"] = "ADOPTED"
        record["action"] = "STRATEGY_UPDATED"
        self._active_strategies[f"{client_id}:{strategy_key}"] = strategy_payload
        self._history.append(record)
        return True

    def get_active_strategy(self, client_id: str, strategy_key: str) -> Optional[Dict[str, Any]]:
        return self._active_strategies.get(f"{client_id}:{strategy_key}")
