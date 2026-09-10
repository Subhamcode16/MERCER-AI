"""
Phase 26 Workforce Activity Stream & Event Broadcaster.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from src.control_plane.dto import DTOSanitizer


class WorkforceEventType(str, Enum):
    WORKER_TASK_STARTED = "worker_task_started"
    WORKER_TASK_COMPLETED = "worker_task_completed"
    WORKER_TASK_FAILED = "worker_task_failed"
    WORKER_DELEGATED = "worker_delegated"
    WORKER_HANDOFF_CREATED = "worker_handoff_created"
    WORKER_HANDOFF_REJECTED = "worker_handoff_rejected"
    WORKER_TOOL_REQUESTED = "worker_tool_requested"
    WORKER_TOOL_DENIED = "worker_tool_denied"
    WORKER_POLICY_BLOCKED = "worker_policy_blocked"
    WORKER_WAITING_APPROVAL = "worker_waiting_approval"
    WORKER_APPROVAL_RECEIVED = "worker_approval_received"
    WORKER_APPROVAL_REJECTED = "worker_approval_rejected"
    WORKER_MEMORY_READ = "worker_memory_read"
    WORKER_MEMORY_WRITTEN = "worker_memory_written"
    WORKER_SKILL_STARTED = "worker_skill_started"
    WORKER_SKILL_COMPLETED = "worker_skill_completed"
    WORKER_ROUTINE_TRIGGERED = "worker_routine_triggered"
    WORKER_ROUTINE_BLOCKED = "worker_routine_blocked"
    WORKER_CONTEXT_DENIED = "worker_context_denied"
    WORKER_SUSPENDED = "worker_suspended"
    WORKER_RETIRED = "worker_retired"


@dataclass
class WorkforceEvent:
    event_id: str
    event_type: WorkforceEventType
    tenant_id: str
    client_id: str
    worker_id: str
    room_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WorkforceActivityLogger:
    """Logs sanitized workforce events without secret or CoT leakage."""

    def __init__(self):
        self._events: List[WorkforceEvent] = []

    def emit_event(
        self,
        event_type: WorkforceEventType,
        tenant_id: str,
        client_id: str,
        worker_id: str,
        payload: Optional[Dict[str, Any]] = None,
        room_id: Optional[str] = None,
    ) -> WorkforceEvent:
        # Sanitize payload to purge sensitive tokens and internal reasoning
        sanitized_payload = DTOSanitizer.sanitize(payload or {})

        event = WorkforceEvent(
            event_id=f"wevt_{uuid.uuid4().hex[:12]}",
            event_type=event_type,
            tenant_id=tenant_id,
            client_id=client_id,
            worker_id=worker_id,
            room_id=room_id,
            payload=sanitized_payload,
        )
        self._events.append(event)
        return event

    def query_events(
        self,
        tenant_id: str,
        client_id: Optional[str] = None,
        worker_id: Optional[str] = None,
        room_id: Optional[str] = None,
        event_type: Optional[WorkforceEventType] = None,
    ) -> List[WorkforceEvent]:
        results = []
        for evt in self._events:
            if evt.tenant_id != tenant_id and evt.tenant_id != "*":
                continue
            if client_id and evt.client_id != client_id and evt.client_id != "*":
                continue
            if worker_id and evt.worker_id != worker_id:
                continue
            if room_id and evt.room_id != room_id:
                continue
            if event_type and evt.event_type != event_type:
                continue
            results.append(evt)
        return results
