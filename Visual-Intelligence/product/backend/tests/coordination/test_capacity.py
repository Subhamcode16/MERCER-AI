"""
Unit tests for Phase 12 Global Capacity & Budget Tracker.
"""

import pytest

from src.coordination.capacity import CapacityTracker
from src.coordination.models import CoordinationBudget
from src.coordination.exceptions import CoordinationBudgetExceeded


def test_capacity_token_exhaustion():
    tracker = CapacityTracker(CoordinationBudget(global_max_tokens=1000))
    tracker.record_token_consumption(500)
    assert tracker.consumed_tokens == 500

    with pytest.raises(CoordinationBudgetExceeded):
        tracker.record_token_consumption(600)


def test_capacity_staff_slot_exhaustion():
    tracker = CapacityTracker(CoordinationBudget(global_max_concurrent_staff_tasks=2))
    tracker.acquire_staff_slot()
    tracker.acquire_staff_slot()

    with pytest.raises(CoordinationBudgetExceeded):
        tracker.acquire_staff_slot()

    tracker.release_staff_slot()
    tracker.acquire_staff_slot()  # Succeeds after slot release
