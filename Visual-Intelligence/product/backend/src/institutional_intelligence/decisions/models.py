"""
Decisions Module (Phase 30).
Append-only strategic decision records with governed amendment tracking,
clear separation between Decision Quality and Outcome Quality.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import hashlib
import json
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class DecisionAlternative(BaseModel):
    alternative_id: str = Field(default_factory=lambda: f"alt_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    expected_impact: float = Field(ge=0.0, le=1.0, default=0.5)
    reversibility: float = Field(ge=0.0, le=1.0, default=0.5)
    risks: List[str] = Field(default_factory=list)


class HumanDecisionCapture(BaseModel):
    decision_maker: str
    authorization_token: str
    decided_at: datetime = Field(default_factory=utc_now)
    selected_alternative_id: str
    rejected_alternative_ids: List[str] = Field(default_factory=list)
    rationale: str
    authorization_scope: str  # e.g., "CAMPAIGN_PREPARATION_ONLY"
    expiration_date: Optional[datetime] = None
    review_cadence_days: int = 30
    signature_hash: str = ""

    def generate_signature(self, decision_id: str) -> str:
        payload = f"{decision_id}|{self.decision_maker}|{self.selected_alternative_id}|{self.authorization_scope}|{self.decided_at.isoformat()}"
        self.signature_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return self.signature_hash


class DecisionQualityAssessment(BaseModel):
    evidence_sufficiency: float = Field(ge=0.0, le=1.0, default=0.5)
    reasoning_quality: float = Field(ge=0.0, le=1.0, default=0.5)
    alternative_consideration: float = Field(ge=0.0, le=1.0, default=0.5)
    uncertainty_calibration: float = Field(ge=0.0, le=1.0, default=0.5)
    assumption_visibility: float = Field(ge=0.0, le=1.0, default=0.5)
    process_compliance: float = Field(ge=0.0, le=1.0, default=1.0)
    composite_decision_quality: float = Field(ge=0.0, le=1.0, default=0.5)


class OutcomeQualityAssessment(BaseModel):
    observed_business_result: float = Field(ge=0.0, le=1.0, default=0.5)
    campaign_result: Optional[float] = None
    experiment_result: Optional[float] = None
    objective_progress: float = Field(ge=0.0, le=1.0, default=0.5)
    evaluation_notes: str = ""
    evaluated_at: datetime = Field(default_factory=utc_now)


class StrategicDecision(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    strategic_objective_id: str
    decision_question: str
    owner: str  # Human owner
    deadline: Optional[datetime] = None
    evidence_set: List[str] = Field(default_factory=list)  # Evidence hashes or IDs
    recommendation_history: List[Dict[str, Any]] = Field(default_factory=list)
    alternatives: List[DecisionAlternative] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)  # Assumption IDs
    uncertainty: float = Field(ge=0.0, le=1.0, default=0.5)
    human_decision: Optional[HumanDecisionCapture] = None
    status: str = "DRAFT"  # DRAFT, PENDING_REVIEW, DECIDED, DEFERRED, SUPERSEDED, INVALIDATED
    expected_outcome: str = ""
    review_date: Optional[datetime] = None
    actual_outcome: Optional[str] = None
    decision_quality: Optional[DecisionQualityAssessment] = None
    outcome_quality: Optional[OutcomeQualityAssessment] = None
    created_at: datetime = Field(default_factory=utc_now)
    record_hash: str = ""
    amendments: List[Dict[str, Any]] = Field(default_factory=list)

    def calculate_record_hash(self) -> str:
        data = {
            "decision_id": self.decision_id,
            "tenant_id": self.tenant_id,
            "objective_id": self.strategic_objective_id,
            "question": self.decision_question,
            "owner": self.owner,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
        self.record_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()
        return self.record_hash

    def record_human_decision(self, capture: HumanDecisionCapture, actor: str):
        if self.status == "SUPERSEDED" or self.status == "INVALIDATED":
            # T30-006: Stale/invalidated decision resurrection prevention
            raise GovernanceInvariantViolation(
                ThreatID.T30_006,
                f"Cannot record decision on {self.status} decision record.",
                {"decision_id": self.decision_id, "status": self.status}
            )
        capture.generate_signature(self.decision_id)
        self.human_decision = capture
        self.status = "DECIDED"
        self.amendments.append({
            "action": "DECIDED",
            "actor": actor,
            "timestamp": utc_now().isoformat(),
            "signature": capture.signature_hash
        })
        self.calculate_record_hash()

    def supersede(self, new_decision_id: str, actor: str, rationale: str):
        self.status = "SUPERSEDED"
        self.amendments.append({
            "action": "SUPERSEDED",
            "superseded_by": new_decision_id,
            "actor": actor,
            "rationale": rationale,
            "timestamp": utc_now().isoformat()
        })

    def invalidate(self, actor: str, rationale: str):
        self.status = "INVALIDATED"
        self.amendments.append({
            "action": "INVALIDATED",
            "actor": actor,
            "rationale": rationale,
            "timestamp": utc_now().isoformat()
        })
