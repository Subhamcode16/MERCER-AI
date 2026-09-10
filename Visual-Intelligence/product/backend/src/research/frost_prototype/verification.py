"""
FROST Threshold Signature Verifier.
Verifies Schnorr-style threshold signatures (R, S) against group public key Y and message.
ALL VERIFICATIONS ARE TEST_ONLY RESEARCH ARTIFACTS.
ISOLATED FROM PRODUCTION EXECUTION GATES.
"""

from typing import Optional
from .models import FROSTSignature, GROUP_ORDER_Q, FIELD_PRIME_P, GENERATOR_G
from .commitments import compute_challenge


class VerificationException(Exception):
    """Base exception for signature verification format errors."""
    pass


class FROSTSignatureVerifier:
    """
    FROST Signature Verifier.
    Checks S * G == R + c * Y mod P.
    """
    @staticmethod
    def verify_signature(
        message: bytes,
        group_public_key_Y: int,
        signature: FROSTSignature
    ) -> bool:
        """
        Verifies aggregated threshold signature (R, S) against group public key Y and message bytes.
        Returns True if valid, False otherwise.
        """
        if not signature or not isinstance(signature, FROSTSignature):
            return False

        R = signature.group_commitment_R
        S = signature.signature_scalar_S

        # Boundary checks
        if R <= 0 or R >= FIELD_PRIME_P:
            return False
        if S <= 0 or S >= GROUP_ORDER_Q:
            return False
        if group_public_key_Y <= 0 or group_public_key_Y >= FIELD_PRIME_P:
            return False

        # Recompute challenge c = H(R, Y, message) mod Q
        challenge_c = compute_challenge(R, group_public_key_Y, message)

        # Left hand side: S * G mod P = (G ^ S) mod P
        lhs = pow(GENERATOR_G, S, FIELD_PRIME_P)

        # Right hand side: (R * (Y ^ c mod P)) mod P
        y_c = pow(group_public_key_Y, challenge_c, FIELD_PRIME_P)
        rhs = (R * y_c) % FIELD_PRIME_P

        return lhs == rhs
