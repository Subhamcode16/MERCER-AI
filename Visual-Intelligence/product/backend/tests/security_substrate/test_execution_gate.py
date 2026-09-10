"""
Unit tests for IF-EXECUTE-001 ExecutionGate pass-through lock behavior.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import time
import pytest
from security_substrate.epistemic_state import EpistemicState
from security_substrate.assurance_loop import AssuranceLoopController, EvidencePayload
from security_substrate.execution_gate import ExecutionGate
from security_substrate.exceptions import ExecutionGateLockedException, FailClosedException


@pytest.fixture
def assurance_controller():
    return AssuranceLoopController()


@pytest.fixture
def execution_gate(assurance_controller):
    return ExecutionGate(assurance_controller)


def test_gate_lock_across_all_states(assurance_controller, execution_gate):
    """Verify ExecutionGate permits execution ONLY when state is VERIFIED."""
    
    # 1. UNKNOWN
    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN
    resp = execution_gate.request_execution("action-1")
    assert resp.permitted is False

    # 2. UNVERIFIED
    assurance_controller.ingest_claim_start("claim-1")
    assert assurance_controller.get_current_state() == EpistemicState.UNVERIFIED
    resp = execution_gate.request_execution("action-1")
    assert resp.permitted is False

    # 3. VERIFIED
    ev = EvidencePayload(
        claim_id="claim-1",
        asset_hash="hash-1",
        signature="sig-1",
        timestamp=time.time(),
        nonce="nonce-gate-1",
        status="PASS",
        trust_anchor_id="anchor-1"
    )
    assurance_controller.update_epistemic_state(ev)
    assert assurance_controller.get_current_state() == EpistemicState.VERIFIED
    resp = execution_gate.request_execution("action-1")
    assert resp.permitted is True

    # 4. STALE
    assurance_controller.trigger_stale()
    assert assurance_controller.get_current_state() == EpistemicState.STALE
    resp = execution_gate.request_execution("action-1")
    assert resp.permitted is False

    # 5. REASSESSMENT_REQUIRED
    assurance_controller.store.transition_to(EpistemicState.UNVERIFIED)
    ev2 = EvidencePayload(
        claim_id="claim-2",
        asset_hash="hash-2",
        signature="sig-2",
        timestamp=time.time(),
        nonce="nonce-gate-2",
        status="PASS",
        trust_anchor_id="anchor-1"
    )
    assurance_controller.update_epistemic_state(ev2)
    assurance_controller.trigger_reassessment()
    assert assurance_controller.get_current_state() == EpistemicState.REASSESSMENT_REQUIRED
    resp = execution_gate.request_execution("action-1")
    assert resp.permitted is False

    # 6. RECOVERY_REQUIRED
    assurance_controller.trigger_panic()
    assert assurance_controller.get_current_state() == EpistemicState.RECOVERY_REQUIRED
    resp = execution_gate.request_execution("action-1")
    assert resp.permitted is False

    # 7. BLOCKED
    with pytest.raises(FailClosedException):
        assurance_controller.execute_recovery_reset(recovery_auth_valid=False)
    assert assurance_controller.get_current_state() == EpistemicState.BLOCKED
    resp = execution_gate.request_execution("action-1")
    assert resp.permitted is False


def test_execute_or_raise_behavior(assurance_controller, execution_gate):
    """Verify execute_or_raise executes closure when VERIFIED and raises ExecutionGateLockedException when locked."""
    
    # Locked in UNKNOWN
    with pytest.raises(ExecutionGateLockedException):
        execution_gate.execute_or_raise("action-1", lambda: "success")

    # Move to VERIFIED
    assurance_controller.ingest_claim_start("claim-1")
    ev = EvidencePayload(
        claim_id="claim-1",
        asset_hash="hash-1",
        signature="sig-1",
        timestamp=time.time(),
        nonce="nonce-raise-test",
        status="PASS",
        trust_anchor_id="anchor-1"
    )
    assurance_controller.update_epistemic_state(ev)

    output = execution_gate.execute_or_raise("action-1", lambda x: x * 2, 21)
    assert output == 42


def test_fault_injection_in_closure(assurance_controller, execution_gate):
    """Verify exceptions inside execution closure trigger FailClosedException."""
    assurance_controller.ingest_claim_start("claim-1")
    ev = EvidencePayload(
        claim_id="claim-1",
        asset_hash="hash-1",
        signature="sig-1",
        timestamp=time.time(),
        nonce="nonce-fault-test",
        status="PASS",
        trust_anchor_id="anchor-1"
    )
    assurance_controller.update_epistemic_state(ev)

    def faulty_closure():
        raise ValueError("Injected runtime failure inside callable")

    with pytest.raises(FailClosedException):
        execution_gate.request_execution("action-fault", faulty_closure)


def test_invalid_controller_initialization():
    """Verify initializing ExecutionGate without valid AssuranceLoopController raises FailClosedException."""
    with pytest.raises(FailClosedException):
        ExecutionGate(None)
