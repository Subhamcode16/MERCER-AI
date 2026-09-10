"""
Test T01 — Successful End-to-End Visual Intelligence Workflow Execution.
"""

import hashlib
import time
from src.security_substrate import AssuranceLoopController, ExecutionGate
from src.workflow_integration import (
    AssetReference,
    VisualWorkflowRunner,
    WorkflowRunContext,
    WorkflowStatus,
)


def test_t01_successful_workflow_run():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    raw_asset = bytearray(b"sample visual textile asset bytes 2026")
    asset_hash = hashlib.sha256(raw_asset).hexdigest()

    asset_ref = AssetReference(
        asset_id="asset-t01-01",
        asset_name="banarasi_saree.jpg",
        content_type="image/jpeg",
        sha256_hash=asset_hash,
        size_bytes=len(raw_asset),
    )

    context = WorkflowRunContext(
        run_id="run-t01-001",
        system_id="SYSTEM_001",
        correlation_id="corr-t01-001",
        user_id="user-designer-01",
        timestamp=time.time(),
        asset_ref=asset_ref,
    )

    runner = VisualWorkflowRunner(execution_gate=gate)
    result = runner.run_workflow(context=context, asset_bytes=raw_asset)

    assert result.status == WorkflowStatus.RECONCILED
    assert result.run_id == "run-t01-001"
    assert result.decision_id is not None
    assert result.attestation_id is not None
    assert result.audit_sequence_number == 1
    assert result.reconciliation_status == "CONSISTENT"
    assert result.execution_gate_permitted is False

    # Non-authoritative invariant check
    assert gate.is_permitted() is False
