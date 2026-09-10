"""
Intelligence Observability & Telemetry Engine for Phase 29.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import hashlib
from pydantic import BaseModel, Field


class StrategicAuditEvent(BaseModel):
    event_id: str
    tenant_id: str
    actor: str
    actor_type: str  # SYSTEM, OPERATOR, EXTERNAL
    object_id: str
    object_type: str  # SIGNAL, HYPOTHESIS, SCENARIO, RECOMMENDATION, DECISION
    previous_state: Optional[str] = None
    new_state: str
    reason: str
    evidence_refs: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StrategicTelemetryEngine:
    def __init__(self):
        self._events: List[StrategicAuditEvent] = []

    def record_event(
        self,
        tenant_id: str,
        actor: str,
        actor_type: str,
        object_id: str,
        object_type: str,
        new_state: str,
        reason: str,
        previous_state: Optional[str] = None,
        evidence_refs: Optional[List[str]] = None,
    ) -> StrategicAuditEvent:
        ev_id = f"AUD-{hashlib.sha256(f'{tenant_id}:{object_id}:{new_state}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"
        
        event = StrategicAuditEvent(
            event_id=ev_id,
            tenant_id=tenant_id,
            actor=actor,
            actor_type=actor_type,
            object_id=object_id,
            object_type=object_type,
            previous_state=previous_state,
            new_state=new_state,
            reason=reason,
            evidence_refs=evidence_refs or [],
        )
        self._events.append(event)
        return event

    def get_events(self, tenant_id: Optional[str] = None) -> List[StrategicAuditEvent]:
        if not tenant_id:
            return list(self._events)
        return [e for e in self._events if e.tenant_id == tenant_id]
