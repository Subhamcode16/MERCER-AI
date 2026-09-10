"""
Phase 28 Environmental & Model Drift Detector.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone


class DriftType(str, Enum):
    MODEL_VERSION_DRIFT = "MODEL_VERSION_DRIFT"
    COMPILER_SYNTAX_DRIFT = "COMPILER_SYNTAX_DRIFT"
    SKILL_VERSION_DRIFT = "SKILL_VERSION_DRIFT"
    MACRO_SEASONALITY_DRIFT = "MACRO_SEASONALITY_DRIFT"


@dataclass
class DriftAlert:
    alert_id: str
    drift_type: DriftType
    affected_component: str
    old_version_or_state: str
    new_version_or_state: str
    severity: str  # "LOW", "MEDIUM", "HIGH"
    confounder_warning: str
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EnvironmentDriftDetector:
    """Detects infrastructure, model, and compiler drift that could confound historical learning."""

    def __init__(self):
        self._alerts: List[DriftAlert] = []

    def check_and_record_drift(
        self,
        drift_type: DriftType,
        affected_component: str,
        old_state: str,
        new_state: str,
    ) -> Optional[DriftAlert]:
        if old_state != new_state:
            alert = DriftAlert(
                alert_id=f"drf_{uuid.uuid4().hex[:8]}",
                drift_type=drift_type,
                affected_component=affected_component,
                old_version_or_state=old_state,
                new_version_or_state=new_state,
                severity="MEDIUM",
                confounder_warning=(
                    f"Confounder Warning: Drift detected in {affected_component} ({old_state} -> {new_state}). "
                    "Performance shifts cannot be purely attributed to creative changes."
                ),
            )
            self._alerts.append(alert)
            return alert
        return None

    def list_alerts(self) -> List[DriftAlert]:
        return list(self._alerts)
