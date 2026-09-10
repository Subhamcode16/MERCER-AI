"""
Phase 15 Human Approval Queue.
Provides non-forgeable approval requests and fail-closed expiration management.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import ApprovalRequiredError, ApprovalExpiredError, ClientContextViolation

@dataclass
class ApprovalItem:
    approval_id: str
    client_id: str
    campaign_id: str
    workstream_id: str
    deliverable_id: str
    proposed_action: str
    capability: str
    target_platform: str
    risk_classification: str
    artifact_references: List[str]
    critique_summary: Dict[str, Any]
    independent_review: Dict[str, Any]
    planned_effect: str
    ttl_hours: int = 24
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED, EXPIRED
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str = field(default_factory=lambda: (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat())

    def is_expired(self) -> bool:
        """Returns True if the current time exceeds the expiration timestamp."""
        now = datetime.now(timezone.utc)
        exp = datetime.fromisoformat(self.expires_at)
        return now > exp

class ApprovalQueue:
    """Manages creation, inspection, approval, rejection, and expiration of human approval items."""

    def __init__(self):
        self._items: Dict[str, ApprovalItem] = {}

    def enqueue_request(
        self,
        requesting_client_id: str,
        approval_id: str,
        client_id: str,
        campaign_id: str,
        workstream_id: str,
        deliverable_id: str,
        proposed_action: str,
        capability: str,
        target_platform: str,
        risk_classification: str = "MEDIUM",
        artifact_references: Optional[List[str]] = None,
        critique_summary: Optional[Dict] = None,
        independent_review: Optional[Dict] = None,
        planned_effect: str = "Publish social post",
        ttl_hours: int = 24
    ) -> ApprovalItem:
        """Enqueues an approval request with client isolation checks."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot enqueue approval for client '{client_id}' from context '{requesting_client_id}'."
            )
        if approval_id in self._items:
            raise ApprovalRequiredError(f"Approval item '{approval_id}' already exists.")

        item = ApprovalItem(
            approval_id=approval_id,
            client_id=client_id,
            campaign_id=campaign_id,
            workstream_id=workstream_id,
            deliverable_id=deliverable_id,
            proposed_action=proposed_action,
            capability=capability,
            target_platform=target_platform,
            risk_classification=risk_classification,
            artifact_references=artifact_references or [],
            critique_summary=critique_summary or {},
            independent_review=independent_review or {},
            planned_effect=planned_effect,
            ttl_hours=ttl_hours
        )
        self._items[approval_id] = item
        return item

    def get_approval(self, requesting_client_id: str, approval_id: str) -> ApprovalItem:
        """Retrieves approval item, auto-expiring if TTL passed."""
        if approval_id not in self._items:
            raise ApprovalRequiredError(f"Approval item '{approval_id}' not found.")
        item = self._items[approval_id]
        if requesting_client_id != item.client_id:
            raise ClientContextViolation(
                f"CROSS-CLIENT LEAKAGE: Client '{requesting_client_id}' cannot access approval '{approval_id}' owned by '{item.client_id}'."
            )
        
        # Check expiration
        if item.status == "PENDING" and item.is_expired():
            item.status = "EXPIRED"

        return item

    def record_human_decision(
        self,
        requesting_client_id: str,
        approval_id: str,
        approved: bool,
        authorizer_id: str,
        reason: str = ""
    ) -> ApprovalItem:
        """Records an explicit human decision (approve/reject). Cannot manufacture approvals."""
        item = self.get_approval(requesting_client_id, approval_id)
        
        if item.status == "EXPIRED":
            raise ApprovalExpiredError(f"Cannot approve expired item '{approval_id}'.")
        if item.status != "PENDING":
            raise ApprovalRequiredError(f"Approval item '{approval_id}' is already in state '{item.status}'.")

        item.status = "APPROVED" if approved else "REJECTED"
        return item

    def list_pending_approvals(self, requesting_client_id: str) -> List[ApprovalItem]:
        """Lists active pending approval items for a client."""
        pending = []
        for item in self._items.values():
            if item.client_id == requesting_client_id:
                if item.status == "PENDING" and item.is_expired():
                    item.status = "EXPIRED"
                if item.status == "PENDING":
                    pending.append(item)
        return pending
