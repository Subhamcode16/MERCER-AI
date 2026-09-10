"""
Phase 25 External Provider Health, Quota, and Latency Summary Views.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ExternalProviderHealthSummary:
    provider_id: str
    provider_type: str # LLM, VISUAL, MCP, DATABASE
    status: str # HEALTHY, DEGRADED, OUTAGE, UNCONFIGURED
    p95_latency_ms: float
    error_rate_pct: float
    circuit_breaker_state: str # CLOSED, OPEN, HALF_OPEN
    active_model_or_endpoint: str
