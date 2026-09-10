"""
Unit tests for Phase 13 Capability Mapping Registry (INV-13-002).
"""

import pytest

from src.execution_control.capability_models import ExecutionCapability
from src.integration_boundary.capability_mapping import CapabilityMappingRegistry
from src.integration_boundary.exceptions import CapabilityMappingError


def test_capability_mapping_success():
    reg = CapabilityMappingRegistry()
    reg.register_mapping("mock_social", "create_draft", ExecutionCapability.CREATE_DRAFT)

    cap = reg.resolve_capability("mock_social", "create_draft")
    assert cap == ExecutionCapability.CREATE_DRAFT


def test_capability_mapping_wildcard_rejection():
    reg = CapabilityMappingRegistry()

    # Rejects wildcard register attempt
    with pytest.raises(CapabilityMappingError):
        reg.register_mapping("mock_social", "*", ExecutionCapability.CREATE_DRAFT)

    with pytest.raises(CapabilityMappingError):
        reg.register_mapping("mock_social", "admin", ExecutionCapability.CREATE_DRAFT)


def test_unregistered_operation_rejection():
    reg = CapabilityMappingRegistry()
    reg.register_mapping("mock_social", "create_draft", ExecutionCapability.CREATE_DRAFT)

    with pytest.raises(CapabilityMappingError):
        reg.resolve_capability("mock_social", "delete_everything")
