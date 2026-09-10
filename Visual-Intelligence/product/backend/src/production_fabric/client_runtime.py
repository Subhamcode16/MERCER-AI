"""
Phase 17 Client Production Runtime.
Maintains an unshared, isolated runtime state for a single client.
Enforces INV-17-008: Client Isolation.
"""

from typing import Dict, Any, List, Optional
from src.production_fabric.production_models import ProductionWorkItem, ProductionRun
from src.production_fabric.exceptions import CrossClientFabricViolation

class ClientProductionRuntime:
    """Isolated runtime context managing production state for a single tenant."""

    def __init__(self, client_id: str):
        if not client_id or not client_id.strip():
            raise CrossClientFabricViolation("ClientProductionRuntime requires a non-empty client_id.")
        self.client_id = client_id
        self._active_runs: Dict[str, ProductionRun] = {}
        self._work_items: Dict[str, ProductionWorkItem] = {}

    def register_work_item(self, item: ProductionWorkItem) -> None:
        """Registers a work item into client runtime context after verifying client match."""
        if item.client_id != self.client_id:
            raise CrossClientFabricViolation(
                f"ClientProductionRuntime for '{self.client_id}' cannot register item belonging to '{item.client_id}'."
            )
        self._work_items[item.item_id] = item

    def get_work_item(self, item_id: str) -> ProductionWorkItem:
        if item_id not in self._work_items:
            raise CrossClientFabricViolation(f"Item '{item_id}' not found in runtime for client '{self.client_id}'.")
        return self._work_items[item_id]

    def list_work_items(self) -> List[ProductionWorkItem]:
        return list(self._work_items.values())
