"""
Unit and security tests for IF-VERIFY-001 Option H Verification Harness.
Verifies ephemeral memory wiping, salted asset binding, signature verification,
zero disk persistence, and integration with Phase 1 Assurance Loop & Execution Gate.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import time
import pytest
from unittest.mock import patch

from security_substrate.epistemic_state import EpistemicState
from security_substrate.exceptions import (
    MalformedEvidenceException,
    ReplayAttackException,
)
from security_substrate.assurance_loop import AssuranceLoopController
from security_substrate.execution_gate import ExecutionGate
from security_substrate.crypto_utils import (
    compute_salted_commitment,
    generate_salt,
    verify_evidence_signature,
)
from security_substrate.verification_harness import (
    OptionHVerificationHarness,
    VerificationClaim,
    EvaluationResult,
    DEFAULT_TEST_DOMAIN_KEY,
    MAX_ASSET_SIZE_BYTES,
)


@pytest.fixture
def harness():
    return OptionHVerificationHarness(domain_signing_key=DEFAULT_TEST_DOMAIN_KEY)


@pytest.fixture
def sample_asset_bytes():
    return bytearray(b"RAW_VISUAL_ASSET_PIXEL_DATA_2026_TEST_STREAM")


@pytest.fixture
def sample_claim(sample_asset_bytes):
    salt = generate_salt(32)
    expected_hash = compute_salted_commitment(sample_asset_bytes, salt)
    return VerificationClaim(
        claim_id="claim-harness-001",
        target_property="provenance_hash_match",
        expected_salted_hash=expected_hash,
        salt=salt
    )


def test_option_h_successful_evaluation(harness, sample_asset_bytes, sample_claim):
    """Verify positive evaluation produces PASS result and signed EvidencePayload."""
    # Keep copy for verification before harness zeroing
    anchor_id = "trust-anchor-test-1"

    result = harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, anchor_id)

    assert isinstance(result, EvaluationResult)
    assert result.claim_id == sample_claim.claim_id
    assert result.status == "PASS"
    assert result.evidence is not None
    assert result.evidence.claim_id == sample_claim.claim_id
    assert result.evidence.asset_hash == sample_claim.expected_salted_hash
    assert result.evidence.trust_anchor_id == anchor_id
    assert result.evidence.status == "PASS"


def test_memory_wipe_in_finally_block(harness, sample_asset_bytes, sample_claim):
    """Verify raw asset bytearray is explicitly zeroed out and cleared after evaluation."""
    assert len(sample_asset_bytes) > 0

    harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, "anchor-1")

    # Post-condition: bytearray must be empty / zeroed out
    assert len(sample_asset_bytes) == 0


def test_memory_wipe_on_exception(harness):
    """Verify memory wiping occurs in finally block even when an exception is raised."""
    asset_data = bytearray(b"SENSITIVE_PIXEL_DATA")
    invalid_claim = None  # Will raise MalformedEvidenceException

    with pytest.raises(MalformedEvidenceException):
        harness.evaluate_asset_claim(asset_data, invalid_claim, "anchor-1")

    # Post-condition: memory wiping must execute in finally block
    assert len(asset_data) == 0


def test_asset_size_limit_exceeded(harness, sample_claim):
    """Verify assets exceeding MAX_ASSET_SIZE_BYTES trigger MalformedEvidenceException."""
    huge_asset = bytearray(MAX_ASSET_SIZE_BYTES + 10)

    with pytest.raises(MalformedEvidenceException) as exc_info:
        harness.evaluate_asset_claim(huge_asset, sample_claim, "anchor-1")

    assert "exceeds max limit" in str(exc_info.value)
    assert len(huge_asset) == 0  # Memory wiped in finally block


def test_corrupted_asset_hash_mismatch(harness, sample_claim):
    """Verify modified asset bytes return status=FAIL with evidence=None."""
    corrupted_bytes = bytearray(b"CORRUPTED_PIXEL_DATA_UNMATCHED")

    result = harness.evaluate_asset_claim(corrupted_bytes, sample_claim, "anchor-1")

    assert result.status == "FAIL"
    assert result.evidence is None
    assert len(corrupted_bytes) == 0  # Memory wiped


def test_invalid_trust_anchor_id(harness, sample_asset_bytes, sample_claim):
    """Verify empty trust_anchor_id raises MalformedEvidenceException."""
    with pytest.raises(MalformedEvidenceException):
        harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, "")

    assert len(sample_asset_bytes) == 0


def test_evidence_signature_verification(harness, sample_asset_bytes, sample_claim):
    """Verify emitted EvidencePayload signature passes cryptographic verification."""
    result = harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, "anchor-1")

    ev = result.evidence
    payload_dict = {
        "claim_id": ev.claim_id,
        "asset_hash": ev.asset_hash,
        "timestamp": ev.timestamp,
        "nonce": ev.nonce,
        "status": ev.status,
        "trust_anchor_id": ev.trust_anchor_id,
    }

    is_valid_sig = verify_evidence_signature(payload_dict, ev.signature, DEFAULT_TEST_DOMAIN_KEY)
    assert is_valid_sig is True


def test_no_disk_persistence(harness, sample_asset_bytes, sample_claim):
    """Verify zero disk file write calls occur during Option H evaluation."""
    with patch("builtins.open") as mock_open:
        result = harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, "anchor-1")
        assert result.status == "PASS"
        mock_open.assert_not_called()


def test_integration_with_assurance_loop(harness, sample_asset_bytes, sample_claim):
    """Verify end-to-end flow: Harness -> AssuranceLoopController -> ExecutionGate."""
    assurance_controller = AssuranceLoopController()
    execution_gate = ExecutionGate(assurance_controller)

    # 1. Start claim (state UNUNKNOWN -> UNVERIFIED)
    assurance_controller.ingest_claim_start(sample_claim.claim_id)
    assert assurance_controller.get_current_state() == EpistemicState.UNVERIFIED
    assert execution_gate.is_permitted() is False

    # 2. Evaluate claim using Option H Harness
    eval_result = harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, "anchor-1")
    assert eval_result.status == "PASS"

    # 3. Submit evidence to IF-ASSURE-001 (state UNVERIFIED -> VERIFIED)
    new_state = assurance_controller.update_epistemic_state(eval_result.evidence)
    assert new_state == EpistemicState.VERIFIED
    assert execution_gate.is_permitted() is True

    # 4. Request gate execution
    gate_resp = execution_gate.request_execution("render_artwork", lambda: "ARTWORK_RENDERED")
    assert gate_resp.permitted is True
    assert gate_resp.execution_output == "ARTWORK_RENDERED"


def test_replay_of_harness_evidence(harness, sample_asset_bytes, sample_claim):
    """Verify re-submitting harness-generated evidence to AssuranceLoop triggers ReplayAttackException."""
    assurance_controller = AssuranceLoopController()
    assurance_controller.ingest_claim_start(sample_claim.claim_id)

    eval_result = harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, "anchor-1")
    ev = eval_result.evidence

    # First ingestion succeeds
    assurance_controller.update_epistemic_state(ev)
    assert assurance_controller.get_current_state() == EpistemicState.VERIFIED

    # Transition to STALE
    assurance_controller.trigger_stale()

    # Transition to UNVERIFIED for re-evaluation
    assurance_controller.ingest_claim_start("claim-2")

    # Re-submitting same evidence payload triggers replay attack detection and BLOCKS
    with pytest.raises(ReplayAttackException):
        assurance_controller.update_epistemic_state(ev)

    assert assurance_controller.get_current_state() == EpistemicState.BLOCKED


def test_concurrent_harness_evaluations(harness):
    """Verify 10 concurrent threads running Option H evaluation execute without data races or memory corruption."""
    import concurrent.futures

    def worker(i):
        asset = bytearray(f"THREAD_RAW_ASSET_DATA_{i}".encode("utf-8"))
        salt = generate_salt(32)
        h = compute_salted_commitment(asset, salt)
        claim = VerificationClaim(
            claim_id=f"claim-thread-{i}",
            target_property="hash_match",
            expected_salted_hash=h,
            salt=salt
        )
        res = harness.evaluate_asset_claim(asset, claim, "anchor-thread")
        assert res.status == "PASS"
        assert len(asset) == 0  # Memory wiped
        return res.evidence.nonce

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        nonces = list(executor.map(worker, range(10)))

    # All 10 nonces generated concurrently must be distinct
    assert len(set(nonces)) == 10


def test_exception_traceback_does_not_leak_raw_bytes(harness):
    """Verify stringified exception objects contain zero raw asset bytes."""
    sensitive_bytes = bytearray(b"CONFIDENTIAL_SECRET_IMAGE_BYTES_12345")
    invalid_claim = None

    with pytest.raises(MalformedEvidenceException) as exc_info:
        harness.evaluate_asset_claim(sensitive_bytes, invalid_claim, "anchor-1")

    err_msg = str(exc_info.value)
    assert "CONFIDENTIAL_SECRET" not in err_msg
    assert "12345" not in err_msg


def test_salt_uniqueness_and_entropy():
    """Verify generate_salt produces unique 32-byte cryptographic salts."""
    salts = [generate_salt(32) for _ in range(100)]
    assert len(salts) == 100
    assert len(set(salts)) == 100
    assert all(len(s) == 32 for s in salts)


def test_modified_evidence_fields_rejection(harness, sample_asset_bytes, sample_claim):
    """Verify modifying timestamp, nonce, or asset_hash invalidates HMAC signature."""
    result = harness.evaluate_asset_claim(sample_asset_bytes, sample_claim, "anchor-1")
    ev = result.evidence

    base_payload = {
        "claim_id": ev.claim_id,
        "asset_hash": ev.asset_hash,
        "timestamp": ev.timestamp,
        "nonce": ev.nonce,
        "status": ev.status,
        "trust_anchor_id": ev.trust_anchor_id,
    }

    # 1. Modified timestamp
    mod_ts_payload = dict(base_payload, timestamp=ev.timestamp + 100.0)
    assert verify_evidence_signature(mod_ts_payload, ev.signature, DEFAULT_TEST_DOMAIN_KEY) is False

    # 2. Modified nonce
    mod_nonce_payload = dict(base_payload, nonce="tampered-nonce-999")
    assert verify_evidence_signature(mod_nonce_payload, ev.signature, DEFAULT_TEST_DOMAIN_KEY) is False

    # 3. Modified asset_hash
    mod_hash_payload = dict(base_payload, asset_hash="tampered_hash_value")
    assert verify_evidence_signature(mod_hash_payload, ev.signature, DEFAULT_TEST_DOMAIN_KEY) is False


def test_short_salt_rejection(sample_asset_bytes):
    """Verify salt of less than 32 bytes raises ValueError."""
    short_salt = b"short_salt_16"
    with pytest.raises(ValueError) as exc_info:
        compute_salted_commitment(sample_asset_bytes, short_salt)
    assert "at least 32 bytes" in str(exc_info.value)


def test_direct_unauthorized_transition_to_verified_rejected():
    """Verify direct state transition from UNKNOWN to VERIFIED is forbidden."""
    from security_substrate.epistemic_state import EpistemicState, validate_transition
    from security_substrate.exceptions import InvalidStateTransitionException

    with pytest.raises(InvalidStateTransitionException):
        validate_transition(EpistemicState.UNKNOWN, EpistemicState.VERIFIED)


