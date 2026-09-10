"""
Strategic Cadence Module (Phase 30).
Orchestrates scheduled intelligence preparation routines (Daily, Weekly, Monthly, Quarterly, Ad-hoc)
with strict fail-closed authorization bounds.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import (
    StrategicCadenceType,
    ThreatID,
    GovernanceInvariantViolation,
    utc_now,
)


class CadenceExecutionRecord(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"cad_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    cadence_type: StrategicCadenceType
    executed_at: datetime = Field(default_factory=utc_now)
    changes_detected: List[str] = Field(default_factory=list)
    new_evidence_count: int = 0
    contradictions_found: List[str] = Field(default_factory=list)
    assumption_updates: List[str] = Field(default_factory=list)
    initiative_health_changes: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_agenda_items: List[str] = Field(default_factory=list)
    is_preparation_only: bool = True  # Always True - cannot execute consequential actions


class StrategicCadenceEngine:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._history: List[CadenceExecutionRecord] = []

    def run_cadence_preparation(
        self,
        cadence_type: StrategicCadenceType,
        changes: List[str],
        contradictions: List[str],
        assumption_updates: List[str],
        is_automated_cron: bool = True
    ) -> CadenceExecutionRecord:
        record = CadenceExecutionRecord(
            tenant_id=self.tenant_id,
            cadence_type=cadence_type,
            changes_detected=changes,
            new_evidence_count=len(changes),
            contradictions_found=contradictions,
            assumption_updates=assumption_updates,
            recommended_agenda_items=[
                f"Review {len(contradictions)} identified contradictions",
                f"Assess {len(assumption_updates)} changed assumptions",
                "Evaluate priority attention queue"
            ],
            is_preparation_only=True
        )
        self._history.append(record)
        return record

    def assert_no_automated_execution_authority(self, cadence_id: str, attempted_action: str):
        # T30-004 / T30-020: Scheduled cadence preparation cannot alter or execute initiatives
        raise GovernanceInvariantViolation(
            ThreatID.T30_004,
            f"Scheduled cadence routine '{cadence_id}' attempted unauthorized execution action: {attempted_action}",
            {"cadence_id": cadence_id, "action": attempted_action}
        )
