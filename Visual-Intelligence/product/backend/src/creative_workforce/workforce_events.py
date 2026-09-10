"""
Phase 14 Workforce Event Stream
-------------------------------
Emits secret-free operational events for workforce activities, delegation, critique,
independent review, trend intake, and self-improvement experiments.
Scrubs raw secrets and credentials prior to event broadcast.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import uuid

from src.creative_workforce.exceptions import UntrustedObservationInjectionError

SECRET_KEYWORDS = ["secret", "password", "token", "private_key", "bearer", "api_key"]

@dataclass(frozen=True)
class WorkforceEvent:
    """Secret-free event emitted by the Phase 14 Workforce Event Stream."""
    event_id: str
    event_type: str
    client_id: str
    campaign_id: str
    staff_id: str
    payload: Dict[str, Any]
    emitted_at: float = field(default_factory=time.time)

class WorkforceEventStream:
    """Stream managing workforce telemetry events."""

    def __init__(self):
        self._events: List[WorkforceEvent] = []

    def emit_event(
        self,
        event_type: str,
        client_id: str,
        campaign_id: str,
        staff_id: str,
        payload: Dict[str, Any],
    ) -> WorkforceEvent:
        """Emits a secret-scrubbed workforce event."""
        # Validate that payload contains no raw secrets
        for k, v in payload.items():
            if any(sk in k.lower() for sk in SECRET_KEYWORDS):
                raise UntrustedObservationInjectionError(f"Event payload contains secret field '{k}'. Leakage blocked.")

        event_id = f"evt-{uuid.uuid4().hex[:8]}"
        evt = WorkforceEvent(
            event_id=event_id,
            event_type=event_type,
            client_id=client_id,
            campaign_id=campaign_id,
            staff_id=staff_id,
            payload=payload,
        )
        self._events.append(evt)
        return evt

    def list_events_for_campaign(self, campaign_id: str) -> List[WorkforceEvent]:
        """Lists events emitted for a specific campaign."""
        return [e for e in self._events if e.campaign_id == campaign_id]
