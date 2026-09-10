"""
Unit tests for Phase 15 Studio Operational Scheduler.
"""

import pytest
from datetime import datetime, timezone, timedelta
from src.studio_operations.operational_scheduler import StudioOperationalScheduler

def test_operational_scheduler():
    sched = StudioOperationalScheduler()
    now_str = datetime.now(timezone.utc).isoformat()
    task = sched.schedule_task(
        requesting_client_id="client_nocap",
        schedule_id="sched_001",
        client_id="client_nocap",
        campaign_id="camp_001",
        workstream_id="ws_001",
        task_name="Weekly Content Planning",
        task_type="RESEARCH",
        scheduled_time=now_str
    )
    assert task.status == "SCHEDULED"

    due = sched.get_due_tasks("client_nocap")
    assert len(due) == 1
    assert due[0].schedule_id == "sched_001"

    completed = sched.mark_completed("client_nocap", "sched_001")
    assert completed.status == "COMPLETED"
