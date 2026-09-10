"""
Phase 25 Latency Distribution and Percentile Histograms.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class LatencyPercentileDistributionView:
    component: str
    sample_count: int
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    slo_target_p95_ms: float
    compliant: bool
