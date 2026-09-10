"""
Phase 15 Operational Scheduler.
Provides policy-compliant operational scheduling without bypassing security boundaries.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from src.studio_operations.exceptions import ScheduleConflictError, ClientContextViolation

@dataclass
class ScheduledTask:
    schedule_id: str
    client_id: str
    campaign_id: str
    workstream_id: str
    task_name: str
    task_type: str  # RESEARCH, DRAFT, REVIEW, APPROVAL_REMINDER, OBSERVATION
    scheduled_time: str
    status: str = "SCHEDULED"  # SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED
    requires_authorization: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class StudioOperationalScheduler:
    """Manages scheduled operational tasks across client campaigns."""

    def __init__(self):
        self._schedules: Dict[str, ScheduledTask] = {}

    def schedule_task(
        self,
        requesting_client_id: str,
        schedule_id: str,
        client_id: str,
        campaign_id: str,
        workstream_id: str,
        task_name: str,
        task_type: str,
        scheduled_time: str,
        requires_authorization: bool = False
    ) -> ScheduledTask:
        """Schedules a new operational task."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot schedule task for client '{client_id}' from context '{requesting_client_id}'."
            )
        if schedule_id in self._schedules:
            raise ScheduleConflictError(f"Schedule ID '{schedule_id}' already exists.")

        task = ScheduledTask(
            schedule_id=schedule_id,
            client_id=client_id,
            campaign_id=campaign_id,
            workstream_id=workstream_id,
            task_name=task_name,
            task_type=task_type,
            scheduled_time=scheduled_time,
            requires_authorization=requires_authorization
        )
        self._schedules[schedule_id] = task
        return task

    def get_due_tasks(self, requesting_client_id: str, current_time: Optional[str] = None) -> List[ScheduledTask]:
        """Retrieves scheduled tasks due at or before current_time."""
        now = datetime.fromisoformat(current_time) if current_time else datetime.now(timezone.utc)
        due = []
        for task in self._schedules.values():
            if task.client_id == requesting_client_id and task.status == "SCHEDULED":
                sched_dt = datetime.fromisoformat(task.scheduled_time)
                if sched_dt <= now:
                    due.append(task)
        return due

    def mark_completed(self, requesting_client_id: str, schedule_id: str) -> ScheduledTask:
        """Marks a scheduled task as completed."""
        if schedule_id not in self._schedules:
            raise ScheduleConflictError(f"Schedule '{schedule_id}' not found.")
        task = self._schedules[schedule_id]
        if requesting_client_id != task.client_id:
            raise ClientContextViolation("Client isolation violation.")
        task.status = "COMPLETED"
        return task
