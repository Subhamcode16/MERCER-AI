"""
Phase 22 Runtime Control: Health & Readiness Checkers
------------------------------------------------------
Evaluates system liveness, readiness, and upstream dependency health without leaking internals.
"""

from typing import Dict, Any, List
from enum import Enum
import time

class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"

class HealthChecker:
    """Evaluates core control plane liveness."""

    def __init__(self, app_version: str = "22.0.0"):
        self.app_version = app_version
        self.started_at = time.time()

    def check_liveness(self) -> Dict[str, Any]:
        uptime_seconds = time.time() - self.started_at
        return {
            "status": HealthStatus.HEALTHY.value,
            "version": self.app_version,
            "uptime_seconds": round(uptime_seconds, 2),
            "timestamp": time.time(),
        }

class ReadinessChecker:
    """Verifies that all required control plane sub-systems are loaded and ready."""

    def __init__(self):
        self._subsystems_ready: Dict[str, bool] = {
            "runtime_config": True,
            "model_gateway": True,
            "visual_gateway": True,
            "mcp_gateway": True,
            "workforce_registry": True,
            "security_substrate": True,
        }

    def set_subsystem_status(self, subsystem: str, is_ready: bool) -> None:
        self._subsystems_ready[subsystem] = is_ready

    def check_readiness(self) -> Dict[str, Any]:
        all_ready = all(self._subsystems_ready.values())
        return {
            "ready": all_ready,
            "status": HealthStatus.HEALTHY.value if all_ready else HealthStatus.UNHEALTHY.value,
            "subsystems": dict(self._subsystems_ready),
            "timestamp": time.time(),
        }

class DependencyHealthChecker:
    """Monitors live external dependencies (LLM APIs, MCP endpoints, Vector Stores)."""

    def __init__(self):
        self._dependencies: Dict[str, Dict[str, Any]] = {}

    def record_dependency(self, name: str, status: HealthStatus, latency_ms: float, detail: str = "") -> None:
        self._dependencies[name] = {
            "status": status.value,
            "latency_ms": latency_ms,
            "detail": detail,
            "last_checked": time.time(),
        }

    def check_dependencies(self) -> Dict[str, Any]:
        if not self._dependencies:
            return {"status": HealthStatus.HEALTHY.value, "dependencies": {}, "summary": "No external dependencies registered"}
        
        has_unhealthy = any(d["status"] == HealthStatus.UNHEALTHY.value for d in self._dependencies.values())
        has_degraded = any(d["status"] == HealthStatus.DEGRADED.value for d in self._dependencies.values())
        
        overall = HealthStatus.UNHEALTHY if has_unhealthy else (HealthStatus.DEGRADED if has_degraded else HealthStatus.HEALTHY)
        return {
            "status": overall.value,
            "dependencies": self._dependencies,
            "timestamp": time.time(),
        }
