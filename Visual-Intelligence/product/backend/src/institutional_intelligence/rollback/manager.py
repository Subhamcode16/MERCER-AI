"""
Rollback & Invalidation Manager (Phase 30).
Coordinates recommendation withdrawal, assumption invalidation, initiative pauses, and decision supersession.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class RollbackEvent(BaseModel):
    rollback_id: str = Field(default_factory=lambda: f"rbk_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    target_type: str  # RECOMMENDATION, ASSUMPTION, INITIATIVE, DECISION, BRIEF
    target_id: str
    reason: str
    initiated_by: str
    timestamp: datetime = Field(default_factory=utc_now)
    restored_state_summary: Optional[str] = None


class StrategicRollbackManager:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._rollback_log: List[RollbackEvent] = []

    def execute_rollback(
        self,
        target_type: str,
        target_id: str,
        reason: str,
        actor: str,
        state_summary: str = ""
    ) -> RollbackEvent:
        event = RollbackEvent(
            tenant_id=self.tenant_id,
            target_type=target_type,
            target_id=target_id,
            reason=reason,
            initiated_by=actor,
            restored_state_summary=state_summary
        )
        self._rollback_log.append(event)
        return event

    def assert_no_zombie_authority_restoration(self, rollback_id: str, attempted_privilege: str):
        # T30-032: Rollback must never restore authority that was revoked or expired
        raise GovernanceInvariantViolation(
            ThreatID.T30_032,
            f"Rollback '{rollback_id}' cannot restore revoked/expired execution authority: {attempted_privilege}",
            {"rollback_id": rollback_id, "attempted_privilege": attempted_privilege}
        )
