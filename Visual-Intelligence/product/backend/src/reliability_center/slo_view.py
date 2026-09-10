"""
Phase 25 SLO Compliance and Availability View.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class SLOComplianceView:
    slo_name: str # e.g. "99.9% Production Availability", "p95 Model Latency <= 2500ms"
    target_value: float
    observed_value: float
    unit: str # "%", "ms"
    is_compliant: bool
    evaluation_window_days: int = 30
