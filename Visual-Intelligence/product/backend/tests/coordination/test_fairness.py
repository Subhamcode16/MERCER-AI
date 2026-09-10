"""
Unit tests for Phase 12 Fairness & Aging Engine.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.coordination.fairness import FairnessEngine
from src.coordination.models import CoordinationMission, MissionPriority


def test_fairness_priority_aging():
    engine = FairnessEngine(starvation_threshold_seconds=10)
    now = datetime.now(timezone.utc)

    # Mission admitted 20 seconds ago (waited > threshold)
    m = CoordinationMission(
        mission_id="m_starved",
        priority=MissionPriority.LOW,  # Base priority value 5
        admission_timestamp=now - timedelta(seconds=25),
    )

    updated = engine.check_and_apply_aging([m], current_time=now)
    assert len(updated) == 1
    assert updated[0].aging_boost >= 2

    effective_prio = engine.calculate_effective_priority(updated[0], current_time=now)
    assert effective_prio < 5.0  # Priority rank improved
