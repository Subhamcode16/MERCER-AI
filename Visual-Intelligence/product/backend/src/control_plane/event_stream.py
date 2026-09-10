"""
Phase 25 In-Memory Tenant-Isolated Async Event Stream Bus.
"""
import asyncio
import logging
import time
import uuid
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, field
from src.control_plane.dto import sanitize_payload

logger = logging.getLogger(__name__)

@dataclass
class ControlPlaneEvent:
    event_id: str = field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:10]}")
    event_type: str = ""
    tenant_id: str = ""
    client_id: str = ""
    correlation_id: str = ""
    timestamp: float = field(default_factory=time.time)
    payload: Dict[str, Any] = field(default_factory=dict)

class ControlPlaneEventStreamBus:
    """Publish-subscribe bus ensuring strict tenant and client event stream isolation."""

    def __init__(self):
        self._subscribers: Dict[str, Set[asyncio.Queue]] = {} # tenant_id -> set of queues
        self._history: List[ControlPlaneEvent] = []

    def subscribe(self, tenant_id: str, client_id: str) -> asyncio.Queue:
        """Subscribes an operator connection to tenant-specific events."""
        q: asyncio.Queue = asyncio.Queue(maxsize=1000)
        key = f"{tenant_id}:{client_id}"
        if key not in self._subscribers:
            self._subscribers[key] = set()
        self._subscribers[key].add(q)
        return q

    def unsubscribe(self, tenant_id: str, client_id: str, q: asyncio.Queue) -> None:
        key = f"{tenant_id}:{client_id}"
        if key in self._subscribers and q in self._subscribers[key]:
            self._subscribers[key].remove(q)

    async def publish(self, event: ControlPlaneEvent) -> None:
        """Publishes event strictly to matching tenant/client subscribers."""
        # Sanitize event payload to prevent secret leaks into web sockets
        clean_payload = sanitize_payload(event.payload)
        sanitized_event = ControlPlaneEvent(
            event_id=event.event_id,
            event_type=event.event_type,
            tenant_id=event.tenant_id,
            client_id=event.client_id,
            correlation_id=event.correlation_id,
            timestamp=event.timestamp,
            payload=clean_payload
        )
        self._history.append(sanitized_event)

        # Notify exact tenant:client subscribers
        exact_key = f"{event.tenant_id}:{event.client_id}"
        wildcard_client_key = f"{event.tenant_id}:*"
        admin_key = "*:*"

        target_queues = set()
        if exact_key in self._subscribers:
            target_queues.update(self._subscribers[exact_key])
        if wildcard_client_key in self._subscribers:
            target_queues.update(self._subscribers[wildcard_client_key])
        if admin_key in self._subscribers:
            target_queues.update(self._subscribers[admin_key])

        for q in target_queues:
            try:
                q.put_nowait(sanitized_event)
            except asyncio.QueueFull:
                logger.warning(f"Subscriber queue full; dropping event {event.event_id}")

    def get_tenant_history(self, tenant_id: str, client_id: str, limit: int = 50) -> List[ControlPlaneEvent]:
        """Returns recent events matching tenant and client scope."""
        events = []
        for e in reversed(self._history):
            if tenant_id == "*" or (e.tenant_id == tenant_id and (client_id == "*" or e.client_id == client_id)):
                events.append(e)
            if len(events) >= limit:
                break
        return list(reversed(events))
