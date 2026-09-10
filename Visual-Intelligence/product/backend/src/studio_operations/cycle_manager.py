"""
Phase 15 Studio Cycle Manager.
Manages recurring operational periods (weekly/monthly cycles) across campaigns.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from src.studio_operations.exceptions import ClientContextViolation, StudioOperationError
from src.studio_operations.studio_models import StudioCycle

class StudioCycleManager:
    """Manages cycle creation, progression, and completion for client campaigns."""

    def __init__(self):
        self._cycles: Dict[str, StudioCycle] = {}

    def start_cycle(
        self,
        requesting_client_id: str,
        cycle_id: str,
        campaign_id: str,
        client_id: str,
        cycle_number: int,
        cycle_type: str = "WEEKLY"
    ) -> StudioCycle:
        """Starts a new operational cycle under client isolation."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot start cycle for client '{client_id}' from context '{requesting_client_id}'."
            )
        if cycle_id in self._cycles:
            raise StudioOperationError(f"Cycle '{cycle_id}' already exists.")

        cycle = StudioCycle(
            cycle_id=cycle_id,
            campaign_id=campaign_id,
            client_id=client_id,
            cycle_number=cycle_number,
            cycle_type=cycle_type,
            status="IN_PROGRESS"
        )
        self._cycles[cycle_id] = cycle
        return cycle

    def complete_cycle(self, requesting_client_id: str, cycle_id: str) -> StudioCycle:
        """Completes an operational cycle."""
        if cycle_id not in self._cycles:
            raise StudioOperationError(f"Cycle '{cycle_id}' not found.")
        cycle = self._cycles[cycle_id]
        if requesting_client_id != cycle.client_id:
            raise ClientContextViolation("Client isolation violation.")

        cycle.status = "COMPLETED"
        cycle.end_time = datetime.now(timezone.utc).isoformat()
        return cycle

    def get_cycles_for_campaign(self, requesting_client_id: str, campaign_id: str) -> List[StudioCycle]:
        """Lists all cycles for a campaign."""
        return [c for c in self._cycles.values() if c.campaign_id == campaign_id and c.client_id == requesting_client_id]
