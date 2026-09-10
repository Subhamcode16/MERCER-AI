"""
Phase 12 Capacity & Global Budget Engine.

Enforces system-wide model token consumption, staff task concurrency,
execution slot caps, and API rate-limit buckets across all active missions.
"""

import threading
from typing import Dict, Any, Optional

from .models import CoordinationBudget
from .exceptions import CoordinationBudgetExceeded


class CapacityTracker:
    """Thread-safe global capacity and budget tracker."""

    def __init__(self, global_budget: Optional[CoordinationBudget] = None):
        self.budget = global_budget or CoordinationBudget()
        self.consumed_tokens: int = 0
        self.active_staff_tasks: int = 0
        self.active_execution_slots: int = 0
        self.external_request_count: int = 0
        self._lock = threading.RLock()

    def record_token_consumption(self, tokens: int) -> None:
        """Records token consumption against global token budget."""
        with self._lock:
            if tokens < 0:
                raise ValueError("Token consumption cannot be negative.")
            if self.consumed_tokens + tokens > self.budget.global_max_tokens:
                raise CoordinationBudgetExceeded(
                    f"Global token budget exceeded ({self.consumed_tokens + tokens} > {self.budget.global_max_tokens})."
                )
            self.consumed_tokens += tokens

    def acquire_staff_slot(self) -> None:
        """Acquires an active staff task slot."""
        with self._lock:
            if self.active_staff_tasks + 1 > self.budget.global_max_concurrent_staff_tasks:
                raise CoordinationBudgetExceeded(
                    f"Global staff concurrency limit reached ({self.active_staff_tasks + 1} > {self.budget.global_max_concurrent_staff_tasks})."
                )
            self.active_staff_tasks += 1

    def release_staff_slot(self) -> None:
        """Releases an active staff task slot."""
        with self._lock:
            self.active_staff_tasks = max(0, self.active_staff_tasks - 1)

    def acquire_execution_slot(self) -> None:
        """Acquires an execution slot."""
        with self._lock:
            if self.active_execution_slots + 1 > self.budget.global_max_execution_slots:
                raise CoordinationBudgetExceeded(
                    f"Global execution slot limit reached ({self.active_execution_slots + 1} > {self.budget.global_max_execution_slots})."
                )
            self.active_execution_slots += 1

    def release_execution_slot(self) -> None:
        """Releases an execution slot."""
        with self._lock:
            self.active_execution_slots = max(0, self.active_execution_slots - 1)
