"""
Phase 23 Priority Task Queue Runtime with Multi-Tenant Isolation and Dead-Letter Queue (DLQ).
"""
import asyncio
import logging
import time
from typing import Dict, Optional, List, Any
from src.production_runtime.runtime_models import RuntimeTask, QueuePriority
from src.production_runtime.exceptions import QueueCapacityError

logger = logging.getLogger(__name__)

class ProductionQueueRuntime:
    """Async priority queue supporting multi-tenant isolation, capacity limits, and dead-letter handling."""

    def __init__(self, max_capacity: int = 1000, dlq_max_capacity: int = 500):
        self.max_capacity = max_capacity
        self.dlq_max_capacity = dlq_max_capacity
        self._queues: Dict[QueuePriority, asyncio.Queue] = {
            p: asyncio.Queue() for p in QueuePriority
        }
        self._dead_letter_queue: List[Dict[str, Any]] = []
        self._task_count = 0
        self._completed_count = 0
        self._failed_count = 0
        self._tenant_task_counts: Dict[str, int] = {}

    @property
    def total_depth(self) -> int:
        return sum(q.qsize() for q in self._queues.values())

    @property
    def dead_letter_depth(self) -> int:
        return len(self._dead_letter_queue)

    async def enqueue(self, task: RuntimeTask) -> None:
        """Enqueues a task into the appropriate priority queue."""
        if self.total_depth >= self.max_capacity:
            logger.error(f"Task queue capacity exceeded ({self.max_capacity})")
            raise QueueCapacityError(f"Task queue at maximum capacity: {self.max_capacity}")

        await self._queues[task.priority].put(task)
        self._task_count += 1
        self._tenant_task_counts[task.tenant_id] = self._tenant_task_counts.get(task.tenant_id, 0) + 1
        logger.debug(f"Enqueued task {task.task_id} (Priority: {task.priority.name}, Tenant: {task.tenant_id})")

    async def dequeue(self, timeout_seconds: float = 1.0) -> Optional[RuntimeTask]:
        """Dequeues the highest priority task available within timeout."""
        start = time.time()
        for priority in sorted(QueuePriority, key=lambda p: p.value):
            q = self._queues[priority]
            if not q.empty():
                task: RuntimeTask = await q.get()
                return task

        # If all queues empty, wait briefly on highest priority
        try:
            return await asyncio.wait_for(self._queues[QueuePriority.CRITICAL].get(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            return None

    def mark_completed(self, task: RuntimeTask) -> None:
        self._completed_count += 1
        if task.tenant_id in self._tenant_task_counts:
            self._tenant_task_counts[task.tenant_id] = max(0, self._tenant_task_counts[task.tenant_id] - 1)

    def route_to_dead_letter(self, task: RuntimeTask, failure_reason: str) -> None:
        """Routes a permanently failed task to the dead-letter queue."""
        self._failed_count += 1
        if task.tenant_id in self._tenant_task_counts:
            self._tenant_task_counts[task.tenant_id] = max(0, self._tenant_task_counts[task.tenant_id] - 1)

        dlq_entry = {
            "task_id": task.task_id,
            "tenant_id": task.tenant_id,
            "client_id": task.client_id,
            "action_name": task.action_name,
            "payload": task.payload,
            "retries_exhausted": task.retry_count,
            "failure_reason": failure_reason,
            "timestamp": time.time()
        }
        if len(self._dead_letter_queue) < self.dlq_max_capacity:
            self._dead_letter_queue.append(dlq_entry)
        else:
            self._dead_letter_queue.pop(0)
            self._dead_letter_queue.append(dlq_entry)

        logger.warning(f"Task {task.task_id} routed to DLQ: {failure_reason}")

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_depth": self.total_depth,
            "priority_depths": {p.name: self._queues[p].qsize() for p in QueuePriority},
            "dead_letter_depth": self.dead_letter_depth,
            "total_enqueued": self._task_count,
            "total_completed": self._completed_count,
            "total_failed": self._failed_count,
            "tenant_active_tasks": dict(self._tenant_task_counts)
        }
