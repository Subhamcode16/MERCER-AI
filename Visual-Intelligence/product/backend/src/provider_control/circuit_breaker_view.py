"""
Phase 25 Provider Circuit Breaker State Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class CircuitBreakerStatusView:
    provider: str
    state: str # CLOSED, OPEN, HALF_OPEN
    failure_count: int
    last_failure_timestamp: float
    recovery_probes_remaining: int
    is_tripped: bool
