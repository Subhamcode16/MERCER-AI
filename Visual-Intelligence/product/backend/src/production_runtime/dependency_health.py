"""
Phase 23 Active Dependency Health Evaluation and Probing.
"""
import asyncio
import logging
import time
from typing import Dict, Any, Optional, Callable, Awaitable
from src.production_runtime.exceptions import DependencyUnhealthyError

logger = logging.getLogger(__name__)

class DependencyHealthMonitor:
    """Monitors live status of models, vision, MCP servers, and persistent stores."""

    def __init__(self):
        self._probes: Dict[str, Callable[[], Awaitable[bool]]] = {}
        self._status: Dict[str, Dict[str, Any]] = {}

    def register_probe(self, dependency_name: str, probe_fn: Callable[[], Awaitable[bool]], is_critical: bool = True) -> None:
        self._probes[dependency_name] = probe_fn
        self._status[dependency_name] = {
            "healthy": True,
            "is_critical": is_critical,
            "last_checked": 0.0,
            "consecutive_failures": 0,
            "last_error": None
        }

    async def evaluate_dependency(self, dependency_name: str) -> bool:
        if dependency_name not in self._probes:
            return False

        probe = self._probes[dependency_name]
        entry = self._status[dependency_name]
        try:
            is_healthy = await probe()
            entry["healthy"] = is_healthy
            entry["last_checked"] = time.time()
            if is_healthy:
                entry["consecutive_failures"] = 0
                entry["last_error"] = None
            else:
                entry["consecutive_failures"] += 1
            return is_healthy
        except Exception as e:
            entry["healthy"] = False
            entry["last_checked"] = time.time()
            entry["consecutive_failures"] += 1
            entry["last_error"] = str(e)
            logger.warning(f"Dependency probe failed for {dependency_name}: {e}")
            return False

    async def evaluate_all(self, fail_closed: bool = True) -> Dict[str, Any]:
        results = {}
        has_critical_failure = False

        for name in self._probes:
            healthy = await self.evaluate_dependency(name)
            results[name] = self._status[name]
            if not healthy and self._status[name]["is_critical"]:
                has_critical_failure = True

        if fail_closed and has_critical_failure:
            unhealthy = [k for k, v in results.items() if not v["healthy"] and v["is_critical"]]
            raise DependencyUnhealthyError(f"Critical dependencies unhealthy: {', '.join(unhealthy)}")

        return {
            "overall_healthy": not has_critical_failure,
            "dependencies": results,
            "timestamp": time.time()
        }
