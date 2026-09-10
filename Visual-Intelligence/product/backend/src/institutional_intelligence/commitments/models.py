"""
Strategic Commitments Module (Phase 30).
Human-approved organizational commitments, milestones, and expiration conditions.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class StrategicCommitment(BaseModel):
    commitment_id: str = Field(default_factory=lambda: f"cmt_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    owner: str  # Human owner
    title: str
    description: str
    target_date: datetime
    expiration_date: datetime
    status: str = "ACTIVE"  # ACTIVE, FULFILLED, EXPIRED, CANCELLED, AT_RISK
    linked_initiative_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    approved_by: str
    review_condition: str

    def check_expiration(self) -> bool:
        if utc_now() > self.expiration_date and self.status == "ACTIVE":
            self.status = "EXPIRED"
            return True
        return False
