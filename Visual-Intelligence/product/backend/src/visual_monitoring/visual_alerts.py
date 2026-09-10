"""
Phase 24 Visual Quality Degradation Alerts and Automated Quarantine.
"""
import logging
from typing import Dict, Any, List
from src.reliability.slo_models import AlertSeverity

logger = logging.getLogger(__name__)

class VisualAlertEngine:
    """Dispatches visual drift alerts and tags corrupted/degraded artifacts for quarantine."""

    def __init__(self):
        self._quarantined_artifacts: List[str] = []

    def handle_drift_evaluation(self, artifact_id: str, drift_result: Dict[str, Any]) -> Dict[str, Any]:
        if drift_result.get("is_degraded", False):
            self._quarantined_artifacts.append(artifact_id)
            logger.warning(f"Artifact {artifact_id} quarantined due to visual degradation/drift!")
            return {
                "action": "QUARANTINE",
                "severity": AlertSeverity.CRITICAL.value,
                "artifact_id": artifact_id,
                "reason": f"Drift {drift_result.get('drift_percentage', 0.0):.2%} exceeded limit"
            }

        return {"action": "PERMIT", "artifact_id": artifact_id}

    def list_quarantined(self) -> List[str]:
        return list(self._quarantined_artifacts)
