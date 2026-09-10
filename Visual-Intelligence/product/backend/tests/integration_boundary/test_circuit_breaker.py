"""
Unit tests for Phase 13 Integration Circuit Breaker (INV-13-009).
"""

from datetime import datetime, timezone, timedelta
import pytest

from src.integration_boundary.circuit_breaker import IntegrationCircuitBreaker, CircuitState
from src.integration_boundary.exceptions import IntegrationCircuitOpenError


def test_circuit_breaker_trips_to_open():
    cb = IntegrationCircuitBreaker(failure_threshold=3, recovery_timeout_seconds=30)
    now = datetime.now(timezone.utc)

    assert cb.get_state("mock_social") == CircuitState.CLOSED

    cb.record_failure("mock_social", current_time=now)
    cb.record_failure("mock_social", current_time=now)
    assert cb.get_state("mock_social") == CircuitState.CLOSED

    # 3rd failure trips circuit to OPEN
    cb.record_failure("mock_social", current_time=now)
    assert cb.get_state("mock_social") == CircuitState.OPEN

    # Execution check while OPEN raises IntegrationCircuitOpenError
    with pytest.raises(IntegrationCircuitOpenError):
        cb.check_state("mock_social", current_time=now)


def test_circuit_breaker_recovery_half_open():
    cb = IntegrationCircuitBreaker(failure_threshold=1, recovery_timeout_seconds=10)
    now = datetime.now(timezone.utc)

    cb.record_failure("mock_social", current_time=now)
    assert cb.get_state("mock_social") == CircuitState.OPEN

    # 15 seconds later (past recovery_timeout_seconds) -> transitions to HALF_OPEN
    later = now + timedelta(seconds=15)
    cb.check_state("mock_social", current_time=later)
    assert cb.get_state("mock_social") == CircuitState.HALF_OPEN

    # Successful call resets circuit to CLOSED
    cb.record_success("mock_social")
    assert cb.get_state("mock_social") == CircuitState.CLOSED
