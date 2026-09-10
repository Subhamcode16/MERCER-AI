"""
Unit tests for Phase 11 Mission Scheduler.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.mission_control.scheduler import MissionScheduler, ScheduleMode
from src.mission_control.exceptions import AuthorizationRequiredError


def test_scheduler_priority_and_popping():
    scheduler = MissionScheduler()
    now = datetime.now(timezone.utc)

    scheduler.schedule_task("m1", "t_low", priority=20, current_time=now)
    scheduler.schedule_task("m1", "t_high", priority=5, current_time=now)

    ready = scheduler.pop_ready_tasks(current_time=now)
    assert len(ready) == 2
    assert ready[0].task_id == "t_high"
    assert ready[1].task_id == "t_low"


def test_scheduler_authorization_expiry_boundary():
    scheduler = MissionScheduler()
    now = datetime.now(timezone.utc)
    expiry = now + timedelta(hours=1)
    future_run = now + timedelta(hours=2)

    # Scheduling beyond authorization expiry window raises AuthorizationRequiredError
    with pytest.raises(AuthorizationRequiredError):
        scheduler.schedule_task(
            mission_id="m1",
            task_id="t1",
            mode=ScheduleMode.RUN_AT,
            run_at=future_run,
            authorization_expiry=expiry,
            current_time=now,
        )
