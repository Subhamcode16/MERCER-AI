"""
Phase 28 Confidence-to-Outcome Calibration Tracker.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import math


@dataclass
class CalibrationBucket:
    range_label: str  # e.g. "0.80 - 1.00"
    min_confidence: float
    max_confidence: float
    prediction_count: int = 0
    success_count: int = 0
    empirical_accuracy: float = 0.0
    calibration_error: float = 0.0
    is_statistically_reliable: bool = False  # True if prediction_count >= 50


@dataclass
class CalibrationReport:
    domain: str  # "VISUAL_QUALITY", "CREATIVE_DIRECTION", "AUDIENCE_FIT", "PERFORMANCE_LIFT"
    total_predictions: int
    expected_calibration_error: float
    buckets: List[CalibrationBucket]


class CalibrationTracker:
    """Evaluates whether model confidence aligns with observed empirical reality."""

    def __init__(self):
        self._predictions: Dict[str, List[Dict[str, Any]]] = {
            "VISUAL_QUALITY": [],
            "CREATIVE_DIRECTION": [],
            "AUDIENCE_FIT": [],
            "PERFORMANCE_LIFT": [],
        }

    def record_prediction(self, domain: str, predicted_confidence: float, was_successful: bool):
        if domain not in self._predictions:
            self._predictions[domain] = []
        self._predictions[domain].append({
            "confidence": predicted_confidence,
            "success": was_successful,
        })

    def get_calibration_report(self, domain: str) -> CalibrationReport:
        records = self._predictions.get(domain, [])
        bucket_defs = [
            ("0.00 - 0.20", 0.00, 0.20),
            ("0.20 - 0.40", 0.20, 0.40),
            ("0.40 - 0.60", 0.40, 0.60),
            ("0.60 - 0.80", 0.60, 0.80),
            ("0.80 - 1.00", 0.80, 1.00),
        ]

        buckets = []
        total_error_weighted = 0.0
        total_count = len(records)

        for label, low, high in bucket_defs:
            b_records = [
                r for r in records
                if (low <= r["confidence"] < high) or (high == 1.00 and r["confidence"] == 1.00)
            ]
            count = len(b_records)
            successes = sum(1 for r in b_records if r["success"])
            emp_acc = (successes / count) if count > 0 else 0.0
            avg_conf = (sum(r["confidence"] for r in b_records) / count) if count > 0 else (low + high) / 2.0
            error = abs(emp_acc - avg_conf) if count > 0 else 0.0

            if total_count > 0:
                total_error_weighted += (count / total_count) * error

            buckets.append(CalibrationBucket(
                range_label=label,
                min_confidence=low,
                max_confidence=high,
                prediction_count=count,
                success_count=successes,
                empirical_accuracy=round(emp_acc, 3),
                calibration_error=round(error, 3),
                is_statistically_reliable=(count >= 50),
            ))

        ece = round(total_error_weighted, 3) if total_count > 0 else 0.0
        return CalibrationReport(
            domain=domain,
            total_predictions=total_count,
            expected_calibration_error=ece,
            buckets=buckets,
        )
