"""
Phase 25 Error Budget Burn Rate and Risk Gauge View.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ErrorBudgetBurnView:
    total_budget_percentage: float = 0.10 # 0.1% for 99.9% availability
    consumed_percentage: float = 0.0
    burn_rate_ratio: float = 0.0 # Burn rate over baseline
    alert_status: str = "HEALTHY" # HEALTHY, WARNING, CRITICAL, EXHAUSTED
    circuit_breaker_tripped: bool = False
