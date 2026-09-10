"""
Unit tests for Phase 12 Coordination Immutable Models.
"""

import pytest

from src.coordination.models import (
    ResourceDescriptor,
    ResourceRequest,
    MissionPriority,
    CoordinationBudget,
)
from src.coordination.exceptions import CoordinationPolicyViolation


def test_resource_descriptor_validation():
    rd = ResourceDescriptor("r1", "STAFF_SLOT", capacity=5, scope_string="staff:designer")
    assert rd.resource_id == "r1"
    assert rd.capacity == 5

    with pytest.raises(CoordinationPolicyViolation):
        ResourceDescriptor("", "STAFF_SLOT", capacity=5, scope_string="staff:designer")

    with pytest.raises(CoordinationPolicyViolation):
        ResourceDescriptor("r1", "STAFF_SLOT", capacity=-1, scope_string="staff:designer")

    with pytest.raises(CoordinationPolicyViolation):
        ResourceDescriptor("r1", "STAFF_SLOT", capacity=True, scope_string="staff:designer")


def test_resource_request_validation():
    req = ResourceRequest("req1", "m1", "r1", quantity=2)
    assert req.quantity == 2

    with pytest.raises(CoordinationPolicyViolation):
        ResourceRequest("req1", "m1", "r1", quantity=-5)


def test_coordination_budget_validation():
    budget = CoordinationBudget(global_max_tokens=100000)
    assert budget.global_max_tokens == 100000

    with pytest.raises(CoordinationPolicyViolation):
        CoordinationBudget(global_max_tokens=-10)
