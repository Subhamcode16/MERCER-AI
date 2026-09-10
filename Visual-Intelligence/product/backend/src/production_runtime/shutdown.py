"""
Phase 23 Two-Phase Graceful Shutdown Coordinator.
"""
import asyncio
import logging
import time
from typing import Dict, Any
from src.production_runtime.process_manager import ProcessManager
from src.production_runtime.worker_manager import WorkerManager
from src.production_runtime.queue_runtime import ProductionQueueRuntime
from src.production_runtime.exceptions import GracefulShutdownTimeout

logger = logging.getLogger(__name__)

class ShutdownCoordinator:
    """Coordinates a safe two-phase graceful shutdown: cutoff ingress then drain active workers."""

    def __init__(self, process_mgr: ProcessManager, worker_mgr: WorkerManager, queue_runtime: ProductionQueueRuntime, drain_timeout_seconds: float = 30.0):
        self.process_mgr = process_mgr
        self.worker_mgr = worker_mgr
        self.queue_runtime = queue_runtime
        self.drain_timeout_seconds = drain_timeout_seconds
        self.is_shutdown = False

    async def execute_shutdown(self) -> Dict[str, Any]:
        """Executes the two-phase shutdown."""
        start_time = time.time()
        logger.warning("Initiating Phase 23 Two-Phase Graceful Shutdown...")

        # Phase 1: Cut off ingress and mark draining
        self.process_mgr.mark_draining()
        self.worker_mgr.set_draining()
        logger.info("Shutdown Phase 1 complete: Ingress stopped, workers set to DRAINING.")

        # Phase 2: Drain in-flight worker tasks
        deadline = start_time + self.drain_timeout_seconds
        while self.worker_mgr.active_worker_count > 0:
            if time.time() > deadline:
                logger.error(f"Graceful shutdown timed out after {self.drain_timeout_seconds}s. {self.worker_mgr.active_worker_count} workers still active.")
                self.process_mgr.mark_stopped()
                self.is_shutdown = True
                raise GracefulShutdownTimeout(f"Shutdown exceeded {self.drain_timeout_seconds}s timeout")
            await asyncio.sleep(0.1)

        self.process_mgr.mark_stopped()
        self.is_shutdown = True
        elapsed = time.time() - start_time
        logger.info(f"Shutdown Phase 2 complete: All workers drained in {round(elapsed, 2)}s.")

        return {
            "success": True,
            "elapsed_seconds": round(elapsed, 2),
            "final_status": self.process_mgr.status.value,
            "unprocessed_queue_depth": self.queue_runtime.total_depth
        }
