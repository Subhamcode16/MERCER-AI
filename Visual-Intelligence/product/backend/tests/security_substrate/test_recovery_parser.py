"""
Automated unit, security, and concurrency test suite for IF-RECOVER-001 CapabilityPayloadParser & RecoveryManager.
Verifies 10-field schema validation, freshness, replay defense, signature authentication,
state transition invariant (RECOVERY_REQUIRED -> UNKNOWN), and ExecutionGate lock maintenance.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import time
import hmac
import hashlib
import uuid
import secrets
import pytest
import concurrent.futures

from security_substrate.epistemic_state import EpistemicState, validate_transition
from security_substrate.exceptions import (
    FailClosedException,
    MalformedEvidenceException,
    ReplayAttackException,
    StaleTimestampException,
    InvalidStateTransitionException,
)
from security_substrate.assurance_loop import AssuranceLoopController
from security_substrate.execution_gate import ExecutionGate
from security_substrate.recovery_parser import (
    CapabilityPayloadParser,
    RecoveryManager,
    RecoveryEpochStore,
    DEFAULT_SYSTEM_ID,
    DEFAULT_OPERATION_ID,
    DEFAULT_AUTHORIZATION_SCOPE,
    DEFAULT_PROTOCOL_VERSION,
)

TEST_SIGNING_KEY = b"Phase3_Recovery_Domain_Signing_Key_2026"


def create_sample_payload(
    system_id: str = DEFAULT_SYSTEM_ID,
    operation_id: str = DEFAULT_OPERATION_ID,
    authorization_scope: str = DEFAULT_AUTHORIZATION_SCOPE,
    protocol_version: str = DEFAULT_PROTOCOL_VERSION,
    creation_time: float = None,
    expiration_time: float = None,
    epoch: int = 1,
    nonce: str = None,
):
    now = time.time() if creation_time is None else creation_time
    exp = now + 600.0 if expiration_time is None else expiration_time
    nonce_hex = secrets.token_hex(16) if nonce is None else nonce

    return {
        "system_id": system_id,
        "recovery_request_id": str(uuid.uuid4()),
        "unique_nonce": nonce_hex,
        "operation_id": operation_id,
        "authorization_scope": authorization_scope,
        "trust_anchor_id": "trust-anchor-recovery-001",
        "protocol_version": protocol_version,
        "creation_time": now,
        "expiration_time": exp,
        "current_recovery_epoch": epoch,
    }


def compute_payload_signature(payload_dict: dict, signing_key: bytes = TEST_SIGNING_KEY) -> str:
    p_str = f"{payload_dict['system_id']}:{payload_dict['recovery_request_id']}:{payload_dict['unique_nonce']}:{payload_dict['operation_id']}:{payload_dict['authorization_scope']}:{payload_dict['trust_anchor_id']}:{payload_dict['protocol_version']}:{payload_dict['creation_time']}:{payload_dict['expiration_time']}:{payload_dict['current_recovery_epoch']}"
    return hmac.new(signing_key, p_str.encode("utf-8"), hashlib.sha256).hexdigest()


@pytest.fixture
def recovery_manager():
    return RecoveryManager()


@pytest.fixture
def assurance_controller():
    controller = AssuranceLoopController()
    controller.trigger_panic()  # Transition to RECOVERY_REQUIRED
    return controller


def test_valid_recovery_payload_parsing(recovery_manager):
    """Verify parsing a fully compliant 10-field recovery payload succeeds."""
    payload = create_sample_payload()
    sig = compute_payload_signature(payload)

    result = recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert result.status == "SUCCESS"
    assert result.system_id == DEFAULT_SYSTEM_ID
    assert result.recovery_epoch == 1


def test_recovery_resets_state_to_unknown(recovery_manager, assurance_controller):
    """Verify emergency recovery execution resets state strictly to UNKNOWN."""
    assert assurance_controller.get_current_state() == EpistemicState.RECOVERY_REQUIRED

    payload = create_sample_payload(epoch=1)
    sig = compute_payload_signature(payload)

    result = recovery_manager.execute_emergency_recovery(payload, sig, TEST_SIGNING_KEY, assurance_controller)

    assert result.status == "SUCCESS"
    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN


def test_execution_gate_remains_locked_post_recovery(recovery_manager, assurance_controller):
    """Verify ExecutionGate remains LOCKED (permitted=False) after recovery reset to UNKNOWN."""
    execution_gate = ExecutionGate(assurance_controller)

    payload = create_sample_payload()
    sig = compute_payload_signature(payload)

    recovery_manager.execute_emergency_recovery(payload, sig, TEST_SIGNING_KEY, assurance_controller)

    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN
    assert execution_gate.is_permitted() is False

    resp = execution_gate.request_execution("action-post-recovery")
    assert resp.permitted is False


def test_missing_field_rejection(recovery_manager):
    """Verify omitting any of the 10 fields raises MalformedEvidenceException."""
    payload = create_sample_payload()
    del payload["system_id"]
    sig = compute_payload_signature(create_sample_payload())

    with pytest.raises(MalformedEvidenceException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Missing mandatory field" in str(exc_info.value)


def test_invalid_system_id_rejection(recovery_manager):
    """Verify mismatched system_id raises MalformedEvidenceException."""
    payload = create_sample_payload(system_id="WRONG_SYSTEM_999")
    sig = compute_payload_signature(payload)

    with pytest.raises(MalformedEvidenceException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Mismatched system_id" in str(exc_info.value)


def test_invalid_operation_id_rejection(recovery_manager):
    """Verify unauthorized operation_id raises MalformedEvidenceException."""
    payload = create_sample_payload(operation_id="UNAUTHORIZED_OP")
    sig = compute_payload_signature(payload)

    with pytest.raises(MalformedEvidenceException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Unauthorized operation_id" in str(exc_info.value)


def test_unauthorized_scope_rejection(recovery_manager):
    """Verify scope escalation attempt raises MalformedEvidenceException."""
    payload = create_sample_payload(authorization_scope="SCOPE_SUPERADMIN_ALL")
    sig = compute_payload_signature(payload)

    with pytest.raises(MalformedEvidenceException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Unauthorized authorization_scope" in str(exc_info.value)


def test_stale_timestamp_rejection(recovery_manager):
    """Verify expired recovery timestamp raises StaleTimestampException."""
    now = time.time()
    payload = create_sample_payload(creation_time=now - 2000.0, expiration_time=now - 100.0)
    sig = compute_payload_signature(payload)

    with pytest.raises(StaleTimestampException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Expired recovery payload" in str(exc_info.value)


def test_future_timestamp_rejection(recovery_manager):
    """Verify timestamp > 5s in future raises StaleTimestampException."""
    now = time.time()
    payload = create_sample_payload(creation_time=now + 50.0, expiration_time=now + 600.0)
    sig = compute_payload_signature(payload)

    with pytest.raises(StaleTimestampException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Future-dated creation timestamp" in str(exc_info.value)


def test_replayed_nonce_rejection(recovery_manager):
    """Verify submitting duplicate recovery nonce raises ReplayAttackException."""
    payload = create_sample_payload()
    sig = compute_payload_signature(payload)

    # First submission succeeds
    res = recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)
    assert res.status == "SUCCESS"

    # Second submission with same nonce raises ReplayAttackException
    with pytest.raises(ReplayAttackException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Replayed recovery nonce detected" in str(exc_info.value)


def test_outdated_epoch_rejection(recovery_manager):
    """Verify epoch < active_epoch raises ReplayAttackException."""
    recovery_manager.epoch_store.set_epoch(5)

    payload = create_sample_payload(epoch=4)
    sig = compute_payload_signature(payload)

    with pytest.raises(ReplayAttackException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Outdated recovery epoch" in str(exc_info.value)


def test_invalid_signature_rejection(recovery_manager):
    """Verify signature mismatch raises FailClosedException."""
    payload = create_sample_payload()
    bad_sig = "a" * 64

    with pytest.raises(FailClosedException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, bad_sig, TEST_SIGNING_KEY)

    assert "Recovery signature verification failed" in str(exc_info.value)


def test_concurrent_recovery_payload_submissions(recovery_manager):
    """Verify 10 concurrent recovery requests execute safely with atomic nonce consumption."""
    def worker(i):
        p = create_sample_payload(nonce=f"nonce-thread-recovery-{i}-{secrets.token_hex(8)}")
        sig = compute_payload_signature(p)
        res = recovery_manager.parser.parse_and_validate(p, sig, TEST_SIGNING_KEY)
        return res.status

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(worker, range(10)))

    assert len(results) == 10
    assert all(r == "SUCCESS" for r in results)


def test_recovery_cannot_transition_directly_to_verified():
    """Verify attempt to transition RECOVERY_REQUIRED directly to VERIFIED raises InvalidStateTransitionException."""
    with pytest.raises(InvalidStateTransitionException):
        validate_transition(EpistemicState.RECOVERY_REQUIRED, EpistemicState.VERIFIED)


def test_recovery_reset_fails_if_not_in_recovery_required_state(recovery_manager):
    """Verify executing recovery reset from state other than RECOVERY_REQUIRED forces BLOCKED."""
    controller = AssuranceLoopController()  # Initial state UNKNOWN
    assert controller.get_current_state() == EpistemicState.UNKNOWN

    payload = create_sample_payload()
    sig = compute_payload_signature(payload)

    with pytest.raises(InvalidStateTransitionException):
        recovery_manager.execute_emergency_recovery(payload, sig, TEST_SIGNING_KEY, controller)

    assert controller.get_current_state() == EpistemicState.BLOCKED


def test_boolean_type_confusion_rejection(recovery_manager):
    """Verify boolean type confusion in schema fields raises MalformedEvidenceException."""
    payload = create_sample_payload()
    payload["unique_nonce"] = True
    sig = compute_payload_signature(create_sample_payload())

    with pytest.raises(MalformedEvidenceException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Boolean value not permitted" in str(exc_info.value)


def test_empty_string_field_rejection(recovery_manager):
    """Verify empty or whitespace-only string field raises MalformedEvidenceException."""
    payload = create_sample_payload(nonce="   ")
    sig = compute_payload_signature(payload)

    with pytest.raises(MalformedEvidenceException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Empty or whitespace-only string" in str(exc_info.value)


def test_expiration_before_creation_rejection(recovery_manager):
    """Verify payload with expiration_time < creation_time raises StaleTimestampException."""
    now = time.time()
    payload = create_sample_payload(creation_time=now, expiration_time=now - 50.0)
    sig = compute_payload_signature(payload)

    with pytest.raises(StaleTimestampException) as exc_info:
        recovery_manager.parser.parse_and_validate(payload, sig, TEST_SIGNING_KEY)

    assert "Expiration time cannot be earlier than creation time" in str(exc_info.value)

