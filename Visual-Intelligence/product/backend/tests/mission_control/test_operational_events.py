"""
Unit tests for Phase 11 Operational Event Telemetry.
"""

import pytest
from datetime import datetime, timezone

from src.mission_control.operational_events import OperationalEvent, OperationalEventType
from src.mission_control.exceptions import MissionControlError


def test_operational_event_structure():
    event = OperationalEvent(
        transition_id="trn_01",
        event_type=OperationalEventType.MISSION_STARTED,
        mission_id="m1",
        previous_state="PLANNED",
        new_state="RUNNING",
        reason_code="START",
        workflow_reference="wf_1",
        authorization_reference="tok_123",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    d = event.to_dict()
    assert d["event_type"] == "MISSION_STARTED"
    assert d["mission_id"] == "m1"


def test_event_secrecy_filter():
    with pytest.raises(MissionControlError):
        OperationalEvent(
            transition_id="trn_01",
            event_type=OperationalEventType.TASK_COMPLETED,
            mission_id="m1",
            previous_state="RUNNING",
            new_state="RUNNING",
            reason_code="DONE",
            workflow_reference="wf_1",
            authorization_reference="tok_123",
            timestamp=datetime.now(timezone.utc).isoformat(),
            details={"api_key": "PROHIBITED_LEAK"},
        )
