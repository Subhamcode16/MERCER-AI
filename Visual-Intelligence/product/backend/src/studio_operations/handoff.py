"""
Phase 15 Human Handoff Manager.
Generates structured, inspectable human handoff packages for escalation, approval, and decision events.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import ClientContextViolation

@dataclass
class HandoffPackage:
    handoff_id: str
    client_id: str
    campaign_id: str
    deliverable_id: Optional[str]
    reason_code: str  # REVISION_LIMIT_EXCEEDED, REVIEW_REJECTION, POLICY_CONFLICT, MISSING_CREDENTIAL, AMBIGUOUS_DIRECTION, HIGH_RISK_ACTION
    summary: str
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    context_data: Dict[str, Any]
    suggested_actions: List[str]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class HumanHandoffManager:
    """Manages creation and collection of human handoff packages."""

    def __init__(self):
        self._handoffs: Dict[str, HandoffPackage] = {}

    def create_handoff(
        self,
        requesting_client_id: str,
        handoff_id: str,
        client_id: str,
        campaign_id: str,
        reason_code: str,
        summary: str,
        risk_level: str = "HIGH",
        deliverable_id: Optional[str] = None,
        context_data: Optional[Dict] = None,
        suggested_actions: Optional[List[str]] = None
    ) -> HandoffPackage:
        """Creates a human handoff package under client isolation checks."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot create handoff for client '{client_id}' from context '{requesting_client_id}'."
            )

        handoff = HandoffPackage(
            handoff_id=handoff_id,
            client_id=client_id,
            campaign_id=campaign_id,
            deliverable_id=deliverable_id,
            reason_code=reason_code,
            summary=summary,
            risk_level=risk_level,
            context_data=context_data or {},
            suggested_actions=suggested_actions or ["Review issue", "Provide human direction", "Override or re-assign"]
        )
        self._handoffs[handoff_id] = handoff
        return handoff

    def get_handoff(self, requesting_client_id: str, handoff_id: str) -> HandoffPackage:
        """Retrieves handoff with client isolation."""
        if handoff_id not in self._handoffs:
            raise KeyError(f"Handoff '{handoff_id}' not found.")
        handoff = self._handoffs[handoff_id]
        if requesting_client_id != handoff.client_id:
            raise ClientContextViolation("Client isolation violation.")
        return handoff

    def list_handoffs_for_client(self, requesting_client_id: str) -> List[HandoffPackage]:
        """Lists active handoffs for a client."""
        return [h for h in self._handoffs.values() if h.client_id == requesting_client_id]
