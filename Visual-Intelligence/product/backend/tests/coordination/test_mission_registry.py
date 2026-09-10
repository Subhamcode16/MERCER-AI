"""
Unit tests for Phase 12 Mission Registry & Admission Control.
"""

import pytest

from src.coordination.mission_registry import MissionRegistry
from src.coordination.models import MissionPriority
from src.coordination.exceptions import MissionAdmissionDenied


def test_mission_registry_admission():
    reg = MissionRegistry(max_concurrent_missions=2)

    m1 = reg.admit_mission("m1", priority=MissionPriority.HIGH)
    m2 = reg.admit_mission("m2", priority=MissionPriority.NORMAL)

    assert reg.active_count == 2
    assert reg.get_mission("m1").status == "ADMITTED"

    # Excess admission beyond cap raises MissionAdmissionDenied
    with pytest.raises(MissionAdmissionDenied):
        reg.admit_mission("m3")


def test_mission_registry_duplicate_admission_rejection():
    reg = MissionRegistry()
    reg.admit_mission("m1")

    with pytest.raises(MissionAdmissionDenied):
        reg.admit_mission("m1")
