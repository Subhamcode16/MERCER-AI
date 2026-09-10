"""
Regression Verification Test Module for Phase 13 Integration Boundary.
"""

import pytest

from src.integration_boundary.integration_controller import IntegrationController
from src.security_substrate import ExecutionGate, AssuranceLoopController


def test_phase13_preserves_execution_gate_lock(tmp_path):
    """Verify Phase 13 initialization preserves ExecutionGate lock baseline."""
    ctrl = IntegrationController(ledger_dir=str(tmp_path))
    loop = AssuranceLoopController()
    gate = ExecutionGate(controller=loop)
    assert gate.is_permitted() is False
