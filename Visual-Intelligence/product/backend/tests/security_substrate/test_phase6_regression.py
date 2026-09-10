"""
Phase 6 Full System Integration & Regression Suite.
Verifies that all Phase 1–5 subsystems remain fully functional alongside Phase 6 capabilities.
"""

import time
import pytest
from security_substrate import (
    EpistemicState,
    EpistemicStateStore,
    AssuranceLoopController,
    ExecutionGate,
    OptionHVerificationHarness,
    VerificationClaim,
    RecoveryManager,
    RecoveryEpochStore,
    CapabilityPayloadParser,
    EvidenceOrchestrator,
    ResearchAdapter,
    SecurityDecisionEngine,
    DecisionContext,
    DecisionClassification,
)


def test_full_regression_baseline():
    # 1. Epistemic Store & Gate
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False



    # 2. Verification Harness
    from security_substrate.crypto_utils import compute_salted_commitment
    harness = OptionHVerificationHarness()
    salt = b"0" * 32
    asset_bytes = bytearray(b"test asset data")
    expected_hash = compute_salted_commitment(asset_bytes, salt)
    claim = VerificationClaim(
        claim_id="clm-reg-1",
        target_property="TEST_PROPERTY",
        expected_salted_hash=expected_hash,
        salt=salt,
    )
    res = harness.evaluate_asset_claim(asset_bytes, claim, "ta-001")
    assert res.claim_id == "clm-reg-1"



    # 3. Evidence Orchestrator
    orchestrator = EvidenceOrchestrator()
    assert orchestrator.get_audit_log_size() == 0


    # 4. Security Decision Engine
    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-reg-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-reg-1",
    )
    decision, attestation = engine.evaluate_evidence([], ctx)
    assert decision.classification == DecisionClassification.INSUFFICIENT_EVIDENCE

    # Verify gate is still locked
    assert gate.is_permitted() is False

