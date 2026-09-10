"""
Phase 11 Mission Scheduler.

Provides bounded, event-driven scheduling for mission tasks with priority queues,
delay handling, and authorization expiration validation.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
import heapq

from .exceptions import MissionPolicyViolationError, AuthorizationRequiredError


class ScheduleMode(Enum):
    """Modes of scheduling for mission tasks."""
    RUN_NOW = "RUN_NOW"
    RUN_AT = "RUN_AT"
    RUN_AFTER = "RUN_AFTER"
    WAIT_FOR_DEPENDENCY = "WAIT_FOR_DEPENDENCY"
    RETRY = "RETRY"
    RESUME = "RESUME"


@dataclass(order=True)
class ScheduledItem:
    """Prioritized queue item for the mission scheduler."""
    scheduled_time: float  # Unix timestamp for priority queue sorting
    priority: int           # Lower value = higher priority
    task_id: str = field(compare=False)
    mission_id: str = field(compare=False)
    mode: ScheduleMode = field(compare=False)
    authorization_expiry: Optional[datetime] = field(default=None, compare=False)


class MissionScheduler:
    """Bounded, priority-driven scheduler for mission tasks."""

    def __init__(self):
        self._heap: List[ScheduledItem] = []

    def schedule_task(
        self,
        mission_id: str,
        task_id: str,
        mode: ScheduleMode = ScheduleMode.RUN_NOW,
        run_at: Optional[datetime] = None,
        priority: int = 10,
        authorization_expiry: Optional[datetime] = None,
        current_time: Optional[datetime] = None
    ) -> ScheduledItem:
        """Schedules a task for execution after validating timing and authorization expiry bounds."""
        now = current_time or datetime.now(timezone.utc)

        if run_at and run_at.tzinfo is None:
            run_at = run_at.replace(tzinfo=timezone.utc)

        # Invariant check: Cannot schedule execution beyond authorization expiry window
        if authorization_expiry:
            if authorization_expiry.tzinfo is None:
                authorization_expiry = authorization_expiry.replace(tzinfo=timezone.utc)

            scheduled_timestamp = run_at if run_at else now
            if scheduled_timestamp > authorization_expiry:
                raise AuthorizationRequiredError(
                    f"Scheduled time ({scheduled_timestamp.isoformat()}) exceeds authorization expiration ({authorization_expiry.isoformat()})."
                )

        target_ts = run_at.timestamp() if run_at else now.timestamp()
        item = ScheduledItem(
            scheduled_time=target_ts,
            priority=priority,
            task_id=task_id,
            mission_id=mission_id,
            mode=mode,
            authorization_expiry=authorization_expiry,
        )

        heapq.heappush(self._heap, item)
        return item

    def pop_ready_tasks(self, current_time: Optional[datetime] = None) -> List[ScheduledItem]:
        """Pops and returns all tasks whose scheduled time is less than or equal to current_time."""
        now_ts = (current_time or datetime.now(timezone.utc)).timestamp()
        ready = []

        while self._heap and self._heap[0].scheduled_time <= now_ts:
            item = heapq.heappop(self._heap)
            ready.append(item)

        return ready

    def peek_next(self) -> Optional[ScheduledItem]:
        """Peeks at the next task in queue without removing it."""
        return self._heap[0] if self._heap else None

    @property
    def queue_size(self) -> int:
        """Returns the number of pending tasks in the scheduler."""
        return len(self._heap)
