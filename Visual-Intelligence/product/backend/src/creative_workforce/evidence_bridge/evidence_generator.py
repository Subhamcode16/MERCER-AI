"""
Phase 26 Evidence-Backed Recommendation Bridge.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


@dataclass
class EvidenceBackedRecommendation:
    decision: str
    rationale: str
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    confidence: float = 1.0
    alternatives: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    source_provenance: Dict[str, Any] = field(default_factory=dict)
    is_advisory: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EvidenceBridge:
    """Generates structured evidence packets for worker recommendations."""

    @staticmethod
    def create_recommendation(
        decision: str,
        rationale: str,
        supporting_evidence: List[str],
        confidence: float,
        contradicting_evidence: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        alternatives: Optional[List[str]] = None,
        unknowns: Optional[List[str]] = None,
        source_provenance: Optional[Dict[str, Any]] = None,
    ) -> EvidenceBackedRecommendation:
        return EvidenceBackedRecommendation(
            decision=decision,
            rationale=rationale,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence or [],
            assumptions=assumptions or [],
            confidence=confidence,
            alternatives=alternatives or [],
            unknowns=unknowns or ["Causal relationship not isolated via controlled experiment"],
            source_provenance=source_provenance or {"source": "CREATIVE_WORKFORCE_INFERENCE"},
            is_advisory=True,
        )
