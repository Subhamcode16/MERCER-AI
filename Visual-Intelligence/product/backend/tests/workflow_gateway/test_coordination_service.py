"""
Phase 14 Test Coordination Service
----------------------------------
Tests Phase 12 coordination facade and resource lease management.
"""

import pytest
from src.workflow_gateway.coordination_service import CoordinationService
from src.coordination import ResourceDescriptor

def test_coordination_facade():
    service = CoordinationService()
    admitted = service.admit_mission_to_coordination(
        mission_id="m-coord-1", priority="HIGH", requested_staff_slots=2
    )
    assert admitted is True

    res_desc = ResourceDescriptor(
        resource_id="res-slot-1",
        resource_type="STAFF_SLOT",
        capacity=5,
        scope_string="/slot",
    )
    service._coordinator.resource_registry.register_resource(res_desc)

    lease = service.request_resource_lease(
        mission_id="m-coord-1", resource_id="res-slot-1", duration_seconds=60.0
    )
    assert lease is not None
    assert lease.lease_id is not None

    released = service.release_resource_lease(lease.lease_id)
    assert released is True
