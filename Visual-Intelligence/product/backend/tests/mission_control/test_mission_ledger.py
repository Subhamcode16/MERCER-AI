"""
Unit tests for Phase 11 Append-Only Hash-Linked Mission Ledger.
"""

import pytest
from datetime import datetime, timezone

from src.mission_control.mission_ledger import MissionLedger
from src.mission_control.operational_events import OperationalEvent, OperationalEventType


def test_mission_ledger_hash_linking(tmp_path):
    ledger = MissionLedger(base_dir=str(tmp_path))

    ev1 = OperationalEvent(
        transition_id="t1",
        event_type=OperationalEventType.MISSION_CREATED,
        mission_id="m1",
        previous_state="NONE",
        new_state="PLANNED",
        reason_code="INIT",
        workflow_reference="N/A",
        authorization_reference=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    ev2 = OperationalEvent(
        transition_id="t2",
        event_type=OperationalEventType.MISSION_STARTED,
        mission_id="m1",
        previous_state="PLANNED",
        new_state="RUNNING",
        reason_code="START",
        workflow_reference="N/A",
        authorization_reference=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    ledger.record_event(ev1)
    ledger.record_event(ev2)

    assert len(ledger.entries) == 2
    assert ledger.entries[1].previous_entry_hash == ledger.entries[0].entry_hash
    assert ledger.verify_ledger_integrity() is True
