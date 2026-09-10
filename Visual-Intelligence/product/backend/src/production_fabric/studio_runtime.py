"""
Phase 17 Studio Production Runtime.
Maintains studio-level tenant map and isolated ClientProductionRuntime instances without cross-tenant data leaks.
"""

from typing import Dict, List, Optional
from src.production_fabric.client_runtime import ClientProductionRuntime
from src.production_fabric.exceptions import CrossClientFabricViolation

class StudioProductionRuntime:
    """Global studio runtime orchestrating isolated per-client runtime instances."""

    def __init__(self):
        self._runtimes: Dict[str, ClientProductionRuntime] = {}

    def get_or_create_client_runtime(self, client_id: str) -> ClientProductionRuntime:
        """Gets or creates an isolated ClientProductionRuntime for a client."""
        if not client_id or not client_id.strip():
            raise CrossClientFabricViolation("client_id cannot be empty.")
        if client_id not in self._runtimes:
            self._runtimes[client_id] = ClientProductionRuntime(client_id)
        return self._runtimes[client_id]

    def list_active_clients(self) -> List[str]:
        return list(self._runtimes.keys())
