"""
Unit tests for Phase 17 Multi-Client Production Isolation.
"""

import pytest
from src.production_fabric.orchestrator import ProductionFabricOrchestrator
from src.production_fabric.production_models import ProductionRequest
from src.production_fabric.exceptions import CrossClientFabricViolation

def test_multi_client_isolation(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "iso_ledger"))
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    orch.studio_orchestrator.register_client_engagement("client_b", "Beta", "Retail")

    orch.studio_orchestrator.bind_client_brand("client_a", "b1", "Alpha Brand")
    orch.studio_orchestrator.bind_client_brand("client_b", "b2", "Beta Brand")

    orch.studio_orchestrator.launch_campaign("client_a", "ca", "b1", "Camp A", "Growth")
    orch.studio_orchestrator.launch_campaign("client_b", "cb", "b2", "Camp B", "Awareness")

    req_a = ProductionRequest("req_a", "client_a", "ca", "b1", "Post A")
    req_b = ProductionRequest("req_b", "client_b", "cb", "b2", "Post B")

    item_a = orch.submit_production_request(req_a)
    item_b = orch.submit_production_request(req_b)

    rt_a = orch.studio_runtime.get_or_create_client_runtime("client_a")
    assert rt_a.get_work_item(item_a.item_id).item_id == item_a.item_id

    with pytest.raises(CrossClientFabricViolation):
        rt_a.get_work_item(item_b.item_id)
