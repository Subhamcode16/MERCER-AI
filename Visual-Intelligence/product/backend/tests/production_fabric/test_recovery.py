"""
Unit tests for Phase 17 Production Recovery Engine.
"""

from src.production_fabric.recovery import ProductionRecoveryEngine
from src.production_fabric.production_models import ProductionWorkItem, ProductionState
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_recovery_expired_approval(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "rec_ledger"))
    rec = ProductionRecoveryEngine()
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    item.transition_to(ProductionState.ADMITTED)
    item.transition_to(ProductionState.IN_PRODUCTION)
    item.transition_to(ProductionState.CRITIQUE)
    item.transition_to(ProductionState.REVIEW)
    item.transition_to(ProductionState.AWAITING_APPROVAL)

    res = rec.handle_expired_approval(item, "appr_exp", orch)
    assert res.state == ProductionState.IN_PRODUCTION
    assert res.retry_count == 1
