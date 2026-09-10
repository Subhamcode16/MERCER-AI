"""
Tests for FROST Threshold Signing Protocol Execution across 2-of-3 and 3-of-5 configurations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from research.frost_prototype.models import FROSTConfig
from research.frost_prototype.hardware_custodian import MockHardwareCustodian
from research.frost_prototype.participants import ParticipantNode
from research.frost_prototype.signing import FROSTSigningCoordinator, generate_test_key_set
from research.frost_prototype.verification import FROSTSignatureVerifier


def create_test_coordinator(total_n: int, threshold_t: int):
    group_pubkey, shares = generate_test_key_set(total_n, threshold_t)
    config = FROSTConfig(total_participants_n=total_n, threshold_t=threshold_t)

    nodes = {}
    for p_id, share in shares.items():
        custodian = MockHardwareCustodian(participant_id=p_id, key_share=share)
        nodes[p_id] = ParticipantNode(participant_id=p_id, custodian=custodian)

    coordinator = FROSTSigningCoordinator(config=config, group_public_key=group_pubkey, participant_nodes=nodes)
    return coordinator, group_pubkey


def test_threshold_signing_2_of_3():
    """Verify 2-of-3 threshold signing succeeds and produces a valid verifiable signature."""
    coordinator, group_pubkey = create_test_coordinator(total_n=3, threshold_t=2)
    message = b"Research Test Message - 2 of 3 Threshold Signing"

    sig = coordinator.execute_threshold_signing(message=message, signer_ids=[1, 2])

    assert sig.participating_ids == [1, 2]
    assert sig.marker == "TEST_ONLY_THRESHOLD_SIGNATURE"

    is_valid = FROSTSignatureVerifier.verify_signature(message, group_pubkey, sig)
    assert is_valid is True


def test_threshold_signing_3_of_5_various_subsets():
    """Verify 3-of-5 threshold signing succeeds across different participant combinations."""
    coordinator, group_pubkey = create_test_coordinator(total_n=5, threshold_t=3)
    message = b"Research Test Message - 3 of 5 Threshold Signing"

    # Combination A: {1, 2, 3}
    sig_a = coordinator.execute_threshold_signing(message=message, signer_ids=[1, 2, 3])
    assert FROSTSignatureVerifier.verify_signature(message, group_pubkey, sig_a) is True

    # Combination B: {1, 3, 5}
    sig_b = coordinator.execute_threshold_signing(message=message, signer_ids=[1, 3, 5])
    assert FROSTSignatureVerifier.verify_signature(message, group_pubkey, sig_b) is True

    # Combination C: {2, 4, 5}
    sig_c = coordinator.execute_threshold_signing(message=message, signer_ids=[2, 4, 5])
    assert FROSTSignatureVerifier.verify_signature(message, group_pubkey, sig_c) is True


def test_excess_signers_handling():
    """Verify signing with more signers than threshold (4 signers in 3-of-5) succeeds."""
    coordinator, group_pubkey = create_test_coordinator(total_n=5, threshold_t=3)
    message = b"Excess Signers Test Message"

    sig = coordinator.execute_threshold_signing(message=message, signer_ids=[1, 2, 3, 4])
    assert sig.participating_ids == [1, 2, 3, 4]
    assert FROSTSignatureVerifier.verify_signature(message, group_pubkey, sig) is True
