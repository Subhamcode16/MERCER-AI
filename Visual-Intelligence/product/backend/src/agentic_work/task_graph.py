"""
IF-AGENT-005 Bounded Task Graph & Workflow Engine.
Manages DAG task dependencies, sequential & parallel execution,
retry bounds, and max 3 revision loop limits before escalating to BLOCKED.
"""

import time
import threading
from typing import Dict, Any, List, Optional, Set
from .models import StaffTask, TaskStatus, StaffRole, StaffResult


class TaskGraph:
    """
    Bounded DAG task graph representation.
    """

    def __init__(self, workflow_id: str, max_revisions: int = 3) -> None:
        self.workflow_id = workflow_id
        self.max_revisions = max_revisions
        self._lock = threading.RLock()
        self._tasks: Dict[str, StaffTask] = {}
        self.revision_count: int = 0

    def add_task(self, task: StaffTask) -> None:
        if not isinstance(task, StaffTask):
            raise ValueError("task must be a valid StaffTask instance")
        with self._lock:
            self._tasks[task.task_id] = task

    def get_task(self, task_id: str) -> Optional[StaffTask]:
        with self._lock:
            return self._tasks.get(task_id)

    def get_ready_tasks(self) -> List[StaffTask]:
        """
        Returns list of tasks whose dependencies are COMPLETED and status is PENDING or READY.
        """
        with self._lock:
            ready = []
            for task in self._tasks.values():
                if task.status in (TaskStatus.PENDING, TaskStatus.READY):
                    # Check dependencies
                    deps_met = True
                    for dep_id in task.dependencies:
                        dep_task = self._tasks.get(dep_id)
                        if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                            deps_met = False
                            break
                    if deps_met:
                        task.status = TaskStatus.READY
                        ready.append(task)
            return ready

    def mark_completed(self, task_id: str, output: Dict[str, Any]) -> None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.status = TaskStatus.COMPLETED
                task.output = output
                task.completed_at = time.time()

    def mark_failed(self, task_id: str, error: str) -> None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.status = TaskStatus.FAILED
                task.error = error
                task.completed_at = time.time()

    def request_revision(self, task_id: str, critique_findings: List[str]) -> bool:
        """
        Requests a revision loop for a task.
        Bounded to max_revisions (3). Escalates to BLOCKED if limit exceeded.
        """
        with self._lock:
            self.revision_count += 1
            if self.revision_count > self.max_revisions:
                for t in self._tasks.values():
                    t.status = TaskStatus.BLOCKED
                    t.error = f"Max revision limit ({self.max_revisions}) exceeded. Escalated to BLOCKED."
                return False

            task = self._tasks.get(task_id)
            if task:
                task.status = TaskStatus.REVISION_REQUIRED
                task.attempt += 1
                task.inputs["revision_findings"] = critique_findings
                task.status = TaskStatus.READY
                return True
            return False

    def is_finished(self) -> bool:
        with self._lock:
            for task in self._tasks.values():
                if task.status not in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.BLOCKED, TaskStatus.CANCELLED):
                    return False
            return True

    def is_successful(self) -> bool:
        with self._lock:
            for task in self._tasks.values():
                if task.status != TaskStatus.COMPLETED:
                    return False
            return True
