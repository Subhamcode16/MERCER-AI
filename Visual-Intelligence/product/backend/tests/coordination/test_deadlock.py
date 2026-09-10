"""
Unit tests for Phase 12 Deadlock Detector.
"""

import pytest
from datetime import datetime, timezone

from src.coordination.deadlock import DeadlockDetector
from src.coordination.models import CoordinationMission, MissionPriority


def test_deadlock_cycle_detection():
    detector = DeadlockDetector()

    # Wait-for graph containing cycle m1 -> m2 -> m3 -> m1
    wfg = {
        "m1": {"m2"},
        "m2": {"m3"},
        "m3": {"m1"},
    }

    cycle = detector.detect_deadlock(wfg)
    assert cycle is not None
    assert "m1" in cycle and "m2" in cycle and "m3" in cycle


def test_victim_selection():
    detector = DeadlockDetector()
    now = datetime.now(timezone.utc)

    m1 = CoordinationMission("m1", MissionPriority.HIGH, now)
    m2 = CoordinationMission("m2", MissionPriority.LOW, now)

    victim = detector.select_victim_mission(["m1", "m2"], [m1, m2])
    assert victim.mission_id == "m2"  # Lower priority selected as victim
