"""
Phase 25 Canary Release and Automated Rollback Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class CanaryRollbackStatusView:
    active_release_version: str
    canary_traffic_split_pct: float
    canary_error_rate_pct: float
    baseline_error_rate_pct: float
    sla_breach_detected: bool
    automated_rollback_triggered: bool
    last_rollback_timestamp: Optional[float] = None
    last_known_good_version: str = "v24.0.0"
