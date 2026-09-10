"""
Phase 14 Test Staff Registry
-----------------------------
Tests canonical 5-department staff registry populating and querying.
"""

import pytest
from src.creative_workforce import StaffRegistry, Department, Role, StaffNotFoundError

def test_staff_registry_bootstrap():
    registry = StaffRegistry()
    all_staff = registry.list_all()
    assert len(all_staff) >= 13

    strategy_staff = registry.list_by_department(Department.STRATEGY)
    assert len(strategy_staff) >= 3

    creative_staff = registry.list_by_department(Department.CREATIVE)
    assert len(creative_staff) >= 4

    quality_staff = registry.list_by_department(Department.QUALITY)
    assert len(quality_staff) >= 2

def test_staff_lookup_by_role():
    registry = StaffRegistry()
    designers = registry.list_by_role(Role.VISUAL_DESIGNER)
    assert len(designers) == 1
    assert designers[0].staff_id == "visual_designer_01"

def test_missing_staff_rejection():
    registry = StaffRegistry()
    with pytest.raises(StaffNotFoundError):
        registry.get_staff("non-existent-id")
