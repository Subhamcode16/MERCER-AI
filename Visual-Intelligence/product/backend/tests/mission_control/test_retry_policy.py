"""
Unit tests for Phase 11 Bounded Retry Engine.
"""

import pytest

from src.mission_control.retry_policy import RetryPolicy, BackoffStrategy
from src.mission_control.exceptions import (
    RetryExhaustedError,
    SecurityBoundaryViolation,
    AuthorizationRequiredError,
)


def test_transient_error_retry():
    policy = RetryPolicy(max_attempts=3, backoff_strategy=BackoffStrategy.EXPONENTIAL)

    # Transient error (e.g., ConnectionError) is retryable
    delay = policy.evaluate_retry(attempt_count=1, exc=ConnectionError("Timeout"))
    assert delay > 0.0

    # Reaching max_attempts raises RetryExhaustedError
    with pytest.raises(RetryExhaustedError):
        policy.evaluate_retry(attempt_count=3, exc=ConnectionError("Timeout"))


def test_security_error_non_retryable():
    policy = RetryPolicy(max_attempts=5)

    # Security violations MUST NOT be retried (0 attempts allowed)
    with pytest.raises(SecurityBoundaryViolation):
        policy.evaluate_retry(attempt_count=1, exc=SecurityBoundaryViolation("Unauthorized capability"))

    with pytest.raises(AuthorizationRequiredError):
        policy.evaluate_retry(attempt_count=1, exc=AuthorizationRequiredError("Token missing"))
