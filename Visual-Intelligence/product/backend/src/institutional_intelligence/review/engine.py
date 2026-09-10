"""
Strategic Review Engine (Phase 30).
Synthesizes the 12 canonical strategic review questions into explainable Strategic Briefs.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import hashlib
import json
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class StrategicBrief(BaseModel):
    brief_id: str = Field(default_factory=lambda: f"brf_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    title: str
    created_at: datetime = Field(default_factory=utc_now)
    q1_what_changed: List[str] = Field(default_factory=list)
    q2_what_matters: List[str] = Field(default_factory=list)
    q3_what_became_uncertain: List[str] = Field(default_factory=list)
    q4_what_contradicted_assumptions: List[str] = Field(default_factory=list)
    q5_decisions_needing_attention: List[str] = Field(default_factory=list)
    q6_initiatives_changed: List[str] = Field(default_factory=list)
    q7_opportunities_emerged: List[str] = Field(default_factory=list)
    q8_risks_increased: List[str] = Field(default_factory=list)
    q9_assumptions_expired: List[str] = Field(default_factory=list)
    q10_scenarios_changed: List[str] = Field(default_factory=list)
    q11_human_considerations_next: List[str] = Field(default_factory=list)
    q12_what_remains_unknown: List[str] = Field(default_factory=list)
    evidence_provenance: List[str] = Field(default_factory=list)
    recommendation_summary: str = ""
    is_withdrawn: bool = False
    brief_hash: str = ""

    def calculate_hash(self) -> str:
        payload = {
            "brief_id": self.brief_id,
            "tenant_id": self.tenant_id,
            "title": self.title,
            "recommendation": self.recommendation_summary,
            "created_at": self.created_at.isoformat()
        }
        self.brief_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        return self.brief_hash

    def withdraw(self, actor: str, reason: str):
        # T30-032: Recommendation & Strategic Brief withdrawal
        self.is_withdrawn = True


class StrategicReviewEngine:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def generate_review(
        self,
        title: str,
        changes: List[str],
        material_points: List[str],
        uncertainties: List[str],
        contradictions: List[str],
        attention_decisions: List[str],
        initiative_updates: List[str],
        opportunities: List[str],
        risks: List[str],
        expired_assumptions: List[str],
        scenarios: List[str],
        human_actions: List[str],
        unknowns: List[str],
        evidence_provenance: List[str],
        recommendation: str
    ) -> StrategicBrief:
        brief = StrategicBrief(
            tenant_id=self.tenant_id,
            title=title,
            q1_what_changed=changes,
            q2_what_matters=material_points,
            q3_what_became_uncertain=uncertainties,
            q4_what_contradicted_assumptions=contradictions,
            q5_decisions_needing_attention=attention_decisions,
            q6_initiatives_changed=initiative_updates,
            q7_opportunities_emerged=opportunities,
            q8_risks_increased=risks,
            q9_assumptions_expired=expired_assumptions,
            q10_scenarios_changed=scenarios,
            q11_human_considerations_next=human_actions,
            q12_what_remains_unknown=unknowns or ["Market macro shift impact undetermined."],
            evidence_provenance=evidence_provenance,
            recommendation_summary=recommendation
        )
        brief.calculate_hash()
        return brief
