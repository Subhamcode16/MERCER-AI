"""
Governance Policy Engine enforcing epistemic and organizational invariants for Phase 29.
"""
from typing import List, Tuple
from ..recommendations.recommendation_models import StrategicRecommendation, RecommendationStatus
from ..signals.signal_types import StrategicSignal, EpistemicStatus
from ..graph.models import IntelligenceClassification


class GovernanceViolation(Exception):
    pass


class StrategicGovernancePolicyEngine:
    @staticmethod
    def validate_signal_integrity(signal: StrategicSignal) -> Tuple[bool, List[str]]:
        violations = []

        # Invariant 1: Signal != Fact (confidence cannot be 1.0 on unverified observations)
        if signal.epistemic_status == EpistemicStatus.UNVERIFIED_EXTERNAL and signal.confidence > 0.60:
            violations.append("UNVERIFIED_EXTERNAL_SIGNAL_EXCEEDS_MAX_CONFIDENCE")

        # Invariant 2: Unknowns must never be empty
        if not signal.unknowns:
            violations.append("UNKNOWN_COLLAPSE_VIOLATION: Unknowns list cannot be empty.")

        return len(violations) == 0, violations

    @staticmethod
    def validate_recommendation_governance(
        rec: StrategicRecommendation,
        decision_maker_role: str,
    ) -> Tuple[bool, List[str]]:
        violations = []

        # Invariant 3: Recommendation != Execution Permission (auto-execution forbidden)
        if decision_maker_role not in ("STRATEGIC_OPERATOR", "CAMPAIGN_DIRECTOR", "ADMIN", "EXECUTIVE"):
            violations.append(f"UNAUTHORIZED_DECISION_ROLE: '{decision_maker_role}' cannot authorize strategic execution.")

        # Invariant 4: Withdrawn or expired recommendation cannot be accepted
        if rec.status in (RecommendationStatus.WITHDRAWN, RecommendationStatus.EXPIRED):
            violations.append(f"INVALID_RECOMMENDATION_STATE: Cannot act on recommendation in state '{rec.status.value}'.")

        return len(violations) == 0, violations

    @staticmethod
    def enforce_tenant_boundary(
        source_tenant: str,
        target_tenant: str,
        classification: IntelligenceClassification,
    ) -> bool:
        # Invariant 5: Institutional Learning != Cross-Client Leakage
        if classification == IntelligenceClassification.CLIENT_PRIVATE and source_tenant != target_tenant:
            raise GovernanceViolation(
                f"Cross-Tenant Boundary Violation: Attempted cross-tenant access between '{source_tenant}' and '{target_tenant}' for CLIENT_PRIVATE asset."
            )
        return True
