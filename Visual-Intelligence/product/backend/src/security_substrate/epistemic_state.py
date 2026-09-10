"""
Canonical Epistemic State Machine definitions and transition matrix for Security Substrate.
"""

from enum import Enum
from typing import Set, Dict
from .exceptions import InvalidStateTransitionException


class EpistemicState(str, Enum):
    """
    Monotonic epistemic states governed by AssuranceLoopController.
    """
    UNKNOWN = "UNKNOWN"
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    STALE = "STALE"
    REASSESSMENT_REQUIRED = "REASSESSMENT_REQUIRED"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
    BLOCKED = "BLOCKED"


# Explicit Canonical State-Transition Matrix
PERMITTED_TRANSITIONS: Dict[EpistemicState, Set[EpistemicState]] = {
    EpistemicState.UNKNOWN: {
        EpistemicState.UNVERIFIED,
        EpistemicState.RECOVERY_REQUIRED,
        EpistemicState.BLOCKED,
    },
    EpistemicState.UNVERIFIED: {
        EpistemicState.VERIFIED,
        EpistemicState.BLOCKED,
        EpistemicState.RECOVERY_REQUIRED,
    },
    EpistemicState.VERIFIED: {
        EpistemicState.STALE,
        EpistemicState.REASSESSMENT_REQUIRED,
        EpistemicState.BLOCKED,
        EpistemicState.RECOVERY_REQUIRED,
    },
    EpistemicState.STALE: {
        EpistemicState.UNVERIFIED,
        EpistemicState.BLOCKED,
        EpistemicState.RECOVERY_REQUIRED,
    },
    EpistemicState.REASSESSMENT_REQUIRED: {
        EpistemicState.UNVERIFIED,
        EpistemicState.BLOCKED,
        EpistemicState.RECOVERY_REQUIRED,
    },
    EpistemicState.RECOVERY_REQUIRED: {
        EpistemicState.UNKNOWN,  # Recovery MUST reset to UNKNOWN only
        EpistemicState.BLOCKED,
    },
    EpistemicState.BLOCKED: set(),  # Terminal state
}


def validate_transition(current_state: EpistemicState, target_state: EpistemicState) -> bool:
    """
    Validates whether a transition from current_state to target_state is permitted.

    Raises:
        InvalidStateTransitionException: If the transition violates the canonical matrix.
    """
    if not isinstance(current_state, EpistemicState) or not isinstance(target_state, EpistemicState):
        raise InvalidStateTransitionException(
            f"Invalid state types: current={type(current_state)}, target={type(target_state)}"
        )

    # Hard-coded explicit forbidden checks
    if target_state == EpistemicState.VERIFIED:
        if current_state in (EpistemicState.UNKNOWN, EpistemicState.RECOVERY_REQUIRED, EpistemicState.BLOCKED):
            raise InvalidStateTransitionException(
                f"Forbidden direct transition to VERIFIED from {current_state.value}"
            )

    permitted = PERMITTED_TRANSITIONS.get(current_state, set())
    if target_state not in permitted:
        raise InvalidStateTransitionException(
            f"State transition from {current_state.value} to {target_state.value} is FORBIDDEN by canonical matrix."
        )

    return True
