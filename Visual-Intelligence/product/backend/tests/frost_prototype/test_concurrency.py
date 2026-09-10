"""
Concurrency and Parallel Threading Tests for FROST Research Prototype.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
import concurrent.futures
from research.frost_prototype.nonce import SigningNonceTracker, NonceReuseException
from research.frost_prototype.verification import FROSTSignatureVerifier
from .test_signing import create_test_coordinator


def test_concurrent_nonce_generation():
    """Verify 20 concurrent threads generating nonces produce unique nonces without collision."""
    tracker = SigningNonceTracker()

    def worker(i):
        secret_pair, comm = tracker.generate_nonce_pair(participant_id=(i % 5) + 1)
        return secret_pair.nonce_identifier, comm.commitment_hiding

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(worker, range(20)))

    nonce_ids = [r[0] for r in results]
    commitments = [r[1] for r in results]

    assert len(nonce_ids) == 20
    assert len(set(nonce_ids)) == 20
    assert len(set(commitments)) == 20


def test_concurrent_threshold_signing_requests():
    """Verify 10 concurrent signing requests execute safely under multi-threading."""
    coordinator, group_pubkey = create_test_coordinator(total_n=5, threshold_t=3)

    def worker(i):
        msg = f"Concurrent Message {i}".encode("utf-8")
        sig = coordinator.execute_threshold_signing(msg, signer_ids=[1, 2, 3])
        is_valid = FROSTSignatureVerifier.verify_signature(msg, group_pubkey, sig)
        return is_valid

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(worker, range(10)))

    assert len(results) == 10
    assert all(r is True for r in results)


def test_concurrent_duplicate_nonce_race():
    """Verify concurrent attempts to consume the same nonce result in exactly 1 success and N-1 NonceReuseExceptions."""
    tracker = SigningNonceTracker()
    secret_pair, comm = tracker.generate_nonce_pair(participant_id=1, nonce_id="race-nonce-001")

    success_count = 0
    failure_count = 0

    def worker(_):
        nonlocal success_count, failure_count
        try:
            tracker.consume_nonce(1, "race-nonce-001", comm)
            return "SUCCESS"
        except NonceReuseException:
            return "FAILED"

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(worker, range(10)))

    successes = [r for r in results if r == "SUCCESS"]
    failures = [r for r in results if r == "FAILED"]

    assert len(successes) == 1
    assert len(failures) == 9
