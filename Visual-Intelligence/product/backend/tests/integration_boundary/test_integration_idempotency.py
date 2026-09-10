"""
Unit tests for Phase 13 External Idempotency Barrier (INV-13-008).
"""

import threading
import pytest

from src.integration_boundary.idempotency import ExternalIdempotencyBarrier
from src.integration_boundary.exceptions import ExternalReplayError


def test_idempotency_key_reservation():
    barrier = ExternalIdempotencyBarrier()
    key = barrier.compute_idempotency_key("m1", "auth1", "hash1", "create_draft", "idem1")

    # First reservation passes
    barrier.reserve_key(key)
    assert barrier.is_seen(key) is True

    # Second reservation raises ExternalReplayError
    with pytest.raises(ExternalReplayError):
        barrier.reserve_key(key)


def test_idempotency_concurrent_race():
    barrier = ExternalIdempotencyBarrier()
    key = "race_key_01"
    results = []

    def worker():
        try:
            barrier.reserve_key(key)
            results.append("SUCCESS")
        except ExternalReplayError:
            results.append("REPLAY")

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Exactly 1 thread succeeds, 9 threads get REPLAY
    assert results.count("SUCCESS") == 1
    assert results.count("REPLAY") == 9
