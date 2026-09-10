"""
Phase 17 Production Fabric Work Intake Manager.
Ingests approved work requests, validates client context isolation,
creates bounded production objectives and work items without execution authority.
"""

from typing import Dict, List, Optional, Any
from src.production_fabric.production_models import (
    ProductionRequest, ProductionObjective, ProductionWorkItem, ProductionPriority, ProductionState
)
from src.production_fabric.exceptions import WorkIntakeError, CrossClientFabricViolation

class ProductionIntakeManager:
    """Manager validating and ingesting incoming production requests into bounded objectives."""

    def __init__(self):
        self._requests: Dict[str, ProductionRequest] = {}
        self._objectives: Dict[str, ProductionObjective] = {}
        self._items: Dict[str, ProductionWorkItem] = {}

    def admit_request(self, request: ProductionRequest, studio_orchestrator: Any) -> ProductionWorkItem:
        """Admits an approved request, binding context and creating a work item."""
        if request.request_id in self._requests:
            raise WorkIntakeError(f"Production request '{request.request_id}' already admitted.")

        # Validate client engagement exists in studio operations
        client = studio_orchestrator.client_manager.get_client(request.client_id, request.client_id)
        if not client or client.client_id != request.client_id:
            raise CrossClientFabricViolation(f"Invalid client context '{request.client_id}' for intake.")

        # Store request & objective
        self._requests[request.request_id] = request
        obj_id = f"obj_{request.request_id}"
        objective = ProductionObjective(
            objective_id=obj_id,
            client_id=request.client_id,
            campaign_id=request.campaign_id,
            target_deliverables_count=1
        )
        self._objectives[obj_id] = objective

        # Create deliverable under studio operations
        deliv = studio_orchestrator.deliverable_manager.create_deliverable(
            requesting_client_id=request.client_id,
            deliverable_id=f"del_{request.request_id}",
            workstream_id=f"ws_{request.request_id}",
            campaign_id=request.campaign_id,
            client_id=request.client_id,
            title=request.title
        )

        item_id = f"work_{request.request_id}"
        work_item = ProductionWorkItem(
            item_id=item_id,
            request_id=request.request_id,
            client_id=request.client_id,
            campaign_id=request.campaign_id,
            workstream_id=f"ws_{request.request_id}",
            deliverable_id=deliv.deliverable_id,
            title=request.title,
            priority=request.priority,
            state=ProductionState.PENDING
        )
        work_item.transition_to(ProductionState.ADMITTED)
        self._items[item_id] = work_item
        return work_item

    def get_work_item(self, item_id: str) -> ProductionWorkItem:
        if item_id not in self._items:
            raise WorkIntakeError(f"Work item '{item_id}' not found.")
        return self._items[item_id]

    def list_items_for_client(self, client_id: str) -> List[ProductionWorkItem]:
        return [item for item in self._items.values() if item.client_id == client_id]
