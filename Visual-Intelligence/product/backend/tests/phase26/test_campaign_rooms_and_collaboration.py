"""
Phase 26 Unit Tests: Campaign Rooms & Collaboration Hub.
"""
import pytest
from src.creative_workforce.campaign_rooms.room_manager import (
    CampaignRoomManager,
    RoomStatus,
    CampaignRoomError,
)
from src.creative_workforce.collaboration.collaboration_hub import (
    CollaborationHub,
    CollaborationMessage,
)


def test_campaign_room_lifecycle_and_participants():
    mgr = CampaignRoomManager()

    room = mgr.create_room(
        tenant_id="tenant_alpha",
        client_id="client_haute",
        campaign_id="C-2026-AUTUMN",
        name="Autumn Lookbook Collaboration Room",
        initial_participants={"human_director": "HUMAN", "cd_01": "WORKER"},
    )
    assert room.status == RoomStatus.ACTIVE
    assert "human_director" in room.participants
    assert "cd_01" in room.participants

    # Join another worker
    mgr.join_room(room.room_id, participant_id="visual_01", participant_type="WORKER")
    assert "visual_01" in room.participants

    # Add shared artifact
    mgr.add_artifact(room.room_id, {"artifact_id": "art_001", "type": "MOODBOARD"})
    assert len(room.shared_artifacts) == 1


def test_collaboration_hub_messages():
    mgr = CampaignRoomManager()
    room = mgr.create_room(
        tenant_id="tenant_alpha",
        client_id="client_haute",
        campaign_id="C-2026-AUTUMN",
        name="Autumn Lookbook Room",
    )

    hub = CollaborationHub(room_manager=mgr)
    msg1 = hub.post_message(
        room_id=room.room_id,
        sender_id="human_director",
        sender_type="HUMAN",
        content="Please generate three concept directions for the Milan show.",
    )
    assert msg1.sender_type == "HUMAN"

    msg2 = hub.post_message(
        room_id=room.room_id,
        sender_id="cd_01",
        sender_type="WORKER",
        content="Understood. Initiating concept synthesis with Visual DNA tokens.",
        claims=["Direction aligns with Monochrome Minimalism"],
        confidence=0.95,
    )
    assert msg2.confidence == 0.95

    messages = hub.get_room_messages(room.room_id)
    assert len(messages) == 2
