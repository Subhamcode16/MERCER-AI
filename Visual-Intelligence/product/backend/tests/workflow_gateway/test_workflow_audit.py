"""
Phase 14 Test Workflow Audit
----------------------------
Tests multi-ledger correlation across Phase 7, 10, 11, 12, and 13 ledgers.
"""

import pytest
from src.workflow_gateway.workflow_audit import WorkflowAuditCorrelator

def test_workflow_audit_correlation():
    correlator = WorkflowAuditCorrelator()
    summary = correlator.correlate_workflow_history(workflow_id="wf-aud-1", mission_id="m-aud-1")
    assert summary["workflow_id"] == "wf-aud-1"
    assert summary["mission_id"] == "m-aud-1"
    assert "correlated_at" in summary
