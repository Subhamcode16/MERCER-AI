"""
Unit tests for Phase 17 Production Intake Manager.
"""

import pytest
from src.production_fabric.intake import ProductionIntakeManager
from src.production_fabric.production_models import ProductionRequest
from src.studio_operations.orchestrator import StudioOperationsOrchestrator
from src.production_fabric.exceptions import WorkIntakeError, CrossClientFabricViolation

def test_intake_admission_flow(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "intake_ledger"))
    orch.register_client_engagement("client_a", "Alpha Corp", "Tech")
    orch.bind_client_brand("client_a", "brand_a", "Alpha Brand")
    orch.launch_campaign("client_a", "camp_a", "brand_a", "Launch Campaign", "Growth")

    intake = ProductionIntakeManager()
    req = ProductionRequest("req_101", "client_a", "camp_a", "brand_a", "Launch Hero Video")
    item = intake.admit_request(req, orch)

    assert item.item_id == "work_req_101"
    assert item.client_id == "client_a"
    assert item.state.value == "ADMITTED"

from src.studio_operations.exceptions import ClientContextViolation

def test_intake_invalid_client(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "intake_invalid"))
    intake = ProductionIntakeManager()
    req = ProductionRequest("req_102", "client_nonexistent", "camp_a", "brand_a", "Hero Video")

    with pytest.raises((CrossClientFabricViolation, ClientContextViolation)):
        intake.admit_request(req, orch)
