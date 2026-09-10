"""
Unit tests for Phase 17 Client Production Runtime.
"""

import pytest
from src.production_fabric.client_runtime import ClientProductionRuntime
from src.production_fabric.production_models import ProductionWorkItem
from src.production_fabric.exceptions import CrossClientFabricViolation

def test_client_runtime_isolation():
    runtime_a = ClientProductionRuntime("client_a")
    item_a = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    item_b = ProductionWorkItem("w2", "r2", "client_b", "c1", "ws1", "d1", "Title")

    runtime_a.register_work_item(item_a)
    assert runtime_a.get_work_item("w1").item_id == "w1"

    with pytest.raises(CrossClientFabricViolation):
        runtime_a.register_work_item(item_b)
