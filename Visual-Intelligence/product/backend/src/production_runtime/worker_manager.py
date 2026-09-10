"""
Phase 23 Bounded Worker Management and Execution Pools.
"""
import asyncio
import logging
import time
from typing import Dict, Optional, List, Callable, Any
from src.production_runtime.runtime_models import WorkerDescriptor, WorkerStatus, RuntimeTask
from src.production_runtime.exceptions import WorkerLimitExceededError

logger = logging.getLogger(__name__)

class WorkerManager:
    """Manages a bounded pool of asynchronous worker tasks with per-tenant concurrency limits."""

    def __init__(self, max_global_workers: int = 16, max_tenant_workers: int = 4):
        self.max_global_workers = max_global_workers
        self.max_tenant_workers = max_tenant_workers
        self._workers: Dict[str, WorkerDescriptor] = {}
        self._active_tasks: Dict[str, asyncio.Task] = {}
        self._tenant_active_counts: Dict[str, int] = {}
        self._is_draining = False

        # Initialize worker descriptors
        for i in range(max_global_workers):
            wid = f"worker-{i+1:02d}"
            self._workers[wid] = WorkerDescriptor(worker_id=wid)

    @property
    def total_workers(self) -> int:
        return len(self._workers)

    @property
    def active_worker_count(self) -> int:
        return sum(1 for w in self._workers.values() if w.status == WorkerStatus.BUSY)

    @property
    def idle_worker_count(self) -> int:
        return sum(1 for w in self._workers.values() if w.status == WorkerStatus.IDLE)

    def allocate_worker(self, tenant_id: str, task: RuntimeTask) -> Optional[WorkerDescriptor]:
        """Allocates an idle worker for a tenant subject to global and tenant concurrency limits."""
        if self._is_draining:
            return None

        tenant_count = self._tenant_active_counts.get(tenant_id, 0)
        if tenant_count >= self.max_tenant_workers:
            logger.warning(f"Tenant {tenant_id} reached max worker limit ({self.max_tenant_workers})")
            raise WorkerLimitExceededError(f"Tenant {tenant_id} exceeded worker quota of {self.max_tenant_workers}")

        for worker in self._workers.values():
            if worker.status == WorkerStatus.IDLE:
                worker.status = WorkerStatus.BUSY
                worker.current_task_id = task.task_id
                worker.tenant_id = tenant_id
                worker.last_heartbeat = time.time()
                self._tenant_active_counts[tenant_id] = tenant_count + 1
                return worker

        return None

    def release_worker(self, worker_id: str, success: bool = True) -> None:
        """Releases a busy worker back to the idle pool."""
        worker = self._workers.get(worker_id)
        if not worker:
            return

        tenant_id = worker.tenant_id
        if tenant_id and tenant_id in self._tenant_active_counts:
            self._tenant_active_counts[tenant_id] = max(0, self._tenant_active_counts[tenant_id] - 1)

        worker.status = WorkerStatus.IDLE
        worker.current_task_id = None
        worker.tenant_id = None
        worker.tasks_processed += 1
        if not success:
            worker.error_count += 1
        worker.last_heartbeat = time.time()

    def set_draining(self) -> None:
        self._is_draining = True

    def get_worker_status_summary(self) -> Dict[str, Any]:
        return {
            "max_global_workers": self.max_global_workers,
            "max_tenant_workers": self.max_tenant_workers,
            "active_workers": self.active_worker_count,
            "idle_workers": self.idle_worker_count,
            "tenant_allocations": dict(self._tenant_active_counts)
        }
