"""
Recommendation Quality Contract enforcing strict epistemic integrity and automatic downgrading.
"""
from typing import List, Tuple
from .recommendation_models import StrategicRecommendation, RecommendationStatus, EpistemicStatus


class QualityAuditResult:
    def __init__(self, passed: bool, adjusted_confidence: float, flags: List[str], final_status: RecommendationStatus):
        self.passed = passed
        self.adjusted_confidence = adjusted_confidence
        self.flags = flags
        self.final_status = final_status


class RecommendationQualityContract:
    @staticmethod
    def audit_recommendation(rec: StrategicRecommendation) -> QualityAuditResult:
        flags = []
        confidence = rec.confidence
        status = rec.status

        # Invariant 1: If no supporting evidence, downgrade to INSUFFICIENT_EVIDENCE
        if not rec.supporting_evidence:
            flags.append("NO_SUPPORTING_EVIDENCE")
            confidence = min(confidence, 0.20)
            rec.epistemic_status = EpistemicStatus.INSUFFICIENT_EVIDENCE

        # Invariant 2: If contradictory evidence exists and is equal or greater than supporting evidence
        if rec.contradicting_evidence and len(rec.contradicting_evidence) >= len(rec.supporting_evidence):
            flags.append("HIGH_CONTRADICTION_RATIO")
            confidence *= 0.60
            status = RecommendationStatus.DOWNGRADED

        # Invariant 3: If epistemic status is observational correlation, cap confidence at 0.70
        if rec.epistemic_status in (EpistemicStatus.OBSERVATIONAL_CORRELATION, EpistemicStatus.CONFOUNDED_OBSERVATION):
            if confidence > 0.70:
                flags.append("OBSERVATIONAL_CONFIDENCE_CAP_APPLIED")
                confidence = 0.70

        # Invariant 4: If assumptions exceed supporting facts, flag high speculative risk
        if len(rec.assumptions) > len(rec.supporting_evidence):
            flags.append("ASSUMPTIONS_EXCEED_EVIDENCE")
            confidence *= 0.85

        # Invariant 5: Unknowns must never be empty
        if not rec.unknowns:
            rec.unknowns = ["Unobserved counterfactual dynamics remain unknown."]
            flags.append("DEFAULT_UNKNOWN_PRESERVED")

        return QualityAuditResult(
            passed=len(flags) == 0 or (confidence >= 0.30 and rec.epistemic_status != EpistemicStatus.INSUFFICIENT_EVIDENCE),
            adjusted_confidence=round(max(0.0, min(1.0, confidence)), 3),
            flags=flags,
            final_status=status,
        )
