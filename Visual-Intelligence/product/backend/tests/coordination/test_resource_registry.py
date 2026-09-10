"""
Unit tests for Phase 12 Resource Registry.
"""

import pytest

from src.coordination.resource_registry import ResourceRegistry
from src.coordination.models import ResourceDescriptor
from src.coordination.exceptions import CoordinationPolicyViolation


def test_resource_registry_defaults():
    reg = ResourceRegistry()

    r = reg.get_resource("staff:designer")
    assert r.capacity == 2

    resources = reg.list_resources()
    assert len(resources) >= 7


def test_resource_registry_custom_registration():
    reg = ResourceRegistry()
    desc = ResourceDescriptor("r_custom", "CUSTOM_TYPE", capacity=10, scope_string="scope:custom")
    reg.register_resource(desc)

    assert reg.get_resource("r_custom").capacity == 10

    with pytest.raises(CoordinationPolicyViolation):
        reg.register_resource(desc)  # Duplicate
