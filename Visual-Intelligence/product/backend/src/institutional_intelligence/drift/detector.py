"""
Strategic Drift Detection Module (Phase 30).
Detects divergence between objectives, initiatives, assumptions, evidence, and measured outcomes.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class DriftSignal(BaseModel):
    drift_id: str = Field(default_factory=lambda: f"drf_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    drift_type: str  # OBJECTIVE_INITIATIVE_DIVERGENCE, ASSUMPTION_EVIDENCE_DIVERGENCE, OUTCOME_EXPECTATION_DIVERGENCE, HORIZON_EXECUTION_DIVERGENCE
    severity: float = Field(ge=0.0, le=1.0, default=0.5)
    title: str
    divergence_summary: str
    target_id: str  # Objective, initiative, or assumption ID
    detected_at: datetime = Field(default_factory=utc_now)
    evidence_ids: List[str] = Field(default_factory=list)
    is_suppressed: bool = False  # Invariant: Must never be silently suppressed (T30-010)


class StrategicDriftDetector:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._drift_signals: List[DriftSignal] = []

    def detect_drift(
        self,
        drift_type: str,
        target_id: str,
        title: str,
        divergence_summary: str,
        severity: float,
        evidence_ids: List[str]
    ) -> DriftSignal:
        signal = DriftSignal(
            tenant_id=self.tenant_id,
            drift_type=drift_type,
            severity=severity,
            title=title,
            divergence_summary=divergence_summary,
            target_id=target_id,
            evidence_ids=evidence_ids
        )
        self._drift_signals.append(signal)
        return signal

    def list_active_drift_signals(self) -> List[DriftSignal]:
        # T30-010: Drift suppression prevention - all signals must surface
        return [s for s in self._drift_signals if not s.is_suppressed]

    def attempt_suppression(self, drift_id: str, actor: str):
        # T30-010: Prevent unverified suppression of strategic drift
        raise GovernanceInvariantViolation(
            ThreatID.T30_010,
            f"Strategic drift signal '{drift_id}' cannot be silently suppressed.",
            {"drift_id": drift_id, "actor": actor}
        )
