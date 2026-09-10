"""
Observability & Strategic Telemetry Module (Phase 30).
Structured audit logging, state transition metrics, and replay verification.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import utc_now


class StrategicAuditEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    event_type: str  # REVIEW_GENERATED, DECISION_CHANGED, ASSUMPTION_INVALIDATED, DRIFT_DETECTED, AUTH_DENIED, ROLLBACK_TRIGGERED
    actor: str
    scope: str
    evidence_references: List[str] = Field(default_factory=list)
    authorization_state: str = "VALID"
    state_transition: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=utc_now)


class StrategicTelemetryEngine:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._audit_log: List[StrategicAuditEvent] = []

    def record_event(
        self,
        event_type: str,
        actor: str,
        scope: str,
        state_transition: Dict[str, Any],
        evidence_refs: Optional[List[str]] = None,
        auth_state: str = "VALID"
    ) -> StrategicAuditEvent:
        event = StrategicAuditEvent(
            tenant_id=self.tenant_id,
            event_type=event_type,
            actor=actor,
            scope=scope,
            evidence_references=evidence_refs or [],
            authorization_state=auth_state,
            state_transition=state_transition
        )
        self._audit_log.append(event)
        return event

    def list_events(self, event_type: Optional[str] = None) -> List[StrategicAuditEvent]:
        if event_type:
            return [e for e in self._audit_log if e.event_type == event_type]
        return list(self._audit_log)
