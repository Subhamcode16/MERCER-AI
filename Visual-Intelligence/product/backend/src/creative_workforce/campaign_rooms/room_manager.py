"""
Phase 26 Campaign Room Collaboration Space Models & Manager.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


class RoomStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"


class CampaignRoomError(Exception):
    pass


@dataclass
class CampaignRoom:
    room_id: str
    tenant_id: str
    client_id: str
    campaign_id: str
    name: str
    status: RoomStatus = RoomStatus.ACTIVE
    participants: Dict[str, str] = field(default_factory=dict)  # participant_id -> role_or_type
    shared_context: Dict[str, Any] = field(default_factory=dict)
    shared_artifacts: List[Dict[str, Any]] = field(default_factory=list)
    activity_log: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CampaignRoomManager:
    """Manages multi-worker and human campaign collaboration rooms."""

    def __init__(self):
        self._rooms: Dict[str, CampaignRoom] = {}

    def create_room(
        self,
        tenant_id: str,
        client_id: str,
        campaign_id: str,
        name: str,
        initial_participants: Optional[Dict[str, str]] = None,
    ) -> CampaignRoom:
        room_id = f"room_{uuid.uuid4().hex[:12]}"
        room = CampaignRoom(
            room_id=room_id,
            tenant_id=tenant_id,
            client_id=client_id,
            campaign_id=campaign_id,
            name=name,
            participants=initial_participants or {},
        )
        self._rooms[room_id] = room
        return room

    def get_room(self, room_id: str, tenant_id: Optional[str] = None) -> Optional[CampaignRoom]:
        room = self._rooms.get(room_id)
        if not room:
            return None
        if tenant_id and room.tenant_id != tenant_id and tenant_id != "*":
            return None
        return room

    def join_room(self, room_id: str, participant_id: str, participant_type: str) -> CampaignRoom:
        room = self._rooms.get(room_id)
        if not room:
            raise CampaignRoomError(f"Room '{room_id}' not found")
        if room.status != RoomStatus.ACTIVE:
            raise CampaignRoomError(f"Cannot join room in '{room.status.value}' state")
        room.participants[participant_id] = participant_type
        return room

    def add_artifact(self, room_id: str, artifact: Dict[str, Any]) -> CampaignRoom:
        room = self._rooms.get(room_id)
        if not room:
            raise CampaignRoomError(f"Room '{room_id}' not found")
        room.shared_artifacts.append(artifact)
        return room

    def record_decision(self, room_id: str, decision: Dict[str, Any]) -> CampaignRoom:
        room = self._rooms.get(room_id)
        if not room:
            raise CampaignRoomError(f"Room '{room_id}' not found")
        room.decisions.append({
            **decision,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return room
