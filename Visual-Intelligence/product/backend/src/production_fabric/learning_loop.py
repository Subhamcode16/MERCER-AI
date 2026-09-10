"""
Phase 17 Production Learning Loop.
Connects outcome observations to learning signals, candidate operational strategies, and benchmark evaluations.
Enforces INV-17-004: Learning cannot modify security policy.
"""

from typing import Dict, Any, List, Optional
from src.production_fabric.production_models import ProductionOutcome
from src.production_fabric.production_policy import ProductionPolicyEngine
from src.production_fabric.exceptions import FabricPolicyViolation

class ProductionLearningLoop:
    """Learning loop extracting operational strategies from outcome observations without policy escalation."""

    def __init__(self):
        self._policy_engine = ProductionPolicyEngine()
        self._learning_signals: List[Dict[str, Any]] = []

    def process_outcome_learning(
        self,
        outcome: ProductionOutcome,
        target_strategy_key: str,
        proposed_optimization_value: Any
    ) -> Dict[str, Any]:
        """Processes an outcome into a candidate operational strategy change after policy verification."""
        # Verify that target_strategy_key is NOT an immutable security policy
        self._policy_engine.validate_policy_mutation(target_strategy_key, proposed_optimization_value)

        signal = {
            "signal_id": f"learn_{outcome.outcome_id}",
            "client_id": outcome.client_id,
            "deliverable_id": outcome.deliverable_id,
            "strategy_key": target_strategy_key,
            "proposed_value": proposed_optimization_value,
            "provenance": outcome.provenance,
            "status": "CANDIDATE"
        }
        self._learning_signals.append(signal)
        return signal
