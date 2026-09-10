"""
Phase 15 Workstream Manager.
Manages persistent creative workstreams attached to campaigns with client isolation.
"""

from typing import Dict, List, Optional
from src.studio_operations.exceptions import ClientContextViolation, StudioOperationError
from src.studio_operations.studio_models import Workstream

class WorkstreamManager:
    """Manages creation, retrieval, and status tracking for persistent workstreams."""

    def __init__(self):
        self._workstreams: Dict[str, Workstream] = {}

    def create_workstream(
        self,
        requesting_client_id: str,
        workstream_id: str,
        campaign_id: str,
        client_id: str,
        name: str,
        workstream_type: str = "social_content"
    ) -> Workstream:
        """Creates a workstream attached to a campaign."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot create workstream for client '{client_id}' from requesting context '{requesting_client_id}'."
            )
        if workstream_id in self._workstreams:
            raise StudioOperationError(f"Workstream '{workstream_id}' already exists.")

        workstream = Workstream(
            workstream_id=workstream_id,
            campaign_id=campaign_id,
            client_id=client_id,
            name=name,
            workstream_type=workstream_type
        )
        self._workstreams[workstream_id] = workstream
        return workstream

    def get_workstream(self, requesting_client_id: str, workstream_id: str) -> Workstream:
        """Retrieves a workstream with fail-closed client isolation."""
        if workstream_id not in self._workstreams:
            raise StudioOperationError(f"Workstream '{workstream_id}' not found.")
        workstream = self._workstreams[workstream_id]
        if requesting_client_id != workstream.client_id:
            raise ClientContextViolation(
                f"CROSS-CLIENT LEAKAGE: Client '{requesting_client_id}' cannot access workstream '{workstream_id}' owned by '{workstream.client_id}'."
            )
        return workstream

    def list_workstreams_for_campaign(self, requesting_client_id: str, campaign_id: str) -> List[Workstream]:
        """Lists all workstreams under a specific campaign."""
        return [
            w for w in self._workstreams.values()
            if w.campaign_id == campaign_id and w.client_id == requesting_client_id
        ]
