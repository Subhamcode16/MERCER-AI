"""
Tests for Strategic Operating Rooms and Cadence Engine (Phase 30).
"""
import pytest
from src.institutional_intelligence.types import (
    StrategicCadenceType,
    WorkerRole,
    ThreatID,
    GovernanceInvariantViolation,
)
from src.institutional_intelligence.operating_rooms.room import (
    OperatingRoomParticipant,
    StrategicOperatingRoom,
)
from src.institutional_intelligence.cadence.engine import (
    CadenceExecutionRecord,
    StrategicCadenceEngine,
)


def test_operating_room_lifecycle_and_participants():
    room = StrategicOperatingRoom(
        tenant_id="tenant_01",
        title="Q3 European Expansion War Room",
        strategic_objective_id="obj_euro_01"
    )
    human_part = OperatingRoomParticipant(
        participant_id="user_director",
        name="Creative Director",
        role=WorkerRole.CREATIVE_DIRECTOR_WORKER,
        is_human=True
    )
    ai_part = OperatingRoomParticipant(
        participant_id="worker_strat_ai",
        name="Strategy AI Agent",
        role=WorkerRole.STRATEGY_WORKER,
        is_human=False
    )
    room.add_participant(human_part)
    room.add_participant(ai_part)

    assert len(room.participants) == 2
    assert len(room.activity_timeline) == 2


def test_t30_019_ai_worker_cannot_execute_in_operating_room():
    room = StrategicOperatingRoom(
        tenant_id="tenant_01",
        title="Strategy Room",
        strategic_objective_id="obj_1"
    )
    ai_part = OperatingRoomParticipant(
        participant_id="worker_ai_01",
        name="AI Worker",
        role=WorkerRole.STRATEGY_WORKER,
        is_human=False
    )
    room.add_participant(ai_part)

    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        room.assert_worker_authority("worker_ai_01", attempted_action="AUTHORIZE_INITIATIVE_BUDGET")
    assert excinfo.value.threat_id == ThreatID.T30_019


def test_cadence_engine_preparation_routine():
    engine = StrategicCadenceEngine(tenant_id="tenant_01")
    record = engine.run_cadence_preparation(
        cadence_type=StrategicCadenceType.DAILY_PREPARATION,
        changes=["Competitor launched new visual collection", "Silk fabric lead times reduced 2 days"],
        contradictions=["Assumption on consumer price sensitivity challenged"],
        assumption_updates=["asm_market_pricing"]
    )
    assert record.is_preparation_only is True
    assert record.new_evidence_count == 2
    assert len(record.recommended_agenda_items) > 0


def test_t30_004_cadence_cannot_self_authorize():
    engine = StrategicCadenceEngine(tenant_id="tenant_01")
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        engine.assert_no_automated_execution_authority("cad_daily_01", attempted_action="PUBLISH_MARKET_CAMPAIGN")
    assert excinfo.value.threat_id == ThreatID.T30_004
