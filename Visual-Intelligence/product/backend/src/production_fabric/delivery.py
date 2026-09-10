"""
Phase 17 Delivery Coordinator.
Coordinates workforce assignment, mission creation, critique/review routing,
and execution dispatch through existing Phase 10-13 substrate controls without bypassing any boundary.
"""

from typing import Dict, Any, List, Optional
from src.production_fabric.production_models import ProductionWorkItem, ProductionState
from src.production_fabric.exceptions import ContinuationBoundaryError, FabricPolicyViolation

from src.studio_operations.studio_models import DeliverableStatus

class DeliveryCoordinator:
    """Coordinator routing work items through Phase 14 workforce, Phase 15 studio ops, and Phase 10-13 controls."""

    def __init__(self):
        self._assignments: Dict[str, List[str]] = {}

    def assign_workforce(
        self,
        item: ProductionWorkItem,
        staff_ids: List[str],
        studio_orchestrator: Any
    ) -> None:
        """Assigns specialized staff identities from Phase 14 workforce to work item."""
        registry = studio_orchestrator.workforce_orchestrator.staff_registry
        for staff_id in staff_ids:
            # Verify staff existence in registry
            staff = registry.get_staff(staff_id)
            if staff_id not in item.assigned_staff_ids:
                item.assigned_staff_ids.append(staff.staff_id)
        self._assignments[item.item_id] = item.assigned_staff_ids

    def advance_production_stage(
        self,
        item: ProductionWorkItem,
        target_state: ProductionState,
        studio_orchestrator: Any,
        content_payload: Optional[Dict[str, Any]] = None
    ) -> ProductionWorkItem:
        """Advances work item state in lockstep with Studio Operations deliverable FSM."""
        deliv_id = item.deliverable_id
        client_id = item.client_id
        deliv_mgr = studio_orchestrator.deliverable_manager
        deliv = deliv_mgr.get_deliverable(client_id, deliv_id)

        # Map ProductionState to DeliverableStatus Enum
        if target_state == ProductionState.IN_PRODUCTION:
            if deliv.status == DeliverableStatus.PLANNED:
                deliv_mgr.transition_deliverable(client_id, deliv_id, DeliverableStatus.IN_PROGRESS)
        elif target_state == ProductionState.CRITIQUE:
            if deliv.status == DeliverableStatus.IN_PROGRESS:
                deliv_mgr.transition_deliverable(client_id, deliv_id, DeliverableStatus.DRAFT)
            if deliv.status in (DeliverableStatus.DRAFT, DeliverableStatus.REVISION):
                deliv_mgr.transition_deliverable(client_id, deliv_id, DeliverableStatus.CRITIQUE)
        elif target_state == ProductionState.REVIEW:
            if deliv.status == DeliverableStatus.CRITIQUE:
                deliv_mgr.transition_deliverable(client_id, deliv_id, DeliverableStatus.REVIEW)

        item.transition_to(target_state)
        return item
