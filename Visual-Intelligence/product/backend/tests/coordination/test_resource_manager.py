"""
Unit tests for Phase 12 Resource Manager.
"""

import pytest

from src.coordination.resource_manager import ResourceManager
from src.coordination.models import ResourceRequest
from src.coordination.exceptions import ResourceUnavailable


def test_resource_manager_allocation_and_release():
    mgr = ResourceManager()
    req = ResourceRequest("req1", "m1", "staff:designer", quantity=1)

    lease = mgr.allocate(req)
    assert lease.mission_id == "m1"
    assert mgr.get_allocated_quantity("staff:designer") == 1

    mgr.release_lease(lease.lease_id)
    assert mgr.get_allocated_quantity("staff:designer") == 0


def test_resource_manager_capacity_depletion():
    mgr = ResourceManager()
    # "staff:designer" capacity is 2
    req1 = ResourceRequest("req1", "m1", "staff:designer", quantity=2)
    mgr.allocate(req1)

    # Allocating beyond capacity raises ResourceUnavailable
    req2 = ResourceRequest("req2", "m2", "staff:designer", quantity=1)
    with pytest.raises(ResourceUnavailable):
        mgr.allocate(req2)
