"""
Phase 10 — Execution Ledger Unit Tests
"""

import os
import shutil
import tempfile
import pytest

from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.execution_ledger import ExecutionLedger, ExecutionLedgerRecord


@pytest.fixture
def temp_ledger_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_execution_ledger_save_and_load(temp_ledger_dir):
    ledger = ExecutionLedger(base_dir=temp_ledger_dir)

    record = ExecutionLedgerRecord(
        execution_id="exec_999",
        action_id="act_100",
        workflow_id="wf_100",
        authorization_id="auth_100",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope="brand:aura",
        decision_reference="DEC_99",
        start_time="2026-09-05T14:00:00Z",
        end_time="2026-09-05T14:00:01Z",
        status="SUCCESS",
        output_summary={"post_id": "sandbox_post_1"},
    )

    path = ledger.record_execution(record)
    assert os.path.exists(path)

    loaded = ledger.load_execution("exec_999")
    assert loaded.action_id == "act_100"
    assert loaded.status == "SUCCESS"
    assert loaded.compute_hash() == record.compute_hash()
