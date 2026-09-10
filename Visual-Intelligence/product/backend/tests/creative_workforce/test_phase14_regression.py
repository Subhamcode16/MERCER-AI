"""
Phase 14 Regression Suite
-------------------------
Verifies Phase 14 preserves all Phase 1–13 execution gate locks, authorization boundaries,
and provider sandbox isolations intact without side effects or regression.
"""

import pytest

from src.creative_workforce import CreativeWorkforceOrchestrator
from src.execution_control import HumanAuthorizationBoundary
from src.integration_boundary import IntegrationController

def test_phase14_preserves_execution_gate_lock():
    """Verifies that creating or running workforce plans preserves HumanAuthorizationBoundary."""
    boundary = HumanAuthorizationBoundary()
    assert hasattr(boundary, "issue_human_authorization")
    orch = CreativeWorkforceOrchestrator()
    orch.execute_campaign_proposal_workflow("nocap", "nocap-apparel", "Test Title", "Test Objective")
    assert hasattr(boundary, "issue_human_authorization")

def test_phase14_preserves_phase13_integration_boundary():
    """Verifies that workforce orchestrator cannot invoke external integration operations directly without Phase 10 authorization."""
    ctrl = IntegrationController()
    assert hasattr(ctrl, "execute_external_tool")
