"""
Phase 17 Substrate Integration & Regression Test.
Verifies Phase 17 operating seamlessly on top of Phase 14, Phase 15, and Phase 16 substrates.
"""

from src.production_fabric.orchestrator import ProductionFabricOrchestrator
from src.client_experience.command_center import StudioCommandCenter
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_phase17_substrate_integration(tmp_path):
    studio_orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "reg_studio_ledger"))
    cmd_center = StudioCommandCenter(studio_orchestrator=studio_orch, audit_dir=str(tmp_path / "reg_cmd_ledger"))
    prod_fabric = ProductionFabricOrchestrator(studio_orchestrator=studio_orch, ledger_dir=str(tmp_path / "reg_prod_ledger"))

    # Register client via command center
    studio_orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    studio_orch.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")
    studio_orch.launch_campaign("client_nocap", "camp_001", "brand_nocap", "Fall Drop", "Awareness")

    # Verify all control planes share consistent client context
    assert prod_fabric.studio_orchestrator.client_manager.get_client("client_nocap", "client_nocap").name == "NOCAP Studio"
    assert cmd_center.studio_orchestrator.client_manager.get_client("client_nocap", "client_nocap").name == "NOCAP Studio"
