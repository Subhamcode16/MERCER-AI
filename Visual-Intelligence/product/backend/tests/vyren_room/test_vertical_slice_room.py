"""
❖ Vertical Slice 1 End-to-End Integration Test.
Validates: User Brief → Orchestrator → Intelligence Worker → research.search Tool → Evidence → Artifacts → Human Confirmation.
"""

import pytest
from src.agent_runtime.openai.openai_runtime_adapter import OpenAIAgentRuntimeAdapter
from src.vyren_room.room_service import RoomService
from src.orchestrator.vyren_orchestrator import VyrenOrchestrator


@pytest.mark.asyncio
async def test_vertical_slice_room_collaboration():
    """Validates complete Vertical Slice 1 lifecycle."""
    runtime = OpenAIAgentRuntimeAdapter()
    room_service = RoomService()
    orchestrator = VyrenOrchestrator(runtime=runtime, room_service=room_service)

    tenant_id = "tenant_luxury_bridal_01"
    room = room_service.create_room(
        tenant_id=tenant_id,
        title="Autumn/Winter 2026: The Modern Sovereign Creative Room"
    )

    # 1. User submits launch prompt
    user_prompt = "Create a campaign for our luxury bridal collection targeting younger high-intent buyers."
    vyren_msg = await orchestrator.process_user_turn(
        room_id=room.room_id,
        tenant_id=tenant_id,
        user_prompt=user_prompt,
        user_name="Elena Vance"
    )

    # 2. Verify Room Message and Sender
    assert vyren_msg.sender_id == "vyren_core"
    assert vyren_msg.sender_name == "VYREN"
    assert "bridal" in vyren_msg.content.lower()

    # 3. Verify Generated In-Room Artifacts
    assert len(vyren_msg.artifacts) == 2
    
    # Artifact 1: Research Evidence
    res_artifact = next(a for a in vyren_msg.artifacts if a.artifact_type == "RESEARCH")
    assert "Luxury Bridal" in res_artifact.title
    assert res_artifact.data["epistemic_status"] == "OBSERVED"

    # Artifact 2: Creative Directions
    dir_artifact = next(a for a in vyren_msg.artifacts if a.artifact_type == "CREATIVE_DIRECTION")
    assert "Modern Sovereign" in dir_artifact.title
    assert "territory_a" in dir_artifact.data

    # 4. Verify Human Decision Gate Presence
    assert len(vyren_msg.decisions) == 1
    decision = vyren_msg.decisions[0]
    assert decision.status == "PENDING"
    assert len(decision.options) == 2

    # 5. Human Decision Recorded
    confirmed_decision = room_service.record_decision(
        room_id=room.room_id,
        tenant_id=tenant_id,
        decision_id=decision.decision_id,
        chosen_option_id="opt-01",
        decided_by="Elena Vance"
    )

    assert confirmed_decision.status == "CONFIRMED"
    assert confirmed_decision.chosen_option_id == "opt-01"
    assert confirmed_decision.decided_by == "Elena Vance"

    # 6. Verify Full Room State Persistence
    stored_room = room_service.get_room(room.room_id, tenant_id)
    assert len(stored_room.messages) == 2  # User msg + VYREN msg
    assert len(stored_room.artifacts) == 2
