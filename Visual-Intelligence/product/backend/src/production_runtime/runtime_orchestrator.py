"""
Phase 23 Production Runtime Orchestrator.
"""
import logging
from typing import Dict, Any, Optional
from src.production_runtime.process_manager import ProcessManager
from src.production_runtime.worker_manager import WorkerManager
from src.production_runtime.queue_runtime import ProductionQueueRuntime
from src.production_runtime.dependency_health import DependencyHealthMonitor
from src.production_runtime.runtime_state import RuntimeStateManager
from src.production_runtime.startup import StartupCoordinator
from src.production_runtime.shutdown import ShutdownCoordinator
from src.production_runtime.runtime_models import RuntimeStateSnapshot

logger = logging.getLogger(__name__)

class ProductionRuntimeOrchestrator:
    """Master orchestrator integrating process supervision, bounded workers, queues, health, and state."""

    def __init__(self, max_global_workers: int = 16, max_tenant_workers: int = 4, max_queue_capacity: int = 1000):
        self.process_mgr = ProcessManager()
        self.worker_mgr = WorkerManager(max_global_workers=max_global_workers, max_tenant_workers=max_tenant_workers)
        self.queue_runtime = ProductionQueueRuntime(max_capacity=max_queue_capacity)
        self.health_monitor = DependencyHealthMonitor()
        self.state_mgr = RuntimeStateManager()

        self.startup_coordinator = StartupCoordinator(self.process_mgr, self.health_monitor)
        self.shutdown_coordinator = ShutdownCoordinator(self.process_mgr, self.worker_mgr, self.queue_runtime)

    async def start(self, verify_dependencies: bool = True) -> Dict[str, Any]:
        return await self.startup_coordinator.execute_startup(verify_dependencies=verify_dependencies)

    async def stop(self) -> Dict[str, Any]:
        return await self.shutdown_coordinator.execute_shutdown()

    def get_snapshot(self) -> RuntimeStateSnapshot:
        q_stats = self.queue_runtime.get_stats()
        w_stats = self.worker_mgr.get_worker_status_summary()
        p_metrics = self.process_mgr.get_metrics()

        return RuntimeStateSnapshot(
            process_id=self.process_mgr.pid,
            process_status=self.process_mgr.status,
            uptime_seconds=p_metrics["uptime_seconds"],
            active_workers=w_stats["active_workers"],
            idle_workers=w_stats["idle_workers"],
            queue_depth=q_stats["total_depth"],
            dead_letter_depth=q_stats["dead_letter_depth"],
            total_tasks_completed=q_stats["total_completed"],
            total_tasks_failed=q_stats["total_failed"],
            active_tenants=list(w_stats["tenant_allocations"].keys())
        )
