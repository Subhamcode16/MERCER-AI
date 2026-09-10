"""
Phase 25 Golden Visual Benchmark Comparison Views.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class VisualBenchmarkComparatorView:
    benchmark_id: str
    benchmark_version: str
    total_golden_samples: int
    mean_pass_rate_pct: float
    regression_detected: bool
    last_benchmark_run_timestamp: float
