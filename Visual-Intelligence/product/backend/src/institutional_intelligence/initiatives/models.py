"""
Strategic Initiatives Module (Phase 30).
Links Objectives, Decisions, and authorized operational scope without granting execution authority.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import (
    StrategicHorizon,
    InitiativeHealthState,
    ThreatID,
    GovernanceInvariantViolation,
    utc_now,
)


class StrategicInitiative(BaseModel):
    initiative_id: str = Field(default_factory=lambda: f"init_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    strategic_objective_id: str
    decision_id: Optional[str] = None
    title: str
    description: str
    owner: str  # Human owner
    authorized_scope: str  # e.g., "RESEARCH_AND_DRAFT_CAMPAIGN"
    expected_outcomes: List[str] = Field(default_factory=list)
    linked_campaign_ids: List[str] = Field(default_factory=list)
    linked_experiment_ids: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)  # Initiative IDs
    risks: List[str] = Field(default_factory=list)
    health_state: InitiativeHealthState = InitiativeHealthState.HEALTHY
    horizon: StrategicHorizon = StrategicHorizon.NOW
    review_cadence_days: int = 14
    is_paused: bool = False
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    mutation_history: List[Dict[str, Any]] = Field(default_factory=list)

    def validate_dependency_chain(self, all_initiatives: Dict[str, "StrategicInitiative"]):
        # T30-024: Detect circular or invalid dependencies
        visited = set()
        stack = [self.initiative_id]
        
        def check_cycle(curr_id: str, path: List[str]):
            if curr_id in path:
                raise GovernanceInvariantViolation(
                    ThreatID.T30_024,
                    f"Circular initiative dependency detected: {' -> '.join(path + [curr_id])}",
                    {"initiative_id": curr_id, "cycle_path": path}
                )
            if curr_id not in all_initiatives:
                return
            for dep in all_initiatives[curr_id].dependencies:
                check_cycle(dep, path + [curr_id])

        for dep_id in self.dependencies:
            if dep_id == self.initiative_id:
                raise GovernanceInvariantViolation(
                    ThreatID.T30_024,
                    "Initiative cannot depend on itself.",
                    {"initiative_id": self.initiative_id}
                )
            check_cycle(dep_id, [self.initiative_id])

    def mutate_scope(self, new_scope: str, modifier_actor: str, is_automated: bool = False, rationale: str = ""):
        # T30-023: Unauthorized initiative modification prevention
        if is_automated:
            raise GovernanceInvariantViolation(
                ThreatID.T30_023,
                "Autonomous agents cannot alter the authorized scope of a strategic initiative.",
                {"initiative_id": self.initiative_id, "actor": modifier_actor}
            )
        self.mutation_history.append({
            "previous_scope": self.authorized_scope,
            "new_scope": new_scope,
            "actor": modifier_actor,
            "rationale": rationale,
            "timestamp": utc_now().isoformat()
        })
        self.authorized_scope = new_scope
        self.updated_at = utc_now()

    def pause_initiative(self, actor: str, reason: str):
        self.is_paused = True
        self.health_state = InitiativeHealthState.WATCH
        self.mutation_history.append({
            "action": "PAUSED",
            "actor": actor,
            "reason": reason,
            "timestamp": utc_now().isoformat()
        })
