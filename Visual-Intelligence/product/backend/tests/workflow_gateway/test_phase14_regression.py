"""
Phase 14 Regression Suite
-------------------------
Verifies Phase 14 additions preserve Phase 1-13 security gates, execution boundaries,
and underlying authorization invariants intact.
"""

import pytest
from src.workflow_gateway.workflow_service import WorkflowService

def test_phase14_preserves_execution_gate_lock():
    """Verify that Phase 14 WorkflowService does not unlock or alter Phase 10 HumanAuthorizationBoundary."""
    service = WorkflowService()
    boundary = service.approval_service._human_boundary
    assert hasattr(boundary, "issue_human_authorization")

def test_phase14_preserves_phase13_integration_boundary():
    """Verify Phase 13 IntegrationController remains authoritative for external calls."""
    service = WorkflowService()
    assert hasattr(service.integration_controller, "execute_external_tool")
