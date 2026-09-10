"""
Phase 13 Integration Circuit Breaker.

Enforces provider failure containment (INV-13-009). Trips to OPEN state after 3 consecutive
failures, blocking external execution attempts without mutating security policy.
"""

from enum import Enum
from datetime import datetime, timezone, timedelta
import threading
from typing import Dict
from src.integration_boundary.exceptions import IntegrationCircuitOpenError


class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class IntegrationCircuitBreaker:
    """Circuit breaker for external provider health and failure containment."""

    def __init__(self, failure_threshold: int = 3, recovery_timeout_seconds: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds

        self._states: Dict[str, CircuitState] = {}
        self._consecutive_failures: Dict[str, int] = {}
        self._opened_at: Dict[str, datetime] = {}
        self._lock = threading.Lock()

    def check_state(self, provider_id: str, current_time: datetime = None) -> None:
        """
        Validates circuit state for provider_id.
        Raises IntegrationCircuitOpenError if state is OPEN.
        """
        now = current_time or datetime.now(timezone.utc)

        with self._lock:
            state = self._states.get(provider_id, CircuitState.CLOSED)

            if state == CircuitState.OPEN:
                opened_time = self._opened_at.get(provider_id, now)
                if now - opened_time > timedelta(seconds=self.recovery_timeout_seconds):
                    # Transition to HALF_OPEN to test recovery
                    self._states[provider_id] = CircuitState.HALF_OPEN
                else:
                    raise IntegrationCircuitOpenError(
                        f"Integration Circuit Breaker OPEN (INV-13-009): Provider '{provider_id}' is temporarily blocked due to repeated failures."
                    )

    def record_success(self, provider_id: str) -> None:
        """Records successful execution, resetting failure counters."""
        with self._lock:
            self._states[provider_id] = CircuitState.CLOSED
            self._consecutive_failures[provider_id] = 0
            self._opened_at.pop(provider_id, None)

    def record_failure(self, provider_id: str, current_time: datetime = None) -> None:
        """Records provider failure, incrementing failure counter and opening circuit if threshold reached."""
        now = current_time or datetime.now(timezone.utc)

        with self._lock:
            count = self._consecutive_failures.get(provider_id, 0) + 1
            self._consecutive_failures[provider_id] = count

            if count >= self.failure_threshold:
                self._states[provider_id] = CircuitState.OPEN
                self._opened_at[provider_id] = now

    def get_state(self, provider_id: str) -> CircuitState:
        """Returns current state for a provider."""
        with self._lock:
            return self._states.get(provider_id, CircuitState.CLOSED)
