"""
Phase 28 Learning Signal Generator.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class LearningSignalType(str, Enum):
    POSITIVE_SIGNAL = "POSITIVE_SIGNAL"
    NEGATIVE_SIGNAL = "NEGATIVE_SIGNAL"
    MIXED_SIGNAL = "MIXED_SIGNAL"
    NO_SIGNAL = "NO_SIGNAL"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    CONTRADICTORY_SIGNAL = "CONTRADICTORY_SIGNAL"


@dataclass
class LearningSignal:
    signal_id: str
    campaign_id: str
    target_entity: str  # e.g. "token:raking_monolithic_late_sun", "direction:Monolithic_Elegance"
    signal_type: LearningSignalType
    observed_metric: str
    delta_percentage: float
    sample_size: int
    confidence: float
    supporting_notes: str


class LearningSignalGenerator:
    """Generates classified learning signals based on normalized metrics and sample thresholds."""

    def evaluate_signal(
        self,
        campaign_id: str,
        target_entity: str,
        observed_metric: str,
        actual_value: float,
        baseline_value: float,
        sample_size: int,
    ) -> LearningSignal:
        if sample_size < 100:
            return LearningSignal(
                signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                target_entity=target_entity,
                signal_type=LearningSignalType.INSUFFICIENT_EVIDENCE,
                observed_metric=observed_metric,
                delta_percentage=0.0,
                sample_size=sample_size,
                confidence=0.3,
                supporting_notes=f"Sample size ({sample_size}) is below minimum statistical threshold of 100 observations.",
            )

        delta = ((actual_value - baseline_value) / baseline_value) * 100.0 if baseline_value > 0 else 0.0

        if delta >= 10.0:
            sig_type = LearningSignalType.POSITIVE_SIGNAL
            conf = min(0.95, 0.70 + (sample_size / 5000.0) * 0.25)
        elif delta <= -10.0:
            sig_type = LearningSignalType.NEGATIVE_SIGNAL
            conf = min(0.95, 0.70 + (sample_size / 5000.0) * 0.25)
        elif abs(delta) < 3.0:
            sig_type = LearningSignalType.NO_SIGNAL
            conf = 0.85
        else:
            sig_type = LearningSignalType.MIXED_SIGNAL
            conf = 0.65

        return LearningSignal(
            signal_id=f"sig_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            target_entity=target_entity,
            signal_type=sig_type,
            observed_metric=observed_metric,
            delta_percentage=round(delta, 2),
            sample_size=sample_size,
            confidence=round(conf, 3),
            supporting_notes=f"Observed {delta:+.2f}% delta in {observed_metric} over baseline across {sample_size} impressions/interactions.",
        )
