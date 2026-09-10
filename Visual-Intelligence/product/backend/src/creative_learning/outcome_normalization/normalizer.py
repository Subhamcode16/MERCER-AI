"""
Phase 28 Outcome Metric Normalization Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


@dataclass
class NormalizedOutcomeMetric:
    metric_id: str
    campaign_id: str
    metric_name: str  # "IMPRESSIONS", "CTR", "CONVERSION_RATE", "AVG_DWELL_TIME_SEC", "SENTIMENT_POSITIVE_RATIO"
    normalized_value: float
    raw_value: float
    unit: str
    source_platform: str
    normalization_rule: str
    time_window: str  # "7_DAY_POST_LAUNCH", "30_DAY_POST_LAUNCH"
    attribution_model: str = "Multi-Touch-Attribution (Correlational - Not Causal)"
    confidence: float = 0.95


class OutcomeNormalizer:
    """Normalizes cross-platform telemetry into unified campaign performance records without losing source semantics."""

    def normalize_feed(self, campaign_id: str, source_platform: str, raw_metrics: Dict[str, Any], time_window: str = "7_DAY_POST_LAUNCH") -> List[NormalizedOutcomeMetric]:
        normalized = []

        # 1. Impressions
        if "impressions" in raw_metrics:
            raw_imp = float(raw_metrics["impressions"])
            normalized.append(NormalizedOutcomeMetric(
                metric_id=f"met_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                metric_name="IMPRESSIONS",
                normalized_value=raw_imp,
                raw_value=raw_imp,
                unit="count",
                source_platform=source_platform,
                normalization_rule="IDENTITY_INTEGER",
                time_window=time_window,
            ))

        # 2. CTR
        if "clicks" in raw_metrics and "impressions" in raw_metrics and raw_metrics["impressions"] > 0:
            clicks = float(raw_metrics["clicks"])
            imp = float(raw_metrics["impressions"])
            ctr = clicks / imp
            normalized.append(NormalizedOutcomeMetric(
                metric_id=f"met_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                metric_name="CTR",
                normalized_value=round(ctr, 5),
                raw_value=ctr * 100.0,
                unit="ratio",
                source_platform=source_platform,
                normalization_rule="CLICKS_DIV_IMPRESSIONS",
                time_window=time_window,
            ))
        elif "ctr" in raw_metrics:
            raw_ctr = float(raw_metrics["ctr"])
            normalized_ctr = raw_ctr / 100.0 if raw_ctr > 1.0 else raw_ctr
            normalized.append(NormalizedOutcomeMetric(
                metric_id=f"met_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                metric_name="CTR",
                normalized_value=round(normalized_ctr, 5),
                raw_value=raw_ctr,
                unit="ratio",
                source_platform=source_platform,
                normalization_rule="PERCENT_TO_RATIO",
                time_window=time_window,
            ))

        # 3. Conversion Rate
        if "conversions" in raw_metrics and "clicks" in raw_metrics and raw_metrics["clicks"] > 0:
            conv = float(raw_metrics["conversions"])
            clicks = float(raw_metrics["clicks"])
            cvr = conv / clicks
            normalized.append(NormalizedOutcomeMetric(
                metric_id=f"met_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                metric_name="CONVERSION_RATE",
                normalized_value=round(cvr, 5),
                raw_value=cvr * 100.0,
                unit="ratio",
                source_platform=source_platform,
                normalization_rule="CONVERSIONS_DIV_CLICKS",
                time_window=time_window,
            ))

        # 4. Dwell Time
        if "avg_dwell_sec" in raw_metrics:
            dwell = float(raw_metrics["avg_dwell_sec"])
            normalized.append(NormalizedOutcomeMetric(
                metric_id=f"met_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                metric_name="AVG_DWELL_TIME_SEC",
                normalized_value=dwell,
                raw_value=dwell,
                unit="seconds",
                source_platform=source_platform,
                normalization_rule="SECONDS_DURATION",
                time_window=time_window,
            ))

        return normalized
