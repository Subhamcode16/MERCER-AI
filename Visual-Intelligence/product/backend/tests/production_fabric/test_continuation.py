"""
Unit tests for Phase 17 Bounded Continuation Engine.
"""

import pytest
from src.production_fabric.continuation import BoundedContinuationEngine
from src.production_fabric.production_models import ProductionWorkItem, ProductionState
from src.production_fabric.exceptions import ContinuationBoundaryError
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_continuation_engine_tier_0_rejection(tmp_path):
    engine = BoundedContinuationEngine()
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "cont_ledger"))
    orch.register_client_engagement("client_a", "Alpha", "Tech")

    with pytest.raises(ContinuationBoundaryError):
        engine.evaluate_continuation(item, autonomy_tier=0, requires_approval=False, has_valid_approval=False, studio_orchestrator=orch)

def test_continuation_engine_step_progression(tmp_path):
    engine = BoundedContinuationEngine()
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    item.transition_to(ProductionState.ADMITTED)
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "cont_ledger2"))
    orch.register_client_engagement("client_a", "Alpha", "Tech")

    step = engine.evaluate_continuation(item, autonomy_tier=1, requires_approval=False, has_valid_approval=False, studio_orchestrator=orch)
    assert step == "START_PRODUCTION"
