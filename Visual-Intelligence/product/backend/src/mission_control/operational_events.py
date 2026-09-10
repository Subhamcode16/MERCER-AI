"""
Phase 11 Operational Event Telemetry.

Implements INV-11-010: Generates structured, immutable, non-sensitive operational
telemetry records for every mission state transition and task lifecycle event.
"""

from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from .exceptions import MissionControlError


class OperationalEventType(Enum):
    """Enumeration of operational event types."""
    MISSION_CREATED = "MISSION_CREATED"
    MISSION_STARTED = "MISSION_STARTED"
    TASK_STARTED = "TASK_STARTED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_FAILED = "TASK_FAILED"
    TASK_RETRIED = "TASK_RETRIED"
    EXECUTION_REQUESTED = "EXECUTION_REQUESTED"
    EXECUTION_AUTHORIZED = "EXECUTION_AUTHORIZED"
    EXECUTION_DENIED = "EXECUTION_DENIED"
    MISSION_PAUSED = "MISSION_PAUSED"
    MISSION_ESCALATED = "MISSION_ESCALATED"
    MISSION_RESUMED = "MISSION_RESUMED"
    MISSION_COMPLETED = "MISSION_COMPLETED"
    MISSION_FAILED = "MISSION_FAILED"
    MISSION_CANCELLED = "MISSION_CANCELLED"


@dataclass(frozen=True)
class OperationalEvent:
    """Structured telemetry record matching INV-11-010 schema requirements."""
    transition_id: str
    event_type: OperationalEventType
    mission_id: str
    previous_state: str
    new_state: str
    reason_code: str
    workflow_reference: str
    authorization_reference: Optional[str]
    timestamp: str
    policy_version: str = "v1.0"
    details: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        # Guarantee secrecy check: Prevent logging credentials or private keys in details
        if self.details:
            s_details = str(self.details).lower()
            for key in ("api_key", "secret", "password", "token", "private_key"):
                if key in s_details:
                    raise MissionControlError(f"Operational event details contain prohibited secret field '{key}'.")

    def to_dict(self) -> Dict[str, Any]:
        """Converts event object to serializable dictionary."""
        d = asdict(self)
        d["event_type"] = self.event_type.value
        return d
