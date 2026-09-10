"""
Unit tests for Phase 11 Mission Cancellation Engine.
"""

import pytest

from src.mission_control.cancellation import MissionCancellationManager, CancellationReason
from src.mission_control.mission_models import Mission, MissionObjective, MissionConstraints, MissionBudget
from src.mission_control.exceptions import MissionCancelledError


def test_idempotent_cancellation():
    mission = Mission(
        mission_id="m1",
        objective=MissionObjective("obj1", "Title", "Desc"),
        constraints=MissionConstraints(),
        budget=MissionBudget(),
        state="RUNNING",
    )

    record1 = MissionCancellationManager.cancel_mission(mission, CancellationReason.USER_CANCEL, "User stopped")
    assert mission.state == "CANCELLED"
    assert record1.reason == CancellationReason.USER_CANCEL

    # Idempotent second cancel call succeeds without error
    record2 = MissionCancellationManager.cancel_mission(mission, CancellationReason.USER_CANCEL, "Duplicate call")
    assert record2.mission_id == "m1"
