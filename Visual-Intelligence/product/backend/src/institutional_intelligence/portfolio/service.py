"""
Decision Portfolio Service (Phase 30).
Maintains the portfolio of strategic decisions and prioritizes institutional attention.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta
import math
from ..decisions.models import StrategicDecision
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class DecisionAttentionScore(BaseModel):
    decision_id: str
    strategic_impact: float = Field(ge=0.0, le=1.0, default=0.5)
    urgency: float = Field(ge=0.0, le=1.0, default=0.5)
    evidence_change: float = Field(ge=0.0, le=1.0, default=0.5)
    uncertainty: float = Field(ge=0.0, le=1.0, default=0.5)
    dependency_risk: float = Field(ge=0.0, le=1.0, default=0.5)
    reversibility_factor: float = Field(ge=0.0, le=1.0, default=0.5)  # 1 - reversibility (irreversible = higher attention)
    attention_score: float = 0.0
    attention_reasons: List[str] = Field(default_factory=list)

    def calculate(self) -> float:
        # Score = Impact * Urgency * EvidenceChange * Uncertainty * DependencyRisk * (1 + ReversibilityFactor)
        # Scaled to 0.0 - 100.0
        base = (
            self.strategic_impact *
            (self.urgency + 0.1) *
            (self.evidence_change + 0.1) *
            (self.uncertainty + 0.1) *
            (self.dependency_risk + 0.1) *
            (self.reversibility_factor + 0.5)
        )
        self.attention_score = round(min(100.0, base * 100.0), 2)
        return self.attention_score


class DecisionPortfolioService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._decisions: Dict[str, StrategicDecision] = {}

    def add_decision(self, decision: StrategicDecision):
        if decision.tenant_id != self.tenant_id:
            raise GovernanceInvariantViolation(
                ThreatID.T30_017,
                "Cross-tenant decision insertion blocked.",
                {"decision_tenant": decision.tenant_id, "service_tenant": self.tenant_id}
            )
        self._decisions[decision.decision_id] = decision

    def get_decision(self, decision_id: str) -> Optional[StrategicDecision]:
        return self._decisions.get(decision_id)

    def list_decisions(self) -> List[StrategicDecision]:
        return list(self._decisions.values())

    def evaluate_attention(
        self,
        decision_id: str,
        strategic_impact: float = 0.5,
        evidence_change: float = 0.2,
        dependency_risk: float = 0.3,
        reversibility: float = 0.5
    ) -> DecisionAttentionScore:
        decision = self._decisions.get(decision_id)
        if not decision:
            raise ValueError(f"Decision {decision_id} not found.")

        # Compute urgency based on deadline
        urgency = 0.5
        reasons = []
        now = utc_now()
        if decision.deadline:
            days_left = (decision.deadline - now).total_seconds() / 86400.0
            if days_left <= 0:
                urgency = 1.0
                reasons.append("Deadline is overdue.")
            elif days_left < 3:
                urgency = 0.9
                reasons.append(f"Deadline approaching in {days_left:.1f} days.")
            elif days_left < 7:
                urgency = 0.7
                reasons.append("Deadline approaching within a week.")
            else:
                urgency = 0.3

        if len(decision.evidence_set) == 0:
            evidence_change = max(evidence_change, 0.8)
            reasons.append("Decision lacks empirical evidence basis.")

        if decision.uncertainty > 0.7:
            reasons.append(f"High decision uncertainty ({decision.uncertainty}).")

        score = DecisionAttentionScore(
            decision_id=decision_id,
            strategic_impact=strategic_impact,
            urgency=urgency,
            evidence_change=evidence_change,
            uncertainty=decision.uncertainty,
            dependency_risk=dependency_risk,
            reversibility_factor=round(1.0 - reversibility, 2),
            attention_reasons=reasons
        )
        score.calculate()
        return score

    def rank_attention_queue(self) -> List[DecisionAttentionScore]:
        scores = []
        for d_id in self._decisions:
            d = self._decisions[d_id]
            if d.status not in ["SUPERSEDED", "INVALIDATED"]:
                score = self.evaluate_attention(d_id)
                scores.append(score)
        scores.sort(key=lambda s: s.attention_score, reverse=True)
        return scores

    def assert_budget_boundary(self, actor: str, requested_budget: float):
        # T30-005 / T30-031: Ranking or portfolio status does not grant budget authority
        raise GovernanceInvariantViolation(
            ThreatID.T30_005,
            "Portfolio ranking cannot grant financial or resource budget authority.",
            {"actor": actor, "requested_budget": requested_budget}
        )
