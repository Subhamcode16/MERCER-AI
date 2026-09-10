"""
Strategic Decision Memory separating Decision Quality from Subsequent Outcome Quality.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
from pydantic import BaseModel, Field
from ..bridge.campaign_bridge import HumanDecisionRecord


class DecisionQualityGrade(str, Enum):
    HIGH_RIGOR_EVIDENCE_BOUND = "HIGH_RIGOR_EVIDENCE_BOUND"
    MODERATE_RIGOR_ASSUMPTIONS_CONTAINED = "MODERATE_RIGOR_ASSUMPTIONS_CONTAINED"
    LOW_RIGOR_SPECULATIVE = "LOW_RIGOR_SPECULATIVE"


class StrategicDecisionMemoryRecord(BaseModel):
    record_id: str
    tenant_id: str
    decision_record: HumanDecisionRecord
    decision_quality_grade: DecisionQualityGrade
    subsequent_outcome_metrics: Dict[str, Any] = Field(default_factory=dict)
    outcome_observed_at: Optional[datetime] = None
    outcome_alignment: Optional[str] = None  # ALIGNED, DIVERGED, INCONCLUSIVE
    retrospective_learnings: List[str] = Field(default_factory=list)
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StrategicDecisionMemoryStore:
    def __init__(self):
        self._records: Dict[str, StrategicDecisionMemoryRecord] = {}

    def record_decision_memory(
        self,
        decision: HumanDecisionRecord,
        decision_quality_grade: DecisionQualityGrade = DecisionQualityGrade.HIGH_RIGOR_EVIDENCE_BOUND,
    ) -> StrategicDecisionMemoryRecord:
        rec_id = f"MEM-{hashlib.sha256(f'{decision.decision_id}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"
        
        record = StrategicDecisionMemoryRecord(
            record_id=rec_id,
            tenant_id=decision.tenant_id,
            decision_record=decision,
            decision_quality_grade=decision_quality_grade,
        )
        self._records[rec_id] = record
        return record

    def update_subsequent_outcome(
        self,
        record_id: str,
        metrics: Dict[str, Any],
        outcome_alignment: str,
        retrospective_learnings: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
    ) -> StrategicDecisionMemoryRecord:
        record = self._records.get(record_id)
        if not record:
            raise ValueError(f"Memory record '{record_id}' not found.")
        if tenant_id and record.tenant_id != tenant_id:
            raise ValueError(f"Access denied for tenant '{tenant_id}'.")

        record.subsequent_outcome_metrics = metrics
        record.outcome_alignment = outcome_alignment
        record.outcome_observed_at = datetime.now(timezone.utc)
        if retrospective_learnings:
            record.retrospective_learnings.extend(retrospective_learnings)

        return record

    def get_memory(self, record_id: str, tenant_id: Optional[str] = None) -> Optional[StrategicDecisionMemoryRecord]:
        rec = self._records.get(record_id)
        if not rec:
            return None
        if tenant_id and rec.tenant_id != tenant_id:
            return None
        return rec

    def list_memories(self, tenant_id: str) -> List[StrategicDecisionMemoryRecord]:
        return [m for m in self._records.values() if m.tenant_id == tenant_id]
