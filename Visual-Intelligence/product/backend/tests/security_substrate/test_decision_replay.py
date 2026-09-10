"""
Tests for Phase 6 decision replay defense cache.
"""

import time
import pytest
import concurrent.futures
from security_substrate import (
    DecisionReplayCache,
    DecisionReplayException,
    InvalidDecisionException,
)


def test_decision_replay_single_registration():
    cache = DecisionReplayCache(max_retention_window=60.0)
    cache.check_and_register(decision_id="dec-1", attestation_nonce="nonce-1")
    assert cache.is_replayed("dec-1") is True


def test_decision_replay_duplicate_decision_id():
    cache = DecisionReplayCache(max_retention_window=60.0)
    cache.check_and_register(decision_id="dec-1", attestation_nonce="nonce-1")

    with pytest.raises(DecisionReplayException, match="Replayed decision ID"):
        cache.check_and_register(decision_id="dec-1", attestation_nonce="nonce-2")


def test_decision_replay_duplicate_nonce():
    cache = DecisionReplayCache(max_retention_window=60.0)
    cache.check_and_register(decision_id="dec-1", attestation_nonce="nonce-1")

    with pytest.raises(DecisionReplayException, match="Replayed attestation nonce"):
        cache.check_and_register(decision_id="dec-2", attestation_nonce="nonce-1")


def test_decision_replay_invalid_inputs():
    cache = DecisionReplayCache(max_retention_window=60.0)

    with pytest.raises(InvalidDecisionException):
        cache.check_and_register(decision_id=True, attestation_nonce="nonce-1")

    with pytest.raises(InvalidDecisionException):
        cache.check_and_register(decision_id="dec-1", attestation_nonce="")


def test_decision_replay_concurrent_duplicate_race():
    cache = DecisionReplayCache(max_retention_window=60.0)

    results = []

    def attempt_registration():
        try:
            cache.check_and_register(decision_id="dec-concurrent", attestation_nonce="nonce-concurrent")
            return "SUCCESS"
        except DecisionReplayException:
            return "REPLAY"

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(attempt_registration) for _ in range(10)]
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())

    # Exactly 1 success, 9 replays
    assert results.count("SUCCESS") == 1
    assert results.count("REPLAY") == 9
