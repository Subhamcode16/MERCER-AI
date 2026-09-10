"""
Test T09 — Concurrent Real Workflow Runs.
"""

import hashlib
import threading
import time
from src.security_substrate import AssuranceLoopController, ExecutionGate
from src.workflow_integration import (
    AssetReference,
    VisualWorkflowRunner,
    WorkflowRunContext,
    WorkflowStatus,
)


def test_t09_concurrent_workflow_runs():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    runner = VisualWorkflowRunner(execution_gate=gate)
    results = []
    errors = []

    def _worker(idx: int):
        try:
            raw_asset = bytearray(f"concurrent asset bytes {idx}".encode("utf-8"))
            asset_hash = hashlib.sha256(raw_asset).hexdigest()

            asset_ref = AssetReference(
                asset_id=f"asset-t09-{idx}",
                asset_name=f"garment_{idx}.jpg",
                content_type="image/jpeg",
                sha256_hash=asset_hash,
                size_bytes=len(raw_asset),
            )

            context = WorkflowRunContext(
                run_id=f"run-t09-{idx:03d}",
                system_id="SYSTEM_001",
                correlation_id=f"corr-t09-{idx:03d}",
                user_id=f"user-{idx}",
                timestamp=time.time(),
                asset_ref=asset_ref,
            )

            res = runner.run_workflow(context=context, asset_bytes=raw_asset)
            results.append(res)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=_worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(results) == 10
    for res in results:
        assert res.status == WorkflowStatus.RECONCILED
        assert res.execution_gate_permitted is False

    assert gate.is_permitted() is False
