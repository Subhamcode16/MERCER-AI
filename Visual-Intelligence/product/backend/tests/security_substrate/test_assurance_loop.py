"""
Unit tests for IF-ASSURE-001 AssuranceLoopController and state transitions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import time
import pytest
from security_substrate.epistemic_state import EpistemicState
from security_substrate.assurance_loop import (
    AssuranceLoopController,
    EvidencePayload,
    EpistemicStateStore,
)
from security_substrate.exceptions import (
    ReplayAttackException,
    StaleTimestampException,
    MalformedEvidenceException,
    InvalidStateTransitionException,
    FailClosedException,
)


@pytest.fixture
def assurance_controller():
    return AssuranceLoopController()


def create_valid_evidence(
    claim_id: str = "claim-101",
    nonce: str = "nonce-abc-123",
    timestamp: float = None,
    status: str = "PASS",
    trust_anchor_id: str = "anchor-sha256-xyz"
) -> EvidencePayload:
    return EvidencePayload(
        claim_id=claim_id,
        asset_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        signature="sig-ed25519-valid-sample",
        timestamp=timestamp if timestamp is not None else time.time(),
        nonce=nonce,
        status=status,
        trust_anchor_id=trust_anchor_id
    )


def test_initial_state(assurance_controller):
    """Verify initial epistemic state is UNKNOWN."""
    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN


def test_successful_verification_flow(assurance_controller):
    """Verify UNKNOWN -> UNVERIFIED -> VERIFIED transition path."""
    state1 = assurance_controller.ingest_claim_start("claim-101")
    assert state1 == EpistemicState.UNVERIFIED

    evidence = create_valid_evidence(claim_id="claim-101", nonce="nonce-001")
    state2 = assurance_controller.update_epistemic_state(evidence)
    assert state2 == EpistemicState.VERIFIED
    assert assurance_controller.get_current_state() == EpistemicState.VERIFIED


def test_replay_attack_detection(assurance_controller):
    """Verify replaying a consumed nonce triggers ReplayAttackException and sets BLOCKED."""
    assurance_controller.ingest_claim_start("claim-101")
    evidence1 = create_valid_evidence(nonce="reuse-nonce-999")
    assurance_controller.update_epistemic_state(evidence1)
    assert assurance_controller.get_current_state() == EpistemicState.VERIFIED

    # Re-ingest new claim with replayed nonce
    assurance_controller.trigger_stale()
    assurance_controller.ingest_claim_start("claim-102")
    evidence2 = create_valid_evidence(claim_id="claim-102", nonce="reuse-nonce-999")

    with pytest.raises(ReplayAttackException):
        assurance_controller.update_epistemic_state(evidence2)

    assert assurance_controller.get_current_state() == EpistemicState.BLOCKED


def test_stale_timestamp_detection(assurance_controller):
    """Verify evidence > 900s old triggers StaleTimestampException and sets BLOCKED."""
    assurance_controller.ingest_claim_start("claim-101")
    old_timestamp = time.time() - 905.0  # 15 min 5 sec old
    stale_evidence = create_valid_evidence(timestamp=old_timestamp)

    with pytest.raises(StaleTimestampException):
        assurance_controller.update_epistemic_state(stale_evidence)

    assert assurance_controller.get_current_state() == EpistemicState.BLOCKED


def test_malformed_evidence_payload(assurance_controller):
    """Verify incomplete or non-passing evidence triggers MalformedEvidenceException and sets BLOCKED."""
    assurance_controller.ingest_claim_start("claim-101")

    # Empty field
    malformed = create_valid_evidence(claim_id="")
    with pytest.raises(MalformedEvidenceException):
        assurance_controller.update_epistemic_state(malformed)
    assert assurance_controller.get_current_state() == EpistemicState.BLOCKED

    # Non-passing status
    assurance_controller2 = AssuranceLoopController()
    assurance_controller2.ingest_claim_start("claim-102")
    failed_evidence = create_valid_evidence(status="FAIL")
    with pytest.raises(MalformedEvidenceException):
        assurance_controller2.update_epistemic_state(failed_evidence)
    assert assurance_controller2.get_current_state() == EpistemicState.BLOCKED


def test_recovery_reset_flow(assurance_controller):
    """Verify RECOVERY_REQUIRED -> UNKNOWN reset flow, and that recovery NEVER sets VERIFIED directly."""
    assurance_controller.trigger_panic()
    assert assurance_controller.get_current_state() == EpistemicState.RECOVERY_REQUIRED

    # Valid recovery auth resets state strictly to UNKNOWN
    new_state = assurance_controller.execute_recovery_reset(recovery_auth_valid=True)
    assert new_state == EpistemicState.UNKNOWN
    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN

    # Verify recovery cannot directly set VERIFIED
    assurance_controller.trigger_panic()
    with pytest.raises(InvalidStateTransitionException):
        assurance_controller.store.transition_to(EpistemicState.VERIFIED)


def test_invalid_recovery_auth(assurance_controller):
    """Verify invalid recovery authorization forces BLOCKED state."""
    assurance_controller.trigger_panic()
    with pytest.raises(FailClosedException):
        assurance_controller.execute_recovery_reset(recovery_auth_valid=False)
    assert assurance_controller.get_current_state() == EpistemicState.BLOCKED


def test_restart_semantics(assurance_controller):
    """Verify process restart resets state to UNKNOWN and clears in-memory nonce cache."""
    assurance_controller.ingest_claim_start("claim-101")
    evidence = create_valid_evidence(nonce="nonce-restart-test")
    assurance_controller.update_epistemic_state(evidence)
    assert assurance_controller.get_current_state() == EpistemicState.VERIFIED

    # Simulate process restart
    restarted_controller = AssuranceLoopController()
    assert restarted_controller.get_current_state() == EpistemicState.UNKNOWN
    assert not restarted_controller.nonce_cache.has_nonce("nonce-restart-test")
