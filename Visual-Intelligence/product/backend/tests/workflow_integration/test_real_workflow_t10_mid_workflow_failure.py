"""
Test T10 — Mid-Workflow Partial Stage Failure Handling.
"""

import time
from src.security_substrate import AssuranceLoopController, ExecutionGate
from src.workflow_integration import (
    AssetReference,
    VisualWorkflowRunner,
    WorkflowRunContext,
    WorkflowStatus,
)


def test_t10_mid_workflow_failure_handled_gracefully():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    # Force failure by passing malformed extraction data
    raw_asset = bytearray(b"failure test bytes")
    asset_ref = AssetReference(
        asset_id="asset-t10-01",
        asset_name="failure.jpg",
        content_type="image/jpeg",
        sha256_hash="e" * 64,
        size_bytes=len(raw_asset),
    )

    context = WorkflowRunContext(
        run_id="run-t10-001",
        system_id="SYSTEM_001",
        correlation_id="corr-t10-001",
        user_id="user-designer-01",
        timestamp=time.time(),
        asset_ref=asset_ref,
    )

    runner = VisualWorkflowRunner(execution_gate=gate)

    # Pass invalid salt format to trigger failure inside security adapter
    result = runner.run_workflow(
        context=context,
        asset_bytes=raw_asset,
        salt=b"short",  # Invalid salt (must be at least 16/32 bytes)
    )

    assert result.status == WorkflowStatus.FAILED
    assert result.failure_reason is not None
    assert result.execution_gate_permitted is False
    assert gate.is_permitted() is False
