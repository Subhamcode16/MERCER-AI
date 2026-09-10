"""
Test T04 — Evidence Mutation Detection in Real Workflow Execution.
"""

import time
import pytest
from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    AttestationTamperedException,
    verify_attestation,
)
from src.workflow_integration import (
    AssetReference,
    SecurityIntegrationAdapter,
    WorkflowRunContext,
)


def test_t04_evidence_mutation_tamper_detected():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    raw_asset = bytearray(b"authentic asset bytes")
    asset_ref = AssetReference(
        asset_id="asset-t04-01",
        asset_name="authentic.jpg",
        content_type="image/jpeg",
        sha256_hash="c" * 64,
        size_bytes=len(raw_asset),
    )

    context = WorkflowRunContext(
        run_id="run-t04-001",
        system_id="SYSTEM_001",
        correlation_id="corr-t04-001",
        user_id="user-designer-01",
        timestamp=time.time(),
        asset_ref=asset_ref,
    )

    adapter = SecurityIntegrationAdapter()
    evidence_rec, decision, attestation, audit_rec, recon_res = adapter.process_visual_claims(
        context=context,
        asset_bytes=raw_asset,
        visual_extraction_data={"raw_claims": []},
    )

    # Verify authentic attestation passes
    assert verify_attestation(attestation, decision) is True

    # Mutate decision commitment inside attestation to simulate post-generation tampering
    from dataclasses import replace
    tampered_attestation = replace(attestation, decision_commitment="0" * 64)

    # Tampered attestation fails verification with AttestationTamperedException
    with pytest.raises(AttestationTamperedException):
        verify_attestation(tampered_attestation, decision)
    assert gate.is_permitted() is False
