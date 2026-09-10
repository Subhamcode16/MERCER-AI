"""
Phase 17 Production Approval Orchestrator.
Identifies approval requirements, prepares structured approval packages, routes requests to Phase 16 approval queue,
and tracks approval status and expiry without manufacturing authorization tokens.
"""

from typing import Dict, Any, Optional
from src.production_fabric.production_models import ProductionWorkItem, ProductionState
from src.production_fabric.exceptions import ApprovalOrchestrationError, StaleProductionStateError

class ProductionApprovalOrchestrator:
    """Orchestrator preparing and tracking approval packages via Phase 10 & 16 surfaces."""

    def __init__(self):
        self._packages: Dict[str, Dict[str, Any]] = {}

    def prepare_approval_package(
        self,
        item: ProductionWorkItem,
        approval_id: str,
        capability: str,
        platform: str,
        studio_orchestrator: Any
    ) -> Dict[str, Any]:
        """Prepares an approval package and submits it to Phase 15/16 approval queue."""
        client_id = item.client_id
        # Submit approval item to Phase 15 studio operations approval queue
        appr_item = studio_orchestrator.submit_deliverable_for_human_approval(
            requesting_client_id=client_id,
            approval_id=approval_id,
            campaign_id=item.campaign_id,
            workstream_id=item.workstream_id,
            deliverable_id=item.deliverable_id,
            proposed_action=capability,
            capability=capability,
            target_platform=platform
        )

        package = {
            "approval_id": approval_id,
            "item_id": item.item_id,
            "client_id": client_id,
            "deliverable_id": item.deliverable_id,
            "capability": capability,
            "platform": platform,
            "status": appr_item.status,
            "created_at": appr_item.created_at
        }
        self._packages[approval_id] = package
        item.transition_to(ProductionState.AWAITING_APPROVAL)
        return package

    def check_approval_status(self, approval_id: str, studio_orchestrator: Any) -> str:
        """Queries Phase 15 approval queue for approval status."""
        if approval_id not in self._packages:
            raise ApprovalOrchestrationError(f"Approval package '{approval_id}' not found.")

        pkg = self._packages[approval_id]
        client_id = pkg["client_id"]

        try:
            appr_item = studio_orchestrator.approval_queue.get_approval(client_id, approval_id)
            pkg["status"] = appr_item.status
            return appr_item.status
        except Exception as e:
            pkg["status"] = "EXPIRED"
            return "EXPIRED"
