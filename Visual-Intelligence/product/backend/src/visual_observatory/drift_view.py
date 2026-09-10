"""
Phase 25 Visual Drift and SSIM Deviation Monitor.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class VisualDriftReport:
    artifact_id: str
    baseline_ssim: float
    observed_ssim: float
    ssim_delta: float
    color_delta_e: float
    threshold_limit: float = 0.10
    drift_detected: bool = False
    action_taken: str = "PERMITTED" # PERMITTED, QUARANTINED
