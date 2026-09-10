"""
Phase 20 - MCP Circuit Breaker.

Prevents cascade failures by opening circuit breaker when external MCP server failures spike.
"""

from typing import Dict
from .exceptions import MCPCircuitBreakerOpenError


class MCPCircuitBreaker:
    """Manages failure thresholds and circuit states for external MCP servers."""

    def __init__(self, failure_threshold: int = 5):
        self.failure_threshold = failure_threshold
        self._failures: Dict[str, int] = {}
        self._state: Dict[str, str] = {}  # server_id -> "CLOSED" or "OPEN"

    def check_state(self, server_id: str) -> None:
        if self._state.get(server_id) == "OPEN":
            raise MCPCircuitBreakerOpenError(f"Circuit breaker for server '{server_id}' is OPEN.")

    def record_failure(self, server_id: str) -> None:
        count = self._failures.get(server_id, 0) + 1
        self._failures[server_id] = count
        if count >= self.failure_threshold:
            self._state[server_id] = "OPEN"

    def record_success(self, server_id: str) -> None:
        self._failures[server_id] = 0
        self._state[server_id] = "CLOSED"
