"""
Phase 25 Model Intelligence and Telemetry Views.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ModelTelemetryItem:
    model_name: str
    provider: str
    role_assignment: str
    total_calls_count: int
    p50_latency_ms: float
    p95_latency_ms: float
    total_input_tokens: int
    total_output_tokens: int
    total_cost_usd: float
    error_rate_pct: float
    active_fallback: bool = False
