"""
Test T05 — Phase 4 Research Evidence Injection in Real Workflow Execution.
"""

import time
from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    DEFAULT_TRUST_MARKER_RESEARCH,
)
from src.workflow_integration import (
    AssetReference,
    SecurityIntegrationAdapter,
    WorkflowRunContext,
)


def test_t05_research_evidence_injection_remains_non_production():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    raw_asset = bytearray(b"research asset bytes")
    asset_ref = AssetReference(
        asset_id="asset-t05-01",
        asset_name="research.jpg",
        content_type="image/jpeg",
        sha256_hash="d" * 64,
        size_bytes=len(raw_asset),
    )

    context = WorkflowRunContext(
        run_id="run-t05-001",
        system_id="SYSTEM_001",
        correlation_id="corr-t05-001",
        user_id="user-researcher-01",
        timestamp=time.time(),
        asset_ref=asset_ref,
    )

    adapter = SecurityIntegrationAdapter()
    # Inject research evidence trust marker
    evidence_rec, decision, attestation, audit_rec, recon_res = adapter.process_visual_claims(
        context=context,
        asset_bytes=raw_asset,
        visual_extraction_data={"raw_claims": []},
        custom_trust_marker=DEFAULT_TRUST_MARKER_RESEARCH,
    )

    assert evidence_rec.trust_marker == DEFAULT_TRUST_MARKER_RESEARCH
    assert decision.classification.value == "RESEARCH_ONLY"
    assert gate.is_permitted() is False
