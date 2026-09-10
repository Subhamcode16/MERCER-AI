"""
Phase 15 Deliverables Manager.
Enforces strict deliverable lifecycle state transitions (PLANNED -> IN_PROGRESS -> DRAFT -> CRITIQUE -> REVISION -> REVIEW -> APPROVED -> READY_FOR_EXECUTION -> EXECUTED -> OBSERVED -> LEARNED) with client isolation.
"""

from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import DeliverableStateViolation, ClientContextViolation
from src.studio_operations.studio_models import Deliverable, DeliverableStatus, DeliverableType

class DeliverableManager:
    """Manages creation, state machine transitions, and content updates of deliverables."""

    def __init__(self):
        self._deliverables: Dict[str, Deliverable] = {}

    def create_deliverable(
        self,
        requesting_client_id: str,
        deliverable_id: str,
        workstream_id: str,
        campaign_id: str,
        client_id: str,
        title: str,
        deliverable_type: DeliverableType = DeliverableType.SOCIAL_POST,
        content: Optional[Dict[str, Any]] = None
    ) -> Deliverable:
        """Creates a deliverable in PLANNED status under client isolation."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot create deliverable for client '{client_id}' from context '{requesting_client_id}'."
            )
        if deliverable_id in self._deliverables:
            raise DeliverableStateViolation(f"Deliverable '{deliverable_id}' already exists.")

        deliverable = Deliverable(
            deliverable_id=deliverable_id,
            workstream_id=workstream_id,
            campaign_id=campaign_id,
            client_id=client_id,
            title=title,
            deliverable_type=deliverable_type,
            status=DeliverableStatus.PLANNED,
            content=content or {}
        )
        self._deliverables[deliverable_id] = deliverable
        return deliverable

    def transition_deliverable(
        self,
        requesting_client_id: str,
        deliverable_id: str,
        target_status: DeliverableStatus,
        content_update: Optional[Dict[str, Any]] = None
    ) -> Deliverable:
        """Transitions a deliverable to a new state with strict FSM validation."""
        deliverable = self.get_deliverable(requesting_client_id, deliverable_id)
        
        # Enforce state machine transition
        deliverable.transition_to(target_status)
        
        if content_update:
            deliverable.content.update(content_update)
            
        if target_status == DeliverableStatus.REVISION:
            deliverable.revision_count += 1
            deliverable.version = f"1.{deliverable.revision_count}.0"

        return deliverable

    def get_deliverable(self, requesting_client_id: str, deliverable_id: str) -> Deliverable:
        """Retrieves deliverable under strict fail-closed client isolation."""
        if deliverable_id not in self._deliverables:
            raise DeliverableStateViolation(f"Deliverable '{deliverable_id}' not found.")
        deliverable = self._deliverables[deliverable_id]
        if requesting_client_id != deliverable.client_id:
            raise ClientContextViolation(
                f"CROSS-CLIENT LEAKAGE: Client '{requesting_client_id}' cannot access deliverable '{deliverable_id}' owned by '{deliverable.client_id}'."
            )
        return deliverable

    def list_deliverables_for_campaign(
        self, requesting_client_id: str, campaign_id: str, status_filter: Optional[DeliverableStatus] = None
    ) -> List[Deliverable]:
        """Lists deliverables under a campaign filtered by status."""
        items = [
            d for d in self._deliverables.values()
            if d.campaign_id == campaign_id and d.client_id == requesting_client_id
        ]
        if status_filter:
            items = [d for d in items if d.status == status_filter]
        return items
