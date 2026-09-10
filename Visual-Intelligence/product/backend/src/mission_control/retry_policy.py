"""
Phase 11 Bounded Retry Engine.

Implements INV-11-011: Strict retry policies distinguishing retryable transient errors
from non-retryable terminal security, authorization, and scope violations.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Set, Type

from .exceptions import (
    RetryExhaustedError,
    SecurityBoundaryViolation,
    AuthorizationRequiredError,
    MissionPolicyViolationError,
    MissionBudgetExceededError,
)


class BackoffStrategy(Enum):
    """Backoff delay calculation strategy."""
    FIXED = "FIXED"
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"


# Explicit list of non-retryable terminal security exceptions
TERMINAL_ERROR_CLASSES: Set[Type[Exception]] = {
    SecurityBoundaryViolation,
    AuthorizationRequiredError,
    MissionPolicyViolationError,
    MissionBudgetExceededError,
    PermissionError,
}


@dataclass
class RetryPolicy:
    """Configurable retry policy for mission tasks."""
    max_attempts: int = 3
    initial_delay_seconds: float = 1.0
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    backoff_factor: float = 2.0
    max_delay_seconds: float = 60.0

    def is_retryable(self, exc: Exception) -> bool:
        """Determines if an exception is retryable under security policy invariants."""
        # Non-negotiable invariant: Security & authorization failures are terminal
        for term_cls in TERMINAL_ERROR_CLASSES:
            if isinstance(exc, term_cls):
                return False
        return True

    def calculate_delay(self, attempt_count: int) -> float:
        """Calculates backoff delay based on strategy and current attempt index."""
        if attempt_count <= 0:
            return 0.0

        if self.backoff_strategy == BackoffStrategy.FIXED:
            delay = self.initial_delay_seconds
        elif self.backoff_strategy == BackoffStrategy.LINEAR:
            delay = self.initial_delay_seconds * attempt_count
        elif self.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            delay = self.initial_delay_seconds * (self.backoff_factor ** (attempt_count - 1))
        else:
            delay = self.initial_delay_seconds

        return min(delay, self.max_delay_seconds)

    def evaluate_retry(self, attempt_count: int, exc: Exception) -> float:
        """Evaluates whether to retry an exception; returns backoff delay or raises exception."""
        if not self.is_retryable(exc):
            raise exc

        if attempt_count >= self.max_attempts:
            raise RetryExhaustedError(
                f"Task failed after {attempt_count} attempts. Retry limit reached. Original error: {str(exc)}"
            )

        return self.calculate_delay(attempt_count)
