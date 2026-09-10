"""
Phase 24 Rolling Visual Quality Window Aggregator.
"""
import time
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VisualQualityWindow:
    """Aggregates visual fidelity scores over rolling invocation windows."""

    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self._scores: List[Dict[str, Any]] = []

    def record_evaluation(self, artifact_id: str, quality_score: float, ssim: float, model_id: str) -> None:
        entry = {
            "artifact_id": artifact_id,
            "quality_score": quality_score,
            "ssim": ssim,
            "model_id": model_id,
            "timestamp": time.time()
        }
        self._scores.append(entry)
        if len(self._scores) > self.window_size:
            self._scores.pop(0)

    def get_window_metrics(self) -> Dict[str, Any]:
        if not self._scores:
            return {"mean_quality": 0.0, "mean_ssim": 0.0, "count": 0}

        mean_q = sum(s["quality_score"] for s in self._scores) / len(self._scores)
        mean_ssim = sum(s["ssim"] for s in self._scores) / len(self._scores)

        return {
            "mean_quality": round(mean_q, 4),
            "mean_ssim": round(mean_ssim, 4),
            "sample_count": len(self._scores)
        }
