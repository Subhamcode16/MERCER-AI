"""
Initiative Health Module (Phase 30).
Multi-dimensional evaluation of initiative trajectory with first-class UNKNOWN state handling.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import InitiativeHealthState, ThreatID, GovernanceInvariantViolation, utc_now


class InitiativeHealthReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"hlth_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    initiative_id: str
    overall_state: InitiativeHealthState
    alignment_score: float = Field(ge=0.0, le=1.0, default=0.5)
    evidence_quality: float = Field(ge=0.0, le=1.0, default=0.5)
    progress_rate: float = Field(ge=0.0, le=1.0, default=0.5)
    dependency_health: float = Field(ge=0.0, le=1.0, default=0.5)
    assumption_stability: float = Field(ge=0.0, le=1.0, default=0.5)
    is_contradicted: bool = False
    is_stale: bool = False
    notes: List[str] = Field(default_factory=list)
    evaluated_at: datetime = Field(default_factory=utc_now)


class InitiativeHealthEvaluator:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def evaluate(
        self,
        initiative_id: str,
        alignment_score: float = 0.8,
        evidence_quality: float = 0.7,
        progress_rate: float = 0.6,
        dependency_health: float = 0.9,
        assumption_stability: float = 0.8,
        has_contradictions: bool = False,
        is_stale: bool = False,
        is_unknown: bool = False
    ) -> InitiativeHealthReport:
        notes = []
        if is_unknown:
            state = InitiativeHealthState.UNKNOWN
            notes.append("Insufficient data to establish definitive health state.")
        elif has_contradictions:
            state = InitiativeHealthState.CONTRADICTED
            notes.append("Active assumptions or evidence have been contradicted.")
        elif is_stale:
            state = InitiativeHealthState.STALE
            notes.append("Evidence or review timeline is overdue.")
        elif dependency_health < 0.3:
            state = InitiativeHealthState.BLOCKED
            notes.append("Blocked by upstream dependency failure.")
        elif alignment_score < 0.4 or progress_rate < 0.3 or assumption_stability < 0.4:
            state = InitiativeHealthState.AT_RISK
            notes.append("Underperforming across alignment, progress, or assumption stability.")
        elif alignment_score < 0.7 or progress_rate < 0.5:
            state = InitiativeHealthState.WATCH
            notes.append("Moderate variance detected; placed on watch list.")
        else:
            state = InitiativeHealthState.HEALTHY
            notes.append("Operating within normal strategic parameters.")

        return InitiativeHealthReport(
            tenant_id=self.tenant_id,
            initiative_id=initiative_id,
            overall_state=state,
            alignment_score=alignment_score,
            evidence_quality=evidence_quality,
            progress_rate=progress_rate,
            dependency_health=dependency_health,
            assumption_stability=assumption_stability,
            is_contradicted=has_contradictions,
            is_stale=is_stale,
            notes=notes
        )
