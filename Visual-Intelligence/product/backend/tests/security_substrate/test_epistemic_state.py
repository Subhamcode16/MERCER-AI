"""
Unit tests for EpistemicState enum and canonical transition matrix.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from security_substrate.epistemic_state import (
    EpistemicState,
    validate_transition,
    PERMITTED_TRANSITIONS,
)
from security_substrate.exceptions import InvalidStateTransitionException


def test_epistemic_state_enum_values():
    """Verify all 7 canonical epistemic states exist."""
    states = {s.value for s in EpistemicState}
    expected = {
        "UNKNOWN",
        "UNVERIFIED",
        "VERIFIED",
        "STALE",
        "REASSESSMENT_REQUIRED",
        "RECOVERY_REQUIRED",
        "BLOCKED",
    }
    assert states == expected


def test_permitted_transitions_matrix():
    """Verify all 12 permitted state transitions validate successfully."""
    permitted_pairs = [
        (EpistemicState.UNKNOWN, EpistemicState.UNVERIFIED),
        (EpistemicState.UNKNOWN, EpistemicState.RECOVERY_REQUIRED),
        (EpistemicState.UNKNOWN, EpistemicState.BLOCKED),
        (EpistemicState.UNVERIFIED, EpistemicState.VERIFIED),
        (EpistemicState.UNVERIFIED, EpistemicState.BLOCKED),
        (EpistemicState.UNVERIFIED, EpistemicState.RECOVERY_REQUIRED),
        (EpistemicState.VERIFIED, EpistemicState.STALE),
        (EpistemicState.VERIFIED, EpistemicState.REASSESSMENT_REQUIRED),
        (EpistemicState.VERIFIED, EpistemicState.BLOCKED),
        (EpistemicState.VERIFIED, EpistemicState.RECOVERY_REQUIRED),
        (EpistemicState.STALE, EpistemicState.UNVERIFIED),
        (EpistemicState.STALE, EpistemicState.BLOCKED),
        (EpistemicState.STALE, EpistemicState.RECOVERY_REQUIRED),
        (EpistemicState.REASSESSMENT_REQUIRED, EpistemicState.UNVERIFIED),
        (EpistemicState.REASSESSMENT_REQUIRED, EpistemicState.BLOCKED),
        (EpistemicState.REASSESSMENT_REQUIRED, EpistemicState.RECOVERY_REQUIRED),
        (EpistemicState.RECOVERY_REQUIRED, EpistemicState.UNKNOWN),
        (EpistemicState.RECOVERY_REQUIRED, EpistemicState.BLOCKED),
    ]

    for current, target in permitted_pairs:
        assert validate_transition(current, target) is True


def test_forbidden_direct_to_verified_transitions():
    """Verify forbidden direct transitions to VERIFIED raise InvalidStateTransitionException."""
    forbidden_to_verified = [
        EpistemicState.UNKNOWN,
        EpistemicState.RECOVERY_REQUIRED,
        EpistemicState.BLOCKED,
        EpistemicState.STALE,
        EpistemicState.REASSESSMENT_REQUIRED,
    ]

    for state in forbidden_to_verified:
        with pytest.raises(InvalidStateTransitionException):
            validate_transition(state, EpistemicState.VERIFIED)


def test_forbidden_blocked_transitions():
    """Verify BLOCKED is a terminal state that permits zero transitions."""
    for state in EpistemicState:
        with pytest.raises(InvalidStateTransitionException):
            validate_transition(EpistemicState.BLOCKED, state)


def test_invalid_state_types():
    """Verify non-enum types raise InvalidStateTransitionException."""
    with pytest.raises(InvalidStateTransitionException):
        validate_transition("UNKNOWN", EpistemicState.UNVERIFIED)
