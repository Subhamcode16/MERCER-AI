"""
Unit tests for Phase 17 Production Models.
"""

import pytest
from src.production_fabric.production_models import (
    ProductionRequest, ProductionObjective, ProductionWorkItem, ProductionPriority, ProductionState
)
from src.production_fabric.exceptions import WorkIntakeError, ProductionStateViolation, CrossClientFabricViolation

def test_production_request_validation():
    req = ProductionRequest("req_1", "client_a", "camp_1", "brand_1", "Title", "Desc")
    assert req.request_id == "req_1"
    assert req.client_id == "client_a"

    with pytest.raises(WorkIntakeError):
        ProductionRequest("", "client_a", "camp_1", "brand_1", "Title", "Desc")

    with pytest.raises(CrossClientFabricViolation):
        ProductionRequest("req_1", "", "camp_1", "brand_1", "Title", "Desc")

def test_production_objective_negative_budget():
    with pytest.raises(WorkIntakeError):
        ProductionObjective("obj_1", "client_a", "camp_1", 5, max_budget_units=-10.0)

def test_production_work_item_state_machine():
    item = ProductionWorkItem("w1", "r1", "client_a", "camp_1", "ws_1", "d1", "Title")
    assert item.state == ProductionState.PENDING
    item.transition_to(ProductionState.ADMITTED)
    assert item.state == ProductionState.ADMITTED

    with pytest.raises(ProductionStateViolation):
        item.transition_to(ProductionState.COMPLETED)  # Invalid transition from ADMITTED directly to COMPLETED
