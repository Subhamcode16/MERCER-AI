"""
Phase 24 Dynamic Provider Health & Circuit Breaker Manager.
"""
import time
import logging
from typing import Dict, Any, List
from enum import Enum

logger = logging.getLogger(__name__)

class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class ProviderHealthEngine:
    """Monitors live provider error rates and manages circuit-breaker states."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout_seconds: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self._provider_stats: Dict[str, Dict[str, Any]] = {}

    def record_call(self, provider_id: str, success: bool) -> None:
        if provider_id not in self._provider_stats:
            self._provider_stats[provider_id] = {
                "consecutive_failures": 0,
                "total_calls": 0,
                "circuit_state": CircuitState.CLOSED,
                "last_state_change": time.time()
            }

        stats = self._provider_stats[provider_id]
        stats["total_calls"] += 1

        if success:
            stats["consecutive_failures"] = 0
            if stats["circuit_state"] == CircuitState.HALF_OPEN:
                stats["circuit_state"] = CircuitState.CLOSED
                stats["last_state_change"] = time.time()
                logger.info(f"Circuit for {provider_id} CLOSED (recovered).")
        else:
            stats["consecutive_failures"] += 1
            if stats["consecutive_failures"] >= self.failure_threshold and stats["circuit_state"] == CircuitState.CLOSED:
                stats["circuit_state"] = CircuitState.OPEN
                stats["last_state_change"] = time.time()
                logger.error(f"Circuit for {provider_id} tripped OPEN after {self.failure_threshold} failures!")

    def is_provider_available(self, provider_id: str) -> bool:
        stats = self._provider_stats.get(provider_id)
        if not stats:
            return True

        if stats["circuit_state"] == CircuitState.OPEN:
            # Check for half-open trial
            if time.time() - stats["last_state_change"] > self.recovery_timeout_seconds:
                stats["circuit_state"] = CircuitState.HALF_OPEN
                stats["last_state_change"] = time.time()
                logger.info(f"Circuit for {provider_id} transitioned to HALF_OPEN trial.")
                return True
            return False

        return True

    def get_provider_status(self, provider_id: str) -> Dict[str, Any]:
        return self._provider_stats.get(provider_id, {
            "circuit_state": CircuitState.CLOSED.value,
            "consecutive_failures": 0,
            "total_calls": 0
        })
