"""
Concurrency & Race Condition tests for Phase 11.
"""

import threading
import pytest

from src.mission_control.coordinator import MissionCoordinator


def test_concurrent_task_execution_lockout():
    coord = MissionCoordinator()
    coord.create_mission(
        mission_id="m_conc_1",
        title="Concurrency Test",
        description="Desc",
        target_outcomes=[],
        allowed_capabilities={"CREATE_DRAFT"},
    )
    coord.prepare_mission("m_conc_1")
    coord.add_task(mission_id="m_conc_1", task_id="t1", workflow_id="wf_1", assigned_role="RESEARCHER", description="R")
    coord.start_mission("m_conc_1")

    results = []

    def worker():
        try:
            res = coord.execute_next_task("m_conc_1")
            if res:
                results.append(res)
        except Exception as e:
            results.append(e)

    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # Exactly one worker successfully executes the single task
    executed = [r for r in results if isinstance(r, dict) and r.get("status") == "COMPLETED"]
    assert len(executed) == 1
