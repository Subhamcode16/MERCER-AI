"""
Strategic Operating Rooms Module (Phase 30).
Persistent collaborative operating contexts aggregating objectives, decisions, evidence, and timeline.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import ThreatID, GovernanceInvariantViolation, WorkerRole, utc_now


class OperatingRoomParticipant(BaseModel):
    participant_id: str
    name: str
    role: WorkerRole
    is_human: bool = False
    joined_at: datetime = Field(default_factory=utc_now)


class StrategicOperatingRoom(BaseModel):
    room_id: str = Field(default_factory=lambda: f"room_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    title: str
    strategic_objective_id: str
    decision_ids: List[str] = Field(default_factory=list)
    initiative_ids: List[str] = Field(default_factory=list)
    assumption_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    commitment_ids: List[str] = Field(default_factory=list)
    participants: List[OperatingRoomParticipant] = Field(default_factory=list)
    activity_timeline: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    is_active: bool = True

    def add_participant(self, participant: OperatingRoomParticipant):
        self.participants.append(participant)
        self.activity_timeline.append({
            "action": "PARTICIPANT_JOINED",
            "participant_id": participant.participant_id,
            "role": participant.role.value,
            "timestamp": utc_now().isoformat()
        })

    def log_activity(self, action: str, actor_id: str, details: Dict[str, Any]):
        self.activity_timeline.append({
            "action": action,
            "actor_id": actor_id,
            "details": details,
            "timestamp": utc_now().isoformat()
        })

    def assert_worker_authority(self, worker_id: str, attempted_action: str):
        # T30-002 / T30-019: Participation in an operating room does NOT grant decision authority
        participant = next((p for p in self.participants if p.participant_id == worker_id), None)
        if participant and not participant.is_human:
            raise GovernanceInvariantViolation(
                ThreatID.T30_019,
                f"AI worker '{worker_id}' attempted unauthorized action '{attempted_action}' in Operating Room.",
                {"worker_id": worker_id, "room_id": self.room_id, "action": attempted_action}
            )
