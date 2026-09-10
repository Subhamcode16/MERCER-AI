"""
IF-DECISION-002 Phase 6 Security Decision Policy.
Enforces deterministic evaluation rules over normalized evidence records without state mutation.
"""

import time
from typing import List, Set, Tuple, Optional, Dict, Any

from .evidence_models import NormalizedEvidenceRecord, EvidenceClassification, EvidenceStatus
from .decision_models import (
    DecisionClassification,
    DecisionStatus,
    DecisionReasonCode,
    DecisionContext,
    InvalidDecisionException,
)


class DecisionPolicy:
    """
    Deterministic security evaluation policy.
    Evaluates evidence records against policy requirements, temporal windows, and research boundaries.
    Does NOT mutate EpistemicState or invoke ExecutionGate.
    """
    def __init__(
        self,
        policy_version: str = "6.0.0",
        max_freshness_window: float = 900.0,
        required_classifications: Optional[Set[EvidenceClassification]] = None,
    ):
        if isinstance(policy_version, bool) or not isinstance(policy_version, str) or not policy_version.strip():
            raise InvalidDecisionException("policy_version must be a non-empty string")
        if isinstance(max_freshness_window, bool) or not isinstance(max_freshness_window, (int, float)) or max_freshness_window <= 0:
            raise InvalidDecisionException("max_freshness_window must be a positive number")

        self.policy_version = policy_version
        self.max_freshness_window = max_freshness_window
        if required_classifications is None:
            self.required_classifications = {
                EvidenceClassification.VERIFICATION_EVIDENCE,
                EvidenceClassification.ASSURANCE_EVIDENCE,
            }
        else:
            self.required_classifications = set(required_classifications)

    def evaluate(
        self,
        evidence_records: List[NormalizedEvidenceRecord],
        context: DecisionContext,
    ) -> Tuple[DecisionClassification, DecisionStatus, List[DecisionReasonCode]]:
        """
        Evaluates a set of normalized evidence records under the current policy.
        Returns a deterministic classification, status, and reason code list.
        """
        # 1. Validate inputs
        if not isinstance(context, DecisionContext):
            raise InvalidDecisionException("context must be a valid DecisionContext instance")
        if not isinstance(evidence_records, list):
            raise InvalidDecisionException("evidence_records must be a list")

        # 2. Check policy version match
        if context.policy_version != self.policy_version:
            return (
                DecisionClassification.EVALUATION_FAIL,
                DecisionStatus.REJECTED,
                [DecisionReasonCode.POLICY_VERSION_MISMATCH],
            )

        # 3. Handle empty evidence set
        if len(evidence_records) == 0:
            return (
                DecisionClassification.INSUFFICIENT_EVIDENCE,
                DecisionStatus.REJECTED,
                [DecisionReasonCode.MISSING_REQUIRED_EVIDENCE],
            )

        # 4. Check for malformed record structures
        for rec in evidence_records:
            if not isinstance(rec, NormalizedEvidenceRecord):
                return (
                    DecisionClassification.EVALUATION_FAIL,
                    DecisionStatus.REJECTED,
                    [DecisionReasonCode.MALFORMED_INPUT_DETECTED],
                )

        now = context.evaluation_timestamp

        # 5. Check for Quarantined or Rejected status
        has_quarantined_or_rejected = any(
            rec.status in (EvidenceStatus.QUARANTINED, EvidenceStatus.REJECTED)
            for rec in evidence_records
        )
        if has_quarantined_or_rejected:
            return (
                DecisionClassification.EVIDENCE_QUARANTINED,
                DecisionStatus.QUARANTINED,
                [DecisionReasonCode.EVIDENCE_QUARANTINED_OR_REJECTED],
            )

        # 6. Check for Expired evidence or stale creation timestamps
        has_expired = any(
            rec.status == EvidenceStatus.EXPIRED
            or now > rec.expiration_time
            or (now - rec.creation_time) > self.max_freshness_window
            for rec in evidence_records
        )
        if has_expired:
            return (
                DecisionClassification.EVIDENCE_EXPIRED,
                DecisionStatus.EXPIRED,
                [DecisionReasonCode.EVIDENCE_EXPIRED_OR_STALE],
            )

        # 7. Check for Phase 4 Research Evidence
        has_research = any(
            rec.classification == EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE
            or rec.trust_marker == "TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION"
            for rec in evidence_records
        )
        if has_research:
            return (
                DecisionClassification.RESEARCH_ONLY,
                DecisionStatus.EVALUATED,
                [DecisionReasonCode.RESEARCH_EVIDENCE_NOT_AUTHORITATIVE],
            )

        # 8. Check for conflicting evidence (e.g., contradictory commitments for same correlation_id)
        commitments_by_correlation: Dict[str, str] = {}
        for rec in evidence_records:
            corr = rec.correlation_id
            if corr in commitments_by_correlation:
                if commitments_by_correlation[corr] != rec.payload_commitment:
                    return (
                        DecisionClassification.EVIDENCE_CONFLICT,
                        DecisionStatus.REJECTED,
                        [DecisionReasonCode.EVIDENCE_CONTRADICTION_DETECTED],
                    )
            else:
                commitments_by_correlation[corr] = rec.payload_commitment

        # 9. Verify required classifications are satisfied
        present_classifications = {rec.classification for rec in evidence_records}
        missing = self.required_classifications - present_classifications
        if missing:
            return (
                DecisionClassification.INSUFFICIENT_EVIDENCE,
                DecisionStatus.REJECTED,
                [DecisionReasonCode.MISSING_REQUIRED_EVIDENCE],
            )

        # 10. Evaluation Pass
        return (
            DecisionClassification.EVALUATION_PASS,
            DecisionStatus.EVALUATED,
            [DecisionReasonCode.EVIDENCE_SUFFICIENT_AND_VALID],
        )
