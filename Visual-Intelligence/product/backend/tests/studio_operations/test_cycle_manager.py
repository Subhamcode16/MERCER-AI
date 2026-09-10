"""
Unit tests for Phase 15 Studio Cycle Manager.
"""

import pytest
from src.studio_operations.cycle_manager import StudioCycleManager

def test_studio_cycle_lifecycle():
    mgr = StudioCycleManager()
    cycle = mgr.start_cycle("client_nocap", "cyc_001", "camp_001", "client_nocap", cycle_number=1)
    assert cycle.status == "IN_PROGRESS"

    cycle = mgr.complete_cycle("client_nocap", "cyc_001")
    assert cycle.status == "COMPLETED"
    assert cycle.end_time is not None
