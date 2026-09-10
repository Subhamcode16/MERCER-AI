"""
Phase 24 Visual Quality Drift Detector.
Compares live generation outputs against Phase 21/22 visual baselines (SSIM, color fidelity, prompt adherence).
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class VisualDriftDetector:
    """Detects quality drift and degradation against golden reference visual baselines."""

    def __init__(self, max_allowed_drift: float = 0.15, min_quality_score: float = 0.85):
        self.max_allowed_drift = max_allowed_drift
        self.min_quality_score = min_quality_score

    def evaluate_drift(
        self,
        baseline_score: float,
        live_score: float,
        ssim_similarity: float,
        prompt_adherence_score: float
    ) -> Dict[str, Any]:
        """Calculates drift percentage and evaluates compliance against thresholds."""
        drift_delta = max(0.0, baseline_score - live_score)
        drift_percentage = drift_delta / baseline_score if baseline_score > 0 else 0.0

        is_drift_breached = drift_percentage > self.max_allowed_drift
        is_quality_breached = live_score < self.min_quality_score

        is_degraded = is_drift_breached or is_quality_breached

        if is_degraded:
            logger.warning(f"Visual quality drift detected! Drift: {drift_percentage:.2%}, Live Score: {live_score}")

        return {
            "is_degraded": is_degraded,
            "baseline_score": baseline_score,
            "live_score": live_score,
            "drift_percentage": round(drift_percentage, 4),
            "max_allowed_drift": self.max_allowed_drift,
            "ssim_similarity": ssim_similarity,
            "prompt_adherence": prompt_adherence_score,
            "status": "QUARANTINED" if is_degraded else "PASS"
        }
