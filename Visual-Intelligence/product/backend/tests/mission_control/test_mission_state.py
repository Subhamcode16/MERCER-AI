"""
Unit tests for Phase 11 Mission State Machine transitions.
"""

import pytest

from src.mission_control.mission_state import MissionState, MissionStateMachine
from src.mission_control.exceptions import InvalidMissionStateError, MissionCancelledError


def test_valid_state_transitions():
    MissionStateMachine.validate_transition(MissionState.PLANNED, MissionState.READY)
    MissionStateMachine.validate_transition(MissionState.READY, MissionState.RUNNING)
    MissionStateMachine.validate_transition(MissionState.RUNNING, MissionState.PAUSED)
    MissionStateMachine.validate_transition(MissionState.PAUSED, MissionState.RUNNING)
    MissionStateMachine.validate_transition(MissionState.RUNNING, MissionState.COMPLETED)


def test_invalid_state_transitions():
    with pytest.raises(InvalidMissionStateError):
        MissionStateMachine.validate_transition(MissionState.PLANNED, MissionState.RUNNING)

    with pytest.raises(InvalidMissionStateError):
        MissionStateMachine.validate_transition(MissionState.COMPLETED, MissionState.RUNNING)


def test_cancelled_state_terminal_lock():
    with pytest.raises(MissionCancelledError):
        MissionStateMachine.validate_transition(MissionState.CANCELLED, MissionState.RUNNING)


def test_parse_state():
    assert MissionStateMachine.parse_state("RUNNING") == MissionState.RUNNING
    with pytest.raises(InvalidMissionStateError):
        MissionStateMachine.parse_state("UNKNOWN_STATE")
