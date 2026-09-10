"""
IF-ENGINE-001 Phase 6 Security Decision Engine.
Evaluates normalized evidence records and produces committed attestation records.
Possesses zero execution authority, zero state mutation capabilities, and zero ExecutionGate coupling.
"""

import uuid
import time
import threading
from typing import List, Tuple, Optional

from .evidence_models import NormalizedEvidenceRecord
from .decision_models import (
    SecurityDecision,
    AttestationRecord,
    DecisionClassification,
    DecisionStatus,
    DecisionReasonCode,
    DecisionContext,
    DecisionEvidenceReference,
    InvalidDecisionException,
)
from .decision_policy import DecisionPolicy
from .attestation import create_attestation
from .decision_replay import DecisionReplayCache


class SecurityDecisionEngine:
    """
    Deterministic Security Decision Engine.
    Processes normalized evidence through policy evaluation to generate attestation records.
    Explicitly decoupled from execution gating and state transitions.
    """
    def __init__(
        self,
        policy: Optional[DecisionPolicy] = None,
        replay_cache: Optional[DecisionReplayCache] = None,
    ):
        self.policy = policy if policy is not None else DecisionPolicy()
        self.replay_cache = replay_cache if replay_cache is not None else DecisionReplayCache()
        self._lock = threading.RLock()

    def evaluate_evidence(
        self,
        evidence_records: List[NormalizedEvidenceRecord],
        context: DecisionContext,
    ) -> Tuple[SecurityDecision, AttestationRecord]:
        """
        Evaluates normalized evidence records and returns a tuple of (SecurityDecision, AttestationRecord).
        Thread-safe execution under RLock.
        """
        if not isinstance(context, DecisionContext):
            raise InvalidDecisionException("context must be a valid DecisionContext instance")
        if not isinstance(evidence_records, list):
            raise InvalidDecisionException("evidence_records must be a list")

        with self._lock:
            # 1. Evaluate policy
            classification, status, reason_codes = self.policy.evaluate(
                evidence_records=evidence_records,
                context=context,
            )

            # 2. Build evidence references
            evidence_refs: List[DecisionEvidenceReference] = []
            for rec in evidence_records:
                if isinstance(rec, NormalizedEvidenceRecord):
                    evidence_refs.append(
                        DecisionEvidenceReference(
                            evidence_id=rec.evidence_id,
                            classification=rec.classification.value,
                            payload_commitment=rec.payload_commitment,
                            trust_marker=rec.trust_marker,
                        )
                    )

            # 3. Construct SecurityDecision
            decision_id = f"dec-{uuid.uuid4().hex[:12]}"
            decision = SecurityDecision(
                decision_id=decision_id,
                classification=classification,
                status=status,
                reason_codes=reason_codes,
                context=context,
                evidence_references=evidence_refs,
                decision_timestamp=time.time(),
            )

            # 4. Generate AttestationRecord
            attestation = create_attestation(decision)

            # 5. Register in replay defense cache
            self.replay_cache.check_and_register(
                decision_id=decision.decision_id,
                attestation_nonce=attestation.attestation_nonce,
            )

            return decision, attestation
