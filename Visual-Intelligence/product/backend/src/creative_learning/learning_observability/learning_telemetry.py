"""
Phase 28 Learning Observability & Structured Audit Telemetry.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


@dataclass
class LearningTelemetryEvent:
    event_id: str
    event_name: str
    campaign_id: Optional[str]
    operator_id: Optional[str]
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class LearningTelemetryEmitter:
    """Emits structured audit logs across all learning lifecycle operations."""

    def __init__(self):
        self._events: List[LearningTelemetryEvent] = []

    def emit(
        self,
        event_name: str,
        campaign_id: Optional[str] = None,
        operator_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> LearningTelemetryEvent:
        evt = LearningTelemetryEvent(
            event_id=f"evt_{uuid.uuid4().hex[:8]}",
            event_name=event_name,
            campaign_id=campaign_id,
            operator_id=operator_id,
            payload=payload or {},
        )
        self._events.append(evt)
        return evt

    def list_events(self, event_name: Optional[str] = None, campaign_id: Optional[str] = None) -> List[LearningTelemetryEvent]:
        results = self._events
        if event_name:
            results = [e for e in results if e.event_name == event_name]
        if campaign_id:
            results = [e for e in results if e.campaign_id == campaign_id]
        return results
