"""
IF-VERIFY-001 Option H Privacy-Preserving Ephemeral Verification Harness.
Enforces Raw-Asset Non-Persistence via RAM-only processing and in-place memory wiping.
"""

import gc
import time
from dataclasses import dataclass
from typing import Optional

from .assurance_loop import EvidencePayload
from .exceptions import FailClosedException, MalformedEvidenceException
from .crypto_utils import (
    compute_salted_commitment,
    generate_nonce,
    sign_evidence_payload,
)

MAX_ASSET_SIZE_BYTES = 100 * 1024 * 1024  # 100MB Limit
DEFAULT_TEST_DOMAIN_KEY = b"OptionH_Verification_Domain_Signing_Key_2026"


ZERO_CHUNK = b"\x00" * 65536


@dataclass
class VerificationClaim:
    """
    Claim payload submitted to Verification Harness for evaluation.
    EPISTEMIC BOUNDARY:
        Cryptographic Commitment != Semantic Truth
        Successful Computation != Objective Truth
        Provenance Signature != Ground Truth
    """
    claim_id: str
    target_property: str
    expected_salted_hash: str
    salt: bytes


@dataclass
class EvaluationResult:
    """
    Evaluation output produced by IF-VERIFY-001 VerificationHarness.
    """
    claim_id: str
    status: str  # "PASS" or "FAIL"
    evidence: Optional[EvidencePayload]
    evaluation_timestamp: float


class OptionHVerificationHarness:
    """
    IF-VERIFY-001 Option H Ephemeral Verification Harness.
    Ingests transient visual asset bytearrays in RAM, computes salted commitments,
    verifies claims, emits signed EvidencePayload objects, and zeroes controlled buffers.
    """
    def __init__(self, domain_signing_key: bytes = DEFAULT_TEST_DOMAIN_KEY):
        if not domain_signing_key or not isinstance(domain_signing_key, bytes):
            raise ValueError("domain_signing_key must be a non-empty bytes object")
        self._domain_signing_key = domain_signing_key

    def _wipe_transient_memory(self, asset_bytes: bytearray) -> None:
        """
        Executes application-level controlled-buffer zero-overwriting across asset bytearray.

        LIMITATION NOTICE:
        This operation zero-overwrites the caller's application-controlled bytearray buffer in-place.
        It does NOT provide process-wide C-heap memory erasure, OS kernel pagefile swap protection,
        or physical RAM hardware sanitization (which requires kernel-level mlock / unswappable pages).
        """
        if isinstance(asset_bytes, bytearray) and len(asset_bytes) > 0:
            asset_bytes[:] = b"\x00" * len(asset_bytes)
            asset_bytes.clear()

    def evaluate_asset_claim(
        self,
        asset_bytes: bytearray,
        claim: VerificationClaim,
        trust_anchor_id: str
    ) -> EvaluationResult:
        """
        IF-VERIFY-001 Interface Method: Evaluates transient visual asset against a claim payload.

        Bounded Claims:
            - Zero raw asset bytes written to persistent application files or databases.
            - Controlled bytearray buffer zero-overwritten in finally block.
            - Does NOT prove real-world semantic ground truth of image content.

        Returns:
            EvaluationResult containing Signed EvidencePayload on PASS.
        """
        eval_timestamp = time.time()

        try:
            # 1. Structural Precondition Verification
            if asset_bytes is None or not isinstance(asset_bytes, bytearray):
                raise MalformedEvidenceException("asset_bytes must be a mutable bytearray instance")

            if len(asset_bytes) > MAX_ASSET_SIZE_BYTES:
                raise MalformedEvidenceException(
                    f"Asset size ({len(asset_bytes)} bytes) exceeds max limit of {MAX_ASSET_SIZE_BYTES} bytes"
                )

            if not claim or not isinstance(claim, VerificationClaim):
                raise MalformedEvidenceException("Invalid claim payload provided")

            if not claim.claim_id or not claim.expected_salted_hash or not claim.salt:
                raise MalformedEvidenceException("VerificationClaim contains empty mandatory fields")

            if not trust_anchor_id or not isinstance(trust_anchor_id, str):
                raise MalformedEvidenceException("Invalid trust_anchor_id provided")

            # 2. Compute Salted Hash Commitment
            computed_hash = compute_salted_commitment(asset_bytes, claim.salt)

            # 3. Property & Hash Verification
            is_valid = (computed_hash == claim.expected_salted_hash)
            status = "PASS" if is_valid else "FAIL"

            if not is_valid:
                return EvaluationResult(
                    claim_id=claim.claim_id,
                    status="FAIL",
                    evidence=None,
                    evaluation_timestamp=eval_timestamp
                )

            # 4. Construct & Sign Evidence Payload
            nonce = generate_nonce(16)
            payload_dict = {
                "claim_id": claim.claim_id,
                "asset_hash": computed_hash,
                "timestamp": eval_timestamp,
                "nonce": nonce,
                "status": status,
                "trust_anchor_id": trust_anchor_id,
            }

            sig = sign_evidence_payload(payload_dict, self._domain_signing_key)

            evidence = EvidencePayload(
                claim_id=claim.claim_id,
                asset_hash=computed_hash,
                signature=sig,
                timestamp=eval_timestamp,
                nonce=nonce,
                status=status,
                trust_anchor_id=trust_anchor_id
            )

            return EvaluationResult(
                claim_id=claim.claim_id,
                status="PASS",
                evidence=evidence,
                evaluation_timestamp=eval_timestamp
            )

        except MalformedEvidenceException:
            raise
        except Exception as e:
            raise FailClosedException(f"Unexpected error during Option H verification: {str(e)}") from e
        finally:
            # Explicit memory wipe executed in finally block to ensure RAM sanitization
            if asset_bytes is not None and isinstance(asset_bytes, bytearray):
                self._wipe_transient_memory(asset_bytes)
