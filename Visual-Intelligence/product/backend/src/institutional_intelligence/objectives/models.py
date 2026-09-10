"""
Strategic Objectives Module (Phase 30).
Human-defined strategic outcomes with explicit authority bounds.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import StrategicHorizon, ThreatID, GovernanceInvariantViolation, utc_now


class StrategicObjective(BaseModel):
    objective_id: str = Field(default_factory=lambda: f"obj_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    owner: str  # Must be a verified human actor ID
    creation_authority: str  # Human authorization token or role verification
    title: str
    description: str
    scope: str
    success_criteria: List[str] = Field(default_factory=list)
    time_horizon: StrategicHorizon = StrategicHorizon.NOW
    priority: int = Field(ge=1, le=10, default=5)
    status: str = "ACTIVE"  # ACTIVE, PAUSED, ACHIEVED, SUPERSEDED, ABANDONED
    evidence_basis: List[str] = Field(default_factory=list)
    review_cadence_days: int = 30
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    revision_history: List[Dict[str, Any]] = Field(default_factory=list)
    is_human_authorized: bool = True

    def validate_human_authority(self, actor: str, is_automated_agent: bool = False):
        if is_automated_agent:
            raise GovernanceInvariantViolation(
                ThreatID.T30_001,
                "Strategic objectives cannot be created or mutated by automated models or agents alone.",
                {"actor": actor, "objective_id": self.objective_id}
            )
        if not self.owner or not self.creation_authority:
            raise GovernanceInvariantViolation(
                ThreatID.T30_001,
                "Strategic objective must have an explicit human owner and creation authority.",
                {"objective_id": self.objective_id}
            )

    def mutate_scope(self, new_scope: str, modifier_actor: str, is_automated_agent: bool = False, rationale: str = ""):
        if is_automated_agent:
            raise GovernanceInvariantViolation(
                ThreatID.T30_001,
                "Unauthorized objective mutation attempted by autonomous agent.",
                {"modifier": modifier_actor, "objective_id": self.objective_id}
            )
        self.revision_history.append({
            "timestamp": utc_now().isoformat(),
            "previous_scope": self.scope,
            "new_scope": new_scope,
            "modified_by": modifier_actor,
            "rationale": rationale
        })
        self.scope = new_scope
        self.updated_at = utc_now()
