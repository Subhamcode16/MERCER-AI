"""
Phase 24 SLO Models, Error Budget Status, and Alert Definitions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time

class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    ROLLBACK_TRIGGER = "ROLLBACK_TRIGGER"

@dataclass
class SLOTarget:
    name: str
    target_value: float
    unit: str
    is_upper_bound: bool = True  # True if metric must be <= target_value (e.g. latency, error rate)

@dataclass
class SLOMetricWindow:
    window_id: str
    start_time: float
    end_time: float
    total_events: int
    successful_events: int
    failed_events: int
    availability_ratio: float
    p50_latency_ms: float
    p90_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    malformed_output_rate: float
    policy_rejections: int

@dataclass
class ErrorBudgetStatus:
    total_budget: float  # e.g., 0.001 (for 99.9% availability)
    consumed_budget: float
    remaining_budget: float
    burn_rate_1h: float
    burn_rate_24h: float
    exhausted: bool = False
    timestamp: float = field(default_factory=time.time)

@dataclass
class BurnRateAlert:
    alert_id: str
    severity: AlertSeverity
    slo_name: str
    burn_rate: float
    message: str
    recommended_action: str
    timestamp: float = field(default_factory=time.time)
