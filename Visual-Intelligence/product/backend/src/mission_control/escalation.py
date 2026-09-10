"""
Phase 11 Escalation Manager.

Handles policy conflicts, authorization missing events, budget exhaustion, and quality failures
by safely pausing mission continuation, creating structured escalation tickets, and waiting for external tokens.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from .mission_state import MissionState, MissionStateMachine


class EscalationReason(Enum):
    """Reason codes requiring mission escalation."""
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    AUTHORIZATION_REQUIRED = "AUTHORIZATION_REQUIRED"
    RESOURCE_SCOPE_CONFLICT = "RESOURCE_SCOPE_CONFLICT"
    POLICY_CONFLICT = "POLICY_CONFLICT"
    REPEATED_FAILURE = "REPEATED_FAILURE"
    QUALITY_FAILURE = "QUALITY_FAILURE"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    SECURITY_ANOMALY = "SECURITY_ANOMALY"


@dataclass
class EscalationTicket:
    """Structured human review / authorization request ticket."""
    ticket_id: str
    mission_id: str
    task_id: Optional[str]
    reason: EscalationReason
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolution_notes: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EscalationManager:
    """Manages creation, tracking, and resolution of escalation tickets."""

    def __init__(self):
        self.tickets: Dict[str, EscalationTicket] = {}

    def escalate(
        self,
        mission_id: str,
        reason: EscalationReason,
        message: str,
        task_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> EscalationTicket:
        """Generates an escalation ticket for a mission."""
        ticket_id = f"esc_{mission_id}_{len(self.tickets) + 1:04d}"
        ticket = EscalationTicket(
            ticket_id=ticket_id,
            mission_id=mission_id,
            task_id=task_id,
            reason=reason,
            message=message,
            details=details or {},
        )
        self.tickets[ticket_id] = ticket
        return ticket

    def resolve_ticket(self, ticket_id: str, resolution_notes: str) -> EscalationTicket:
        """Resolves an open escalation ticket."""
        if ticket_id not in self.tickets:
            raise KeyError(f"Escalation ticket '{ticket_id}' not found.")

        ticket = self.tickets[ticket_id]
        ticket.resolved = True
        ticket.resolution_notes = resolution_notes
        return ticket

    def get_pending_tickets(self, mission_id: Optional[str] = None) -> List[EscalationTicket]:
        """Returns all unresolved escalation tickets."""
        pending = [t for t in self.tickets.values() if not t.resolved]
        if mission_id:
            pending = [t for t in pending if t.mission_id == mission_id]
        return pending
