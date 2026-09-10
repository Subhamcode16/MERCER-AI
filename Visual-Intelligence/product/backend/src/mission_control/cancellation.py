"""
Phase 11 Mission Cancellation Engine.

Provides idempotent cancellation management across USER, SYSTEM, SECURITY, BUDGET,
and AUTHORIZATION cancellation triggers. Permanently locks missions against restart.
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone

from .mission_models import Mission
from .mission_state import MissionState, MissionStateMachine
from .exceptions import MissionCancelledError


class CancellationReason(Enum):
    """Reason codes for mission cancellation."""
    USER_CANCEL = "USER_CANCEL"
    SYSTEM_CANCEL = "SYSTEM_CANCEL"
    SECURITY_CANCEL = "SECURITY_CANCEL"
    BUDGET_CANCEL = "BUDGET_CANCEL"
    AUTHORIZATION_CANCEL = "AUTHORIZATION_CANCEL"


@dataclass(frozen=True)
class CancellationRecord:
    """Immutable record of a mission cancellation event."""
    mission_id: str
    reason: CancellationReason
    details: str
    cancelled_at: datetime


class MissionCancellationManager:
    """Manages idempotent cancellation of missions."""

    @staticmethod
    def cancel_mission(
        mission: Mission,
        reason: CancellationReason,
        details: str = "Mission cancelled."
    ) -> CancellationRecord:
        """Idempotently cancels a mission and locks state machine."""
        current_state = MissionStateMachine.parse_state(mission.state)

        # Idempotency check: If already cancelled, return existing record
        if current_state == MissionState.CANCELLED:
            return CancellationRecord(
                mission_id=mission.mission_id,
                reason=reason,
                details=details,
                cancelled_at=mission.updated_at
            )

        # Transition to CANCELLED state
        MissionStateMachine.validate_transition(current_state, MissionState.CANCELLED)
        mission.state = MissionState.CANCELLED.value
        mission.updated_at = datetime.now(timezone.utc)

        return CancellationRecord(
            mission_id=mission.mission_id,
            reason=reason,
            details=details,
            cancelled_at=mission.updated_at
        )
