"""
Phase 14 Event Stream
---------------------
Structured workflow event emission and streaming for client observation.
Guarantees secret-free payload formatting and system-only generation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import uuid
import time

from src.workflow_gateway.workflow_projection import WorkflowProjectionEngine
from src.workflow_gateway.exceptions import SecretExposureError

@dataclass(frozen=True)
class WorkflowEvent:
    event_id: str
    workflow_id: str
    mission_id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        # Verify secret sanitization on payload
        payload_str = str(self.payload).lower()
        if any(secret in payload_str for secret in ["secret_key", "bearer_token", "private_key"]):
            raise SecretExposureError("Secret material detected in WorkflowEvent payload!")

class WorkflowEventStream:
    """In-memory event bus and stream for workflow control plane events."""

    def __init__(self):
        self._events: List[WorkflowEvent] = []

    def emit(
        self,
        workflow_id: str,
        mission_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> WorkflowEvent:
        """Emits a new secret-sanitized system WorkflowEvent."""
        sanitized_payload = WorkflowProjectionEngine.sanitize_dict(payload)
        event_id = f"evt-{uuid.uuid4().hex[:8]}"
        evt = WorkflowEvent(
            event_id=event_id,
            workflow_id=workflow_id,
            mission_id=mission_id,
            event_type=event_type,
            payload=sanitized_payload,
            timestamp=time.time(),
        )
        self._events.append(evt)
        return evt

    def list_events(self, workflow_id: str) -> List[WorkflowEvent]:
        """Lists emitted events for a given workflow ID."""
        return [evt for evt in self._events if evt.workflow_id == workflow_id]
