"""
Concurrency & Race Condition tests for Phase 12 (20+ Concurrent Admissions & Thread Safety).
"""

import threading
import pytest

from src.coordination.coordinator import MultiMissionCoordinator
from src.coordination.models import MissionPriority, ResourceRequest


def test_concurrent_mission_admissions_thread_safety(tmp_path):
    coord = MultiMissionCoordinator(max_concurrent_missions=25, ledger_dir=str(tmp_path))
    admitted_ids = []
    errors = []
    lock = threading.Lock()

    def worker(i: int):
        m_id = f"m_thread_{i:02d}"
        try:
            coord.admit_mission(
                mission_id=m_id,
                title=f"Title {i}",
                description="Desc",
                target_outcomes=[],
                priority=MissionPriority.NORMAL,
            )
            with lock:
                admitted_ids.append(m_id)
        except Exception as e:
            with lock:
                errors.append(e)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(25)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(admitted_ids) == 25
    assert len(errors) == 0
    assert coord.mission_registry.active_count == 25
