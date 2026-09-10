"""
Phase 11 Mission State Machine.

Enforces strict mission lifecycle states and explicit transition boundaries.
Terminal states (COMPLETED, FAILED, CANCELLED) cannot be mutated or resumed.
"""

from enum import Enum, auto
from typing import Set, Dict

from .exceptions import InvalidMissionStateError, MissionCancelledError


class MissionState(Enum):
    """Enumeration of valid mission states."""
    PLANNED = "PLANNED"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    ESCALATED = "ESCALATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


# Explicit valid transition mapping
VALID_TRANSITIONS: Dict[MissionState, Set[MissionState]] = {
    MissionState.PLANNED: {MissionState.READY, MissionState.CANCELLED, MissionState.BLOCKED},
    MissionState.READY: {MissionState.RUNNING, MissionState.PAUSED, MissionState.CANCELLED, MissionState.BLOCKED},
    MissionState.RUNNING: {
        MissionState.WAITING,
        MissionState.PAUSED,
        MissionState.ESCALATED,
        MissionState.COMPLETED,
        MissionState.FAILED,
        MissionState.CANCELLED,
        MissionState.BLOCKED,
    },
    MissionState.WAITING: {
        MissionState.RUNNING,
        MissionState.PAUSED,
        MissionState.ESCALATED,
        MissionState.CANCELLED,
        MissionState.BLOCKED,
    },
    MissionState.PAUSED: {MissionState.READY, MissionState.RUNNING, MissionState.CANCELLED, MissionState.BLOCKED},
    MissionState.ESCALATED: {MissionState.READY, MissionState.RUNNING, MissionState.FAILED, MissionState.CANCELLED},
    MissionState.BLOCKED: {MissionState.ESCALATED, MissionState.CANCELLED, MissionState.PAUSED},
    MissionState.COMPLETED: set(),
    MissionState.FAILED: set(),
    MissionState.CANCELLED: set(),
}


class MissionStateMachine:
    """Manages and validates mission state transitions."""

    @staticmethod
    def validate_transition(current_state: MissionState, target_state: MissionState) -> None:
        """Validates if current_state can transition to target_state."""
        if current_state == MissionState.CANCELLED:
            raise MissionCancelledError("Cannot transition out of CANCELLED state. Cancelled missions are terminal.")

        if current_state in (MissionState.COMPLETED, MissionState.FAILED):
            raise InvalidMissionStateError(
                f"Cannot transition out of terminal state {current_state.value} to {target_state.value}."
            )

        valid_next_states = VALID_TRANSITIONS.get(current_state, set())
        if target_state not in valid_next_states:
            raise InvalidMissionStateError(
                f"Invalid mission state transition from {current_state.value} to {target_state.value}."
            )

    @staticmethod
    def parse_state(state_val: str) -> MissionState:
        """Parses string into MissionState or raises InvalidMissionStateError."""
        try:
            return MissionState(state_val)
        except ValueError:
            raise InvalidMissionStateError(f"Unknown mission state: '{state_val}'.")
