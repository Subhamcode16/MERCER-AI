"""
Unit tests for Phase 11 Hierarchical Mission Budget Tracker.
"""

import pytest

from src.mission_control.budget import MissionBudgetTracker
from src.mission_control.mission_models import MissionBudget
from src.mission_control.exceptions import MissionBudgetExceededError


def test_budget_token_exhaustion():
    tracker = MissionBudgetTracker(MissionBudget(token_budget=1000))
    tracker.record_tokens(500)
    assert tracker.usage.tokens_consumed == 500

    with pytest.raises(MissionBudgetExceededError):
        tracker.record_tokens(600)


def test_budget_execution_count_exhaustion():
    tracker = MissionBudgetTracker(MissionBudget(max_executions=2))
    tracker.record_execution()
    tracker.record_execution()

    with pytest.raises(MissionBudgetExceededError):
        tracker.record_execution()
