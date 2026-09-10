"""
Multi-client isolation integration tests for Phase 15 Studio Operations.
"""

import pytest
from src.studio_operations.orchestrator import StudioOperationsOrchestrator
from src.studio_operations.exceptions import ClientContextViolation

def test_multi_client_isolation_orchestrator(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "iso_ledger"))

    # Register Client A (NOCAP) and Client B (Brand Beta)
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    orch.register_client_engagement("client_beta", "Beta Apparel", "Athletics")

    orch.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")
    orch.bind_client_brand("client_beta", "brand_beta", "Beta")

    orch.launch_campaign("client_nocap", "camp_nocap", "brand_nocap", "NOCAP Fall", "Growth")
    orch.launch_campaign("client_beta", "camp_beta", "brand_beta", "Beta Spring", "Awareness")

    # Client A attempting to access Client B campaign
    with pytest.raises(ClientContextViolation):
        orch.evaluate_continuity(requesting_client_id="client_nocap", campaign_id="camp_beta")

    # Client B attempting to access Client A campaign
    with pytest.raises(ClientContextViolation):
        orch.evaluate_continuity(requesting_client_id="client_beta", campaign_id="camp_nocap")
