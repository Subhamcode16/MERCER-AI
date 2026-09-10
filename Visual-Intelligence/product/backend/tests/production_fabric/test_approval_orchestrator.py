"""
Unit tests for Phase 17 Production Approval Orchestrator.
"""

from src.production_fabric.approval_orchestrator import ProductionApprovalOrchestrator
from src.production_fabric.production_models import ProductionWorkItem, ProductionState
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_approval_orchestrator_package_creation(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "appr_ledger"))
    orch.register_client_engagement("client_a", "Alpha", "Tech")
    orch.bind_client_brand("client_a", "brand_a", "Brand Alpha")
    orch.launch_campaign("client_a", "c1", "brand_a", "Camp", "Obj")
    from src.studio_operations.studio_models import DeliverableStatus
    orch.deliverable_manager.create_deliverable("client_a", "d1", "ws1", "c1", "client_a", "Post")
    orch.deliverable_manager.transition_deliverable("client_a", "d1", DeliverableStatus.IN_PROGRESS)
    orch.deliverable_manager.transition_deliverable("client_a", "d1", DeliverableStatus.DRAFT)
    orch.deliverable_manager.transition_deliverable("client_a", "d1", DeliverableStatus.CRITIQUE)
    orch.deliverable_manager.transition_deliverable("client_a", "d1", DeliverableStatus.REVIEW)

    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    item.transition_to(ProductionState.ADMITTED)
    item.transition_to(ProductionState.IN_PRODUCTION)
    item.transition_to(ProductionState.CRITIQUE)
    item.transition_to(ProductionState.REVIEW)

    appr_orch = ProductionApprovalOrchestrator()
    pkg = appr_orch.prepare_approval_package(item, "appr_99", "publish", "instagram", orch)

    assert pkg["approval_id"] == "appr_99"
    assert item.state == ProductionState.AWAITING_APPROVAL
