"""
Phase 23 Process Supervision and Lifecycle Manager.
"""
import os
import time
import logging
from typing import Dict, Any, Optional
from src.production_runtime.runtime_models import ProcessStatus, RuntimeStateSnapshot
from src.production_runtime.exceptions import ProcessCrashError

logger = logging.getLogger(__name__)

class ProcessManager:
    """Supervises host process state, uptime, resource thresholds, and health telemetry."""
    
    def __init__(self, max_memory_mb: float = 4096.0, max_cpu_percent: float = 90.0):
        self.pid = os.getpid()
        self.start_time = time.time()
        self.status = ProcessStatus.INITIALIZING
        self.max_memory_mb = max_memory_mb
        self.max_cpu_percent = max_cpu_percent
        self._restart_count = 0

    def mark_ready(self) -> None:
        self.status = ProcessStatus.RUNNING
        logger.info(f"Process {self.pid} marked RUNNING at {self.start_time}")

    def mark_draining(self) -> None:
        self.status = ProcessStatus.DRAINING
        logger.info(f"Process {self.pid} transitioned to DRAINING")

    def mark_stopped(self) -> None:
        self.status = ProcessStatus.STOPPED
        logger.info(f"Process {self.pid} transitioned to STOPPED")

    def mark_crashed(self, reason: str) -> None:
        self.status = ProcessStatus.CRASHED
        logger.error(f"Process {self.pid} CRASHED: {reason}")
        raise ProcessCrashError(f"Process {self.pid} crashed: {reason}")

    def get_uptime(self) -> float:
        return time.time() - self.start_time

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "pid": self.pid,
            "status": self.status.value,
            "uptime_seconds": round(self.get_uptime(), 2),
            "restart_count": self._restart_count,
            "memory_limit_mb": self.max_memory_mb,
            "cpu_limit_percent": self.max_cpu_percent
        }
