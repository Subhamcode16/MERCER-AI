"""
Phase 26 Workforce Collaboration Hub.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from src.creative_workforce.campaign_rooms.room_manager import CampaignRoomManager, CampaignRoom


@dataclass
class CollaborationMessage:
    message_id: str
    room_id: str
    sender_id: str
    sender_type: str  # "WORKER" or "HUMAN"
    content: str
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    claims: List[str] = field(default_factory=list)
    confidence: float = 1.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CollaborationHub:
    """Orchestrates turn-taking, messaging, and multi-worker deliberation in campaign rooms."""

    def __init__(self, room_manager: CampaignRoomManager):
        self.room_manager = room_manager
        self._messages: Dict[str, List[CollaborationMessage]] = {}  # room_id -> messages

    def post_message(
        self,
        room_id: str,
        sender_id: str,
        sender_type: str,
        content: str,
        artifacts: Optional[List[Dict[str, Any]]] = None,
        claims: Optional[List[str]] = None,
        confidence: float = 1.0,
    ) -> CollaborationMessage:
        room = self.room_manager.get_room(room_id)
        if not room:
            raise KeyError(f"Room '{room_id}' not found")
        
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        msg = CollaborationMessage(
            message_id=msg_id,
            room_id=room_id,
            sender_id=sender_id,
            sender_type=sender_type,
            content=content,
            artifacts=artifacts or [],
            claims=claims or [],
            confidence=confidence,
        )
        if room_id not in self._messages:
            self._messages[room_id] = []
        self._messages[room_id].append(msg)
        return msg

    def get_room_messages(self, room_id: str) -> List[CollaborationMessage]:
        return self._messages.get(room_id, [])
