"""
Phase 28 Learning Hypothesis Store.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class HypothesisScope(str, Enum):
    GLOBAL = "GLOBAL"
    DOMAIN = "DOMAIN"
    CLIENT = "CLIENT"
    BRAND = "BRAND"
    CAMPAIGN = "CAMPAIGN"


@dataclass
class LearningHypothesis:
    hypothesis_id: str
    statement: str
    originating_campaigns: List[str]
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    scope: HypothesisScope
    confidence: float
    known_limitations: List[str]
    test_recommendation: str
    status: str = "PROVISIONAL"  # PROVISIONAL, VALIDATED, REFUTED, PROMOTED


class LearningHypothesisStore:
    """Stores and evaluates structured learning hypotheses with explicit supporting and contradicting evidence."""

    def __init__(self):
        self._hypotheses: Dict[str, LearningHypothesis] = {}

    def create_hypothesis(
        self,
        statement: str,
        originating_campaigns: List[str],
        supporting_evidence: List[str],
        scope: HypothesisScope = HypothesisScope.BRAND,
        confidence: float = 0.85,
        contradicting_evidence: Optional[List[str]] = None,
        known_limitations: Optional[List[str]] = None,
        test_recommendation: str = "",
    ) -> LearningHypothesis:
        hyp = LearningHypothesis(
            hypothesis_id=f"hyp_{uuid.uuid4().hex[:8]}",
            statement=statement,
            originating_campaigns=originating_campaigns,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence or [],
            scope=scope,
            confidence=confidence,
            known_limitations=known_limitations or ["Observed in autumn seasonality only", "Relies on high-contrast architectural backdrops"],
            test_recommendation=test_recommendation or "Run controlled A/B test on next collection hero placement.",
            status="PROVISIONAL",
        )
        self._hypotheses[hyp.hypothesis_id] = hyp
        return hyp

    def get_hypothesis(self, hypothesis_id: str) -> Optional[LearningHypothesis]:
        return self._hypotheses.get(hypothesis_id)

    def list_hypotheses(self, scope: Optional[HypothesisScope] = None) -> List[LearningHypothesis]:
        if scope:
            return [h for h in self._hypotheses.values() if h.scope == scope]
        return list(self._hypotheses.values())

    def add_contradicting_evidence(self, hypothesis_id: str, contradiction_snippet: str) -> LearningHypothesis:
        hyp = self._hypotheses.get(hypothesis_id)
        if not hyp:
            raise KeyError(f"Hypothesis '{hypothesis_id}' not found.")
        hyp.contradicting_evidence.append(contradiction_snippet)
        hyp.confidence = max(0.2, round(hyp.confidence - 0.15, 2))
        return hyp
