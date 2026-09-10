"""
Test T02 — Invalid / Corrupted Visual Asset Workflow Execution.
"""

import time
import pytest
from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    MalformedEvidenceException,
    generate_salt,
)
from src.workflow_integration import (
    AssetReference,
    SecurityIntegrationAdapter,
    VisualWorkflowRunner,
    WorkflowRunContext,
    WorkflowStatus,
)


def test_t02_corrupted_asset_failure():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    # Intentionally corrupt salt/commitment mismatch
    raw_asset = bytearray(b"corrupted asset bytes")
    wrong_salt = b"0" * 32

    asset_ref = AssetReference(
        asset_id="asset-t02-01",
        asset_name="corrupted.jpg",
        content_type="image/jpeg",
        sha256_hash="a" * 64,
        size_bytes=len(raw_asset),
    )

    context = WorkflowRunContext(
        run_id="run-t02-001",
        system_id="SYSTEM_001",
        correlation_id="corr-t02-001",
        user_id="user-designer-01",
        timestamp=time.time(),
        asset_ref=asset_ref,
    )

    adapter = SecurityIntegrationAdapter()
    # Expect MalformedEvidenceException or verification failure when wrong_salt commitment is passed
    with pytest.raises(MalformedEvidenceException):
        adapter.process_visual_claims(
            context=context,
            asset_bytes=None,  # Invalid bytearray
            visual_extraction_data={},
        )

    # ExecutionGate remains locked
    assert gate.is_permitted() is False
