"""
Strategic Assumptions Module (Phase 30).
Exposes, tracks, validates, and detects contradictions/staleness in material strategic assumptions.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import uuid
from ..types import ThreatID, GovernanceInvariantViolation, EpistemicStatus, utc_now


class StrategicAssumption(BaseModel):
    assumption_id: str = Field(default_factory=lambda: f"asm_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    statement: str
    evidence_ids: List[str] = Field(default_factory=list)
    model_confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    empirical_confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    validation_method: str = "EMPIRICAL_TEST"
    created_at: datetime = Field(default_factory=utc_now)
    review_deadline: datetime = Field(default_factory=lambda: utc_now() + timedelta(days=30))
    status: str = "ACTIVE"  # ACTIVE, STALE, VALIDATED, CONTRADICTED, INVALIDATED
    contradiction_history: List[Dict[str, Any]] = Field(default_factory=list)
    epistemic_status: EpistemicStatus = EpistemicStatus.WORKING_ASSUMPTION

    def check_staleness(self) -> bool:
        if utc_now() > self.review_deadline and self.status == "ACTIVE":
            self.status = "STALE"
            return True
        return False

    def record_contradiction(self, evidence_id: str, contradicting_statement: str, recorded_by: str):
        # Contradictions must never be silently suppressed (T30-011)
        self.contradiction_history.append({
            "evidence_id": evidence_id,
            "statement": contradicting_statement,
            "recorded_by": recorded_by,
            "timestamp": utc_now().isoformat()
        })
        self.status = "CONTRADICTED"
        self.epistemic_status = EpistemicStatus.CONTRADICTED


class AssumptionMonitor:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._assumptions: Dict[str, StrategicAssumption] = {}

    def register_assumption(self, assumption: StrategicAssumption, actor_role: str, is_unverified_external: bool = False):
        if assumption.tenant_id != self.tenant_id:
            raise GovernanceInvariantViolation(
                ThreatID.T30_017,
                "Cross-tenant assumption insertion blocked.",
                {"assumption_tenant": assumption.tenant_id, "monitor_tenant": self.tenant_id}
            )
        # T30-008: Assumption poisoning prevention from unverified external claims
        if is_unverified_external:
            assumption.epistemic_status = EpistemicStatus.UNVERIFIED_CLAIM
            assumption.empirical_confidence = 0.1

        # T30-014: Enforce separation between model confidence and empirical confidence
        if assumption.model_confidence > 0.9 and assumption.empirical_confidence < 0.3:
            # Prevent false confidence propagation
            assumption.empirical_confidence = max(0.1, assumption.empirical_confidence)

        self._assumptions[assumption.assumption_id] = assumption

    def get_assumption(self, assumption_id: str) -> Optional[StrategicAssumption]:
        return self._assumptions.get(assumption_id)

    def list_assumptions(self) -> List[StrategicAssumption]:
        return list(self._assumptions.values())

    def scan_for_staleness_and_contradictions(self) -> Dict[str, List[StrategicAssumption]]:
        stale = []
        contradicted = []
        active = []
        for asm in self._assumptions.values():
            asm.check_staleness()
            if asm.status == "STALE":
                stale.append(asm)
            elif asm.status == "CONTRADICTED":
                contradicted.append(asm)
            elif asm.status == "ACTIVE":
                active.append(asm)
        return {
            "active": active,
            "stale": stale,
            "contradicted": contradicted
        }
