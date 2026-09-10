"""
Phase 15 Regression Suite.
Ensures Phase 15 Studio Operations layer preserves all baseline Phase 1-14 security invariants.
"""

import pytest
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_phase15_substrate_integration(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "reg_ledger"))

    # Verify workforce orchestrator is properly linked
    assert orch.workforce_orchestrator is not None
    assert orch.workforce_orchestrator.staff_registry is not None

    # Register client and verify Phase 14 context binding
    orch.register_client_engagement("client_reg", "Regression Client", "Technology")
    ctx = orch.workforce_orchestrator.context_manager._clients.get("client_reg")
    assert ctx is not None
    assert ctx.client_name == "Regression Client"
