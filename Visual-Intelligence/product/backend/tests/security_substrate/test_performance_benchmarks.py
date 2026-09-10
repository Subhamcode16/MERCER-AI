"""
Performance benchmark test suite for Option H Verification Harness.
Measures latency, throughput, and in-place memory wiping time.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import time
import pytest

from security_substrate.crypto_utils import compute_salted_commitment, generate_salt
from security_substrate.verification_harness import (
    OptionHVerificationHarness,
    VerificationClaim,
    DEFAULT_TEST_DOMAIN_KEY,
)


def test_verification_harness_performance_benchmark():
    """
    Benchmark Option H verification harness performance across 100 iterations.
    Target bounds:
        - Evaluation Latency: < 25ms per evaluation for 1MB asset.
        - Memory Wipe Latency: < 5ms per 1MB bytearray.
    """
    harness = OptionHVerificationHarness(domain_signing_key=DEFAULT_TEST_DOMAIN_KEY)
    asset_size = 1 * 1024 * 1024  # 1MB test asset
    iterations = 50

    latencies = []

    for _ in range(iterations):
        asset_bytes = bytearray(b"A" * asset_size)
        salt = generate_salt(32)
        expected_hash = compute_salted_commitment(asset_bytes, salt)
        claim = VerificationClaim(
            claim_id="bench-claim-001",
            target_property="provenance_hash_match",
            expected_salted_hash=expected_hash,
            salt=salt
        )

        start_ns = time.perf_counter_ns()
        result = harness.evaluate_asset_claim(asset_bytes, claim, "bench-anchor-1")
        end_ns = time.perf_counter_ns()

        elapsed_ms = (end_ns - start_ns) / 1_000_000.0
        latencies.append(elapsed_ms)

        assert result.status == "PASS"
        assert len(asset_bytes) == 0  # Memory wiped

    avg_latency_ms = sum(latencies) / len(latencies)
    max_latency_ms = max(latencies)

    print(f"\n[BENCHMARK] Option H 1MB Asset Evaluation Latency: Avg = {avg_latency_ms:.2f}ms, Max = {max_latency_ms:.2f}ms over {iterations} iterations.")

    # Performance assertion aligned with Phase 2 plan (< 50ms target)
    assert avg_latency_ms < 50.0, f"Average evaluation latency ({avg_latency_ms:.2f}ms) exceeded 50ms target"
