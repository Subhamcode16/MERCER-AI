"""
Tests for FROST Signature Verification & Boundary Checks.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from research.frost_prototype.models import FROSTSignature, GROUP_ORDER_Q, FIELD_PRIME_P
from research.frost_prototype.signing import generate_test_key_set
from research.frost_prototype.verification import FROSTSignatureVerifier
from .test_signing import create_test_coordinator


def test_valid_signature_verification():
    """Verify valid signature returns True."""
    coordinator, group_pubkey = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Authentic Research Message"

    sig = coordinator.execute_threshold_signing(msg, [1, 2])
    assert FROSTSignatureVerifier.verify_signature(msg, group_pubkey, sig) is True


def test_modified_message_rejection():
    """Verify modifying message after signing fails verification."""
    coordinator, group_pubkey = create_test_coordinator(total_n=3, threshold_t=2)
    original_msg = b"Original Message Payload"
    tampered_msg = b"Tampered Message Payload"

    sig = coordinator.execute_threshold_signing(original_msg, [1, 2])
    assert FROSTSignatureVerifier.verify_signature(tampered_msg, group_pubkey, sig) is False


def test_modified_signature_scalar_rejection():
    """Verify modifying signature scalars R or S fails verification."""
    coordinator, group_pubkey = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Signature Scalar Tampering Test"

    sig = coordinator.execute_threshold_signing(msg, [1, 2])

    # Tamper S
    bad_sig_s = FROSTSignature(
        group_commitment_R=sig.group_commitment_R,
        signature_scalar_S=(sig.signature_scalar_S + 1) % GROUP_ORDER_Q,
        message_hash=sig.message_hash,
        participating_ids=sig.participating_ids
    )
    assert FROSTSignatureVerifier.verify_signature(msg, group_pubkey, bad_sig_s) is False

    # Tamper R
    bad_sig_r = FROSTSignature(
        group_commitment_R=(sig.group_commitment_R + 1) % FIELD_PRIME_P,
        signature_scalar_S=sig.signature_scalar_S,
        message_hash=sig.message_hash,
        participating_ids=sig.participating_ids
    )
    assert FROSTSignatureVerifier.verify_signature(msg, group_pubkey, bad_sig_r) is False


def test_wrong_group_public_key_rejection():
    """Verify verifying signature against a wrong group public key fails."""
    coordinator1, key1 = create_test_coordinator(total_n=3, threshold_t=2)
    coordinator2, key2 = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Public Key Mismatch Test"

    sig = coordinator1.execute_threshold_signing(msg, [1, 2])
    assert FROSTSignatureVerifier.verify_signature(msg, key2, sig) is False


def test_malformed_signature_bounds_rejection():
    """Verify out-of-bounds R or S or invalid types return False."""
    msg = b"Boundary Test"
    key = 12345

    bad_r_zero = FROSTSignature(0, 500, "hash", [1, 2])
    assert FROSTSignatureVerifier.verify_signature(msg, key, bad_r_zero) is False

    bad_s_overflow = FROSTSignature(500, GROUP_ORDER_Q + 10, "hash", [1, 2])
    assert FROSTSignatureVerifier.verify_signature(msg, key, bad_s_overflow) is False

    assert FROSTSignatureVerifier.verify_signature(msg, key, None) is False
