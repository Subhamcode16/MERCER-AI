"""
Tests for StaffRegistry: 7 prototype staff roles registration and lookup.
"""

from src.agentic_work import (
    StaffRegistry,
    StaffRole,
    ResearcherStaff,
    StrategistStaff,
    DesignerStaff,
    ContentSpecialistStaff,
    TrendAnalystStaff,
    CriticStaff,
    ReviewerStaff,
)


def test_staff_registry_contains_all_7_roles():
    registry = StaffRegistry()
    roles = [
        StaffRole.RESEARCHER,
        StaffRole.STRATEGIST,
        StaffRole.DESIGNER,
        StaffRole.CONTENT_SPECIALIST,
        StaffRole.TREND_ANALYST,
        StaffRole.CRITIC,
        StaffRole.REVIEWER,
    ]
    for role in roles:
        worker = registry.get_staff_by_role(role)
        assert worker is not None
        assert worker.role == role


def test_staff_list():
    registry = StaffRegistry()
    workers = registry.list_staff()
    assert len(workers) == 7
