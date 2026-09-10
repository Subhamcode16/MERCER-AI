"""
Phase 17 Production Observability Stream.
Emits structured, secret-free telemetry events covering production lifecycle milestones.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List
from src.client_experience.presentation_policy import PresentationPolicyEngine

@dataclass(frozen=True)
class ObservabilityEvent:
    event_id: str
    event_type: str
    client_id: str
    campaign_id: str
    item_id: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ProductionObservabilityStream:
    """Stream logger projecting secret-free operational events."""

    def __init__(self):
        self._events: List[ObservabilityEvent] = []
        self._policy = PresentationPolicyEngine()

    def emit_event(
        self,
        event_id: str,
        event_type: str,
        client_id: str,
        campaign_id: str,
        item_id: str,
        payload: Dict[str, Any]
    ) -> ObservabilityEvent:
        """Sanitizes payload to scrub secrets and emits telemetry event."""
        sanitized = self._policy.sanitize_dict(payload)
        event = ObservabilityEvent(
            event_id=event_id,
            event_type=event_type,
            client_id=client_id,
            campaign_id=campaign_id,
            item_id=item_id,
            payload=sanitized
        )
        self._events.append(event)
        return event

    def list_events_for_client(self, client_id: str) -> List[ObservabilityEvent]:
        return [e for e in self._events if e.client_id == client_id]
