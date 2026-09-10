"""
Phase 19 - Intelligence Events & Stream Observer.

Defines structured event models for pattern discovery, strategy lifecycle transitions,
provenance hash-chain verification, workforce recommendations, and governance audits.
"""

import time
import uuid
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class CreativeIntelligenceEvent(BaseModel):
    """Structured event payload for Phase 19 audit logging."""
    event_id: str = Field(default_factory=lambda: f"evt_ci_{uuid.uuid4().hex[:12]}")
    event_type: str  # "PATTERN_DISCOVERED", "STRATEGY_REGISTERED", "STRATEGY_ACTIVATED", "STRATEGY_RETIRED", "RECOMMENDATION_GENERATED", "GOVERNANCE_AUDIT_PASSED"
    phase: str = "Phase19_CreativeIntelligence"
    client_id: Optional[str] = None  # None if global
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class IntelligenceEventStream:
    """In-memory event channel for Phase 19 intelligence telemetry."""

    def __init__(self):
        self._events: List[CreativeIntelligenceEvent] = []

    def emit(self, event_type: str, details: Dict[str, Any], client_id: Optional[str] = None) -> CreativeIntelligenceEvent:
        event = CreativeIntelligenceEvent(
            event_type=event_type,
            details=details,
            client_id=client_id
        )
        self._events.append(event)
        return event

    def get_events(self, event_type: Optional[str] = None) -> List[CreativeIntelligenceEvent]:
        if event_type:
            return [e for e in self._events if e.event_type == event_type]
        return list(self._events)
