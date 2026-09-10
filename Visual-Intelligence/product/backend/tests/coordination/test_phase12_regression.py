"""
Regression verification test module for Phase 12 integration.
"""

import pytest

from src.coordination.coordinator import MultiMissionCoordinator
from src.security_substrate import ExecutionGate, AssuranceLoopController


def test_phase12_preserves_execution_gate_lock(tmp_path):
    """Verify Phase 12 initialization preserves ExecutionGate lock baseline."""
    coord = MultiMissionCoordinator(ledger_dir=str(tmp_path))
    gate = coord.phase11_coordinator.work_orchestrator.execution_gate
    assert gate.is_permitted() is False

