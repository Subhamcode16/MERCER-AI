"""
Phase 10 — Resource Scope Unit Tests
"""

import pytest
from src.execution_control.exceptions import ResourceScopeViolationError
from src.execution_control.resource_scope import ResourceScope


def test_resource_scope_matching():
    parent_scope = ResourceScope("brand:aura/campaign:fall2026")
    exact_child = ResourceScope("brand:aura/campaign:fall2026")
    asset_child = ResourceScope("brand:aura/campaign:fall2026/asset:01")
    different_brand = ResourceScope("brand:other/campaign:fall2026")

    assert parent_scope.matches(exact_child) is True
    assert parent_scope.matches(asset_child) is True
    assert parent_scope.matches(different_brand) is False


def test_resource_scope_boundary_validation():
    parent_scope = ResourceScope("brand:aura")
    other_scope = ResourceScope("brand:lumina")

    # Matching boundary passes
    parent_scope.validate_boundary(ResourceScope("brand:aura/asset:99"))

    # Differing boundary raises ResourceScopeViolationError
    with pytest.raises(ResourceScopeViolationError):
        parent_scope.validate_boundary(other_scope)
