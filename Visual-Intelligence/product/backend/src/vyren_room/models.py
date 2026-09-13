"""
Domain Models for VYREN Room.
Encapsulates conversation, inline interactive artifacts, decisions, approvals, and work streams.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import time
import uuid


class RoomParticipant(BaseModel):
    id: str
    name: str
    role: str
    is_human: bool = False
    avatar: Optional[str] = None


class RoomArtifact(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"art-{uuid.uuid4().hex[:8]}")
    artifact_type: str  # BRAND_UNDERSTANDING, RESEARCH, CREATIVE_DIRECTION, MOODBOARD, APPROVAL_REQUEST, OUTCOME_REPORT
    title: str
    summary: str
    data: Dict[str, Any] = Field(default_factory=dict)
    provenance_hash: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    status: str = "READY"  # READY, AWAITING_APPROVAL, APPROVED, REJECTED


class RoomDecision(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"dec-{uuid.uuid4().hex[:8]}")
    title: str
    context: str
    options: List[Dict[str, Any]] = Field(default_factory=list)
    chosen_option_id: Optional[str] = None
    decided_by: Optional[str] = None
    timestamp: Optional[float] = None
    status: str = "PENDING"  # PENDING, CONFIRMED, REJECTED


class RoomApproval(BaseModel):
    approval_id: str = Field(default_factory=lambda: f"appr-{uuid.uuid4().hex[:8]}")
    title: str
    target_artifact_id: str
    required_authority: str = "creative_director"
    approved_by: Optional[str] = None
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED
    timestamp: Optional[float] = None


class RoomWorkEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"work-{uuid.uuid4().hex[:8]}")
    step: str
    status: str  # PENDING, ACTIVE, DONE, BLOCKED
    timestamp: float = Field(default_factory=time.time)


class RoomMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"msg-{uuid.uuid4().hex[:8]}")
    sender_id: str
    sender_name: str
    sender_role: str
    is_human: bool = False
    content: str
    artifacts: List[RoomArtifact] = Field(default_factory=list)
    decisions: List[RoomDecision] = Field(default_factory=list)
    work_events: List[RoomWorkEvent] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)


class Room(BaseModel):
    room_id: str = Field(default_factory=lambda: f"room-{uuid.uuid4().hex[:8]}")
    tenant_id: str
    title: str
    campaign_id: Optional[str] = None
    participants: List[RoomParticipant] = Field(default_factory=list)
    messages: List[RoomMessage] = Field(default_factory=list)
    artifacts: List[RoomArtifact] = Field(default_factory=list)
    active_work_progress: List[RoomWorkEvent] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
