"""
IF-EVIDENCE-001 Phase 5 Security Evidence Models & Normalization Schema.
Enforces strict schema validation, classification boundaries, and non-trust status tracking.
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from .exceptions import MalformedEvidenceException


class EvidenceClassification(str, Enum):
    """
    Explicit classification categories for ingested security evidence.
    """
    VERIFICATION_EVIDENCE = "VERIFICATION_EVIDENCE"
    ASSURANCE_EVIDENCE = "ASSURANCE_EVIDENCE"
    RECOVERY_EVIDENCE = "RECOVERY_EVIDENCE"
    RESEARCH_CRYPTOGRAPHIC_EVIDENCE = "RESEARCH_CRYPTOGRAPHIC_EVIDENCE"


class EvidenceProvenance(str, Enum):
    """
    Authorized subsystem origin for ingested evidence.
    """
    PHASE_2_VERIFICATION = "PHASE_2_VERIFICATION"
    PHASE_1_ASSURANCE = "PHASE_1_ASSURANCE"
    PHASE_3_RECOVERY = "PHASE_3_RECOVERY"
    PHASE_4_RESEARCH = "PHASE_4_RESEARCH"


class EvidenceStatus(str, Enum):
    """
    Lifecycle status tracking for evidence records.
    Explicitly avoids terms like 'trusted' or 'authorized'.
    """
    RECEIVED = "RECEIVED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"
    EXPIRED = "EXPIRED"
    CONSUMED = "CONSUMED"


DEFAULT_TRUST_MARKER_RESEARCH = "TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION"
DEFAULT_TRUST_MARKER_INFORMATIONAL = "INFORMATIONAL_ONLY"
DEFAULT_TRUST_MARKER_PRODUCTION = "PRODUCTION_EVIDENCE"


@dataclass
class NormalizedEvidenceRecord:
    """
    Normalized, non-secret evidence record container.
    Guarantees strict schema compliance and research boundary enforcement.
    """
    evidence_id: str
    classification: EvidenceClassification
    provenance: EvidenceProvenance
    status: EvidenceStatus
    system_id: str
    protocol_version: str
    creation_time: float
    ingestion_time: float
    expiration_time: float
    payload_commitment: str
    unique_nonce: str
    correlation_id: str
    trust_marker: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # 1. Reject boolean type confusion for all scalar fields
        fields_to_check = {
            "evidence_id": self.evidence_id,
            "system_id": self.system_id,
            "protocol_version": self.protocol_version,
            "payload_commitment": self.payload_commitment,
            "unique_nonce": self.unique_nonce,
            "correlation_id": self.correlation_id,
            "trust_marker": self.trust_marker,
            "creation_time": self.creation_time,
            "ingestion_time": self.ingestion_time,
            "expiration_time": self.expiration_time,
        }
        for name, val in fields_to_check.items():
            if isinstance(val, bool):
                raise MalformedEvidenceException(f"Boolean type confusion not permitted for field: {name}")

        # 2. Reject empty or whitespace-only string identifiers
        string_fields = [
            ("evidence_id", self.evidence_id),
            ("system_id", self.system_id),
            ("protocol_version", self.protocol_version),
            ("payload_commitment", self.payload_commitment),
            ("unique_nonce", self.unique_nonce),
            ("correlation_id", self.correlation_id),
            ("trust_marker", self.trust_marker),
        ]
        for name, val in string_fields:
            if not isinstance(val, str) or not val.strip():
                raise MalformedEvidenceException(f"Field {name} must be a non-empty string")

        # 3. Numeric timestamp validations
        try:
            c_time = float(self.creation_time)
            i_time = float(self.ingestion_time)
            e_time = float(self.expiration_time)
        except (ValueError, TypeError) as err:
            raise MalformedEvidenceException(f"Invalid numeric timestamp format: {str(err)}") from err

        if e_time < c_time:
            raise MalformedEvidenceException("Expiration time cannot be earlier than creation time")

        # 4. Phase 4 Research Boundary Invariant
        # If provenance is PHASE_4_RESEARCH or classification is RESEARCH_CRYPTOGRAPHIC_EVIDENCE,
        # classification MUST be RESEARCH_CRYPTOGRAPHIC_EVIDENCE and trust_marker MUST be DEFAULT_TRUST_MARKER_RESEARCH.
        if self.provenance == EvidenceProvenance.PHASE_4_RESEARCH or self.classification == EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE:
            if self.classification != EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE:
                raise MalformedEvidenceException(
                    f"Research evidence provenance ({self.provenance}) cannot be classified as production evidence ({self.classification})"
                )
            if self.trust_marker != DEFAULT_TRUST_MARKER_RESEARCH:
                raise MalformedEvidenceException(
                    f"Research evidence must bear trust_marker='{DEFAULT_TRUST_MARKER_RESEARCH}', got '{self.trust_marker}'"
                )

        # 5. Phase 3 Recovery Evidence Informational Invariant
        if self.classification == EvidenceClassification.RECOVERY_EVIDENCE or self.provenance == EvidenceProvenance.PHASE_3_RECOVERY:
            if self.trust_marker not in (DEFAULT_TRUST_MARKER_INFORMATIONAL, DEFAULT_TRUST_MARKER_PRODUCTION):
                raise MalformedEvidenceException("Recovery evidence must be marked as informational or recovery audit evidence")
