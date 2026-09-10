"""
Test T03 — Stale Evidence Detection in Real Workflow Execution.
"""

import time
import pytest
from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    StaleTimestampException,
)
from src.workflow_integration import (
    AssetReference,
    SecurityIntegrationAdapter,
    WorkflowRunContext,
)


def test_t03_stale_evidence_surfaced():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    raw_asset = bytearray(b"stale asset bytes")
    asset_ref = AssetReference(
        asset_id="asset-t03-01",
        asset_name="stale.jpg",
        content_type="image/jpeg",
        sha256_hash="b" * 64,
        size_bytes=len(raw_asset),
    )

    # Stale context (timestamp 2 hours ago)
    stale_time = time.time() - 7200.0
    context = WorkflowRunContext(
        run_id="run-t03-001",
        system_id="SYSTEM_001",
        correlation_id="corr-t03-001",
        user_id="user-designer-01",
        timestamp=stale_time,
        asset_ref=asset_ref,
    )

    adapter = SecurityIntegrationAdapter()
    with pytest.raises(StaleTimestampException):
        adapter.process_visual_claims(
            context=context,
            asset_bytes=raw_asset,
            visual_extraction_data={"raw_claims": []},
        )

    assert gate.is_permitted() is False
