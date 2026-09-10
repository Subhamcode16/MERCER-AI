"""
Unit tests for Phase 15 Studio Operations Orchestrator.
"""

import pytest
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_studio_orchestrator_end_to_end_flow(tmp_path):
    ledger_dir = str(tmp_path / "orch_ledger")
    orch = StudioOperationsOrchestrator(ledger_dir=ledger_dir)

    # 1. Register Client
    client = orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    assert client["client_id"] == "client_nocap"

    # 2. Bind Brand
    brand = orch.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")
    assert brand["brand_id"] == "brand_nocap"

    # 3. Launch Campaign
    camp = orch.launch_campaign("client_nocap", "camp_001", "brand_nocap", "September Campaign", "Brand awareness")
    assert camp["status"] == "ACTIVE"

    # 4. Evaluate Continuity
    plan = orch.evaluate_continuity("client_nocap", "camp_001")
    assert plan.status == "VALID"

    # 5. Verify Ledger
    assert orch.verify_ledger_integrity() is True
