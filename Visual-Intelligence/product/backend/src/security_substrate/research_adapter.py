"""
Research Cryptographic Evidence Adapter for Phase 5.
Adapts Phase 4 FROST research results into NormalizedEvidenceRecord containers.
STRICTLY FORCES RESEARCH CLASSIFICATION AND TEST_ONLY TRUST MARKERS.
HAS NO EXECUTION OR AUTHORIZATION PRIVILEGES.
"""

import time
import uuid
import hashlib
from typing import Any, Optional, Dict
from .evidence_models import (
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    DEFAULT_TRUST_MARKER_RESEARCH,
)
from .exceptions import MalformedEvidenceException


class ResearchAdapter:
    """
    Adapter converting Phase 4 FROST research results into normalized research evidence records.
    Permanently tags converted evidence as RESEARCH_CRYPTOGRAPHIC_EVIDENCE and TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION.
    """
    @staticmethod
    def convert_research_result_to_evidence(
        frost_signature: Any,
        message: bytes,
        correlation_id: Optional[str] = None
    ) -> NormalizedEvidenceRecord:
        """
        Converts a FROSTSignature research object into a NormalizedEvidenceRecord.
        Extracts non-secret metadata (group_commitment_R, message_hash, participating_ids).
        Does NOT expose secret shares, secret nonces, or private keys.
        """
        if not frost_signature:
            raise MalformedEvidenceException("Invalid or null FROST research signature submitted")

        # Extract non-secret research attributes
        r_val = getattr(frost_signature, "group_commitment_R", None)
        s_val = getattr(frost_signature, "signature_scalar_S", None)
        msg_hash = getattr(frost_signature, "message_hash", None)
        part_ids = getattr(frost_signature, "participating_ids", [])
        marker = getattr(frost_signature, "marker", "")

        if r_val is None or s_val is None:
            raise MalformedEvidenceException("FROST signature object missing required scalar fields (R, S)")

        now = time.time()
        evid_id = f"research-evid-{uuid.uuid4()}"
        nonce_str = f"nonce-{uuid.uuid4().hex}"
        corr_id = correlation_id or f"corr-{uuid.uuid4().hex[:8]}"

        # Compute payload commitment over non-secret metadata representation
        hasher = hashlib.sha256()
        hasher.update(str(r_val).encode("utf-8"))
        hasher.update(b":")
        hasher.update(str(s_val).encode("utf-8"))
        hasher.update(b":")
        hasher.update(message)
        payload_comm = hasher.hexdigest()

        metadata: Dict[str, Any] = {
            "group_commitment_R": str(r_val),
            "participating_ids": part_ids,
            "message_hash": msg_hash or hashlib.sha256(message).hexdigest(),
            "research_marker": marker or "TEST_ONLY_RESEARCH_RESULT",
        }

        # Force strict research classification and test-only trust marker
        return NormalizedEvidenceRecord(
            evidence_id=evid_id,
            classification=EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_4_RESEARCH,
            status=EvidenceStatus.RECEIVED,
            system_id="SYSTEM_VISUAL_INTELLIGENCE_001",
            protocol_version="1.0",
            creation_time=now,
            ingestion_time=now,
            expiration_time=now + 600.0,  # 10 minute expiration
            payload_commitment=payload_comm,
            unique_nonce=nonce_str,
            correlation_id=corr_id,
            trust_marker=DEFAULT_TRUST_MARKER_RESEARCH,
            metadata=metadata
        )
