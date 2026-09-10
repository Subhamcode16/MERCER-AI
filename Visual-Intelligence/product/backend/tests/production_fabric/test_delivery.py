"""
Unit tests for Phase 17 Delivery Coordinator.
"""

from src.production_fabric.delivery import DeliveryCoordinator
from src.production_fabric.production_models import ProductionWorkItem
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_delivery_coordinator_staff_assignment(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "deliv_ledger"))
    coord = DeliveryCoordinator()
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")

    coord.assign_workforce(item, ["art_director_01", "copywriter_01"], orch)
    assert "art_director_01" in item.assigned_staff_ids
    assert "copywriter_01" in item.assigned_staff_ids
