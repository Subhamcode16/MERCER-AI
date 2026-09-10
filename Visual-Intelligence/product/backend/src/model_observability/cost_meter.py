"""
Phase 22 Model Observability: Cost Meter
-----------------------------------------
Tracks token consumption and real known costs.
Rule: Never invent pricing. If provider price is unknown, record UNKNOWN / None.
"""

from typing import Dict, Any, Optional, List
from src.model_observability.invocation_trace import InvocationTrace

class CostMeter:
    """Tracks token volume and known cost attribution."""

    def __init__(self):
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_known_cost_usd = 0.0
        self._unknown_cost_invocations = 0

    def ingest_trace(self, trace: InvocationTrace) -> None:
        if trace.input_tokens is not None:
            self._total_input_tokens += trace.input_tokens
        if trace.output_tokens is not None:
            self._total_output_tokens += trace.output_tokens
        
        if trace.known_cost_usd is not None:
            self._total_known_cost_usd += trace.known_cost_usd
        else:
            self._unknown_cost_invocations += 1

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_tokens": self._total_input_tokens + self._total_output_tokens,
            "total_known_cost_usd": round(self._total_known_cost_usd, 6),
            "unknown_cost_invocations": self._unknown_cost_invocations,
        }
