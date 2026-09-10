"""
Comprehensive Negative Path & Adversarial Failure Tests for FROST Research Prototype.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from research.frost_prototype.models import FROSTConfig
from research.frost_prototype.signing import (
    FROSTSigningCoordinator,
    generate_test_key_set,
    InsufficientSignersException,
    InvalidParticipantException,
)
from research.frost_prototype.hardware_custodian import (
    MockHardwareCustodian,
    HardwareLockedException,
    HardwareUnavailableException,
    CorruptedShareException,
    HardwareTimeoutException,
)
from research.frost_prototype.participants import ParticipantNode
from research.frost_prototype.nonce import NonceReuseException
from .test_signing import create_test_coordinator


def test_insufficient_signers_rejection():
    """Verify attempting to sign with 1 signer when threshold is 2 raises InsufficientSignersException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Insufficient Signers Test"

    with pytest.raises(InsufficientSignersException, match="Insufficient signers"):
        coordinator.execute_threshold_signing(msg, signer_ids=[1])


def test_duplicate_signer_ids_rejection():
    """Verify specifying duplicate participant IDs raises InvalidParticipantException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Duplicate Signers Test"

    with pytest.raises(InvalidParticipantException, match="Duplicate participant IDs"):
        coordinator.execute_threshold_signing(msg, signer_ids=[1, 1])


def test_unregistered_participant_rejection():
    """Verify including unregistered participant ID raises InvalidParticipantException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Unregistered Participant Test"

    with pytest.raises(InvalidParticipantException, match="not registered"):
        coordinator.execute_threshold_signing(msg, signer_ids=[1, 99])


def test_hardware_locked_device_failure():
    """Verify mock hardware device locking on 3 invalid PIN attempts raises HardwareLockedException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Hardware Locked Test"

    pin_map = {1: "WRONG_PIN", 2: "123456"}

    # Attempt 1
    with pytest.raises(HardwareLockedException):
        coordinator.execute_threshold_signing(msg, [1, 2], pin_map=pin_map)

    # Attempt 2
    with pytest.raises(HardwareLockedException):
        coordinator.execute_threshold_signing(msg, [1, 2], pin_map=pin_map)

    # Attempt 3 - locks device
    with pytest.raises(HardwareLockedException, match="LOCKED"):
        coordinator.execute_threshold_signing(msg, [1, 2], pin_map=pin_map)


def test_hardware_disconnected_device_failure():
    """Verify disconnected mock hardware device raises HardwareUnavailableException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    coordinator.nodes[1].custodian.set_device_status(connected=False)
    msg = b"Disconnected Hardware Test"

    with pytest.raises(HardwareUnavailableException, match="disconnected"):
        coordinator.execute_threshold_signing(msg, [1, 2])


def test_hardware_corrupted_share_failure():
    """Verify corrupted share in mock hardware raises CorruptedShareException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    coordinator.nodes[2].custodian.set_device_status(corrupted=True)
    msg = b"Corrupted Share Test"

    with pytest.raises(CorruptedShareException, match="corrupted"):
        coordinator.execute_threshold_signing(msg, [1, 2])


def test_hardware_timeout_failure():
    """Verify hardware response delay > 5s limit raises HardwareTimeoutException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    coordinator.nodes[1].custodian.set_device_status(delay_seconds=6.0)
    msg = b"Timeout Test"

    with pytest.raises(HardwareTimeoutException, match="timeout"):
        coordinator.execute_threshold_signing(msg, [1, 2])


def test_reused_nonce_manual_replay_failure():
    """Verify manually replaying a used nonce identifier raises NonceReuseException."""
    coordinator, _ = create_test_coordinator(total_n=3, threshold_t=2)
    node = coordinator.nodes[1]

    comm = node.generate_round1_commitment("manual-nonce-001")

    # Round 2 execution consumes nonce
    node.generate_round2_signature_share(
        nonce_id="manual-nonce-001",
        commitment=comm,
        rho_i=123,
        challenge_c=456,
        signing_set=[1, 2]
    )

    # Second attempt to use same nonce raises NonceReuseException
    with pytest.raises(NonceReuseException):
        node.generate_round2_signature_share(
            nonce_id="manual-nonce-001",
            commitment=comm,
            rho_i=123,
            challenge_c=456,
            signing_set=[1, 2]
        )
