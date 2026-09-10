"""
Strategic Horizons Module (Phase 30).
Maps institutional objectives and initiatives across explicit time horizons:
NOW, NEXT, LATER, FUTURE, UNKNOWN.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import StrategicHorizon, ThreatID, GovernanceInvariantViolation, utc_now


class StrategicHorizonMapping(BaseModel):
    mapping_id: str = Field(default_factory=lambda: f"horiz_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    target_id: str  # objective_id or initiative_id
    target_type: str  # "OBJECTIVE", "INITIATIVE", "DECISION"
    horizon: StrategicHorizon = StrategicHorizon.NOW
    rationale: str = ""
    assigned_by: str  # Human actor
    assigned_at: datetime = Field(default_factory=utc_now)
    transition_history: List[Dict[str, Any]] = Field(default_factory=list)

    def transition_horizon(self, new_horizon: StrategicHorizon, actor: str, is_automated: bool = False, rationale: str = ""):
        if is_automated and self.horizon == StrategicHorizon.UNKNOWN and new_horizon != StrategicHorizon.UNKNOWN:
            # T30-012: Unknown state collapse prevention
            raise GovernanceInvariantViolation(
                ThreatID.T30_012,
                "Automated processes cannot collapse an UNKNOWN horizon into an active horizon without human verification.",
                {"mapping_id": self.mapping_id, "attempted_horizon": new_horizon.value}
            )
        self.transition_history.append({
            "from_horizon": self.horizon.value,
            "to_horizon": new_horizon.value,
            "actor": actor,
            "is_automated": is_automated,
            "timestamp": utc_now().isoformat(),
            "rationale": rationale
        })
        self.horizon = new_horizon


class HorizonPortfolioView(BaseModel):
    tenant_id: str
    now: List[str] = Field(default_factory=list)
    next: List[str] = Field(default_factory=list)
    later: List[str] = Field(default_factory=list)
    future: List[str] = Field(default_factory=list)
    unknown: List[str] = Field(default_factory=list)

    def add_item(self, item_id: str, horizon: StrategicHorizon):
        if horizon == StrategicHorizon.NOW:
            self.now.append(item_id)
        elif horizon == StrategicHorizon.NEXT:
            self.next.append(item_id)
        elif horizon == StrategicHorizon.LATER:
            self.later.append(item_id)
        elif horizon == StrategicHorizon.FUTURE:
            self.future.append(item_id)
        elif horizon == StrategicHorizon.UNKNOWN:
            self.unknown.append(item_id)
