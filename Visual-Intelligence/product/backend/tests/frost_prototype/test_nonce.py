"""
Tests for FROST Prototype Nonce Safety, Tracking, and Reuse Prevention.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from research.frost_prototype.nonce import SigningNonceTracker, NonceReuseException


def test_nonce_pair_generation():
    """Verify generating fresh nonce pairs and public commitments."""
    tracker = SigningNonceTracker()
    secret_pair, comm = tracker.generate_nonce_pair(participant_id=1)

    assert secret_pair.participant_id == 1
    assert comm.participant_id == 1
    assert secret_pair.hiding_nonce > 0
    assert secret_pair.binding_nonce > 0
    assert comm.commitment_hiding > 0
    assert comm.commitment_binding > 0


def test_nonce_consumption_success():
    """Verify fresh nonce can be consumed successfully."""
    tracker = SigningNonceTracker()
    secret_pair, comm = tracker.generate_nonce_pair(participant_id=1, nonce_id="nonce-001")

    assert tracker.is_consumed("nonce-001") is False
    res = tracker.consume_nonce(1, "nonce-001", comm)
    assert res is True
    assert tracker.is_consumed("nonce-001") is True


def test_duplicate_nonce_rejection():
    """Verify attempting to consume the same nonce twice raises NonceReuseException."""
    tracker = SigningNonceTracker()
    secret_pair, comm = tracker.generate_nonce_pair(participant_id=1, nonce_id="nonce-reuse-test")

    tracker.consume_nonce(1, "nonce-reuse-test", comm)

    with pytest.raises(NonceReuseException, match="already been consumed"):
        tracker.consume_nonce(1, "nonce-reuse-test", comm)


def test_duplicate_commitment_pair_rejection():
    """Verify replaying an identical commitment pair raises NonceReuseException."""
    tracker = SigningNonceTracker()
    secret_pair1, comm1 = tracker.generate_nonce_pair(participant_id=1, nonce_id="nonce-a")

    tracker.consume_nonce(1, "nonce-a", comm1)

    with pytest.raises(NonceReuseException):
        tracker.consume_nonce(1, "nonce-b", comm1)
