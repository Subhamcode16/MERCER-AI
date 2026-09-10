"""
Unit tests for Phase 13 Provider Rate Limiter.
"""

from datetime import datetime, timezone, timedelta
import pytest

from src.integration_boundary.rate_limiter import ProviderRateLimiter
from src.integration_boundary.exceptions import ExternalRateLimitError


def test_rate_limiter_rpm_exhaustion():
    limiter = ProviderRateLimiter(default_max_requests_per_minute=3, default_burst_limit=10)
    now = datetime.now(timezone.utc)

    # 3 requests pass
    limiter.check_and_acquire("mock_social", "CREATE_DRAFT", current_time=now)
    limiter.check_and_acquire("mock_social", "CREATE_DRAFT", current_time=now)
    limiter.check_and_acquire("mock_social", "CREATE_DRAFT", current_time=now)

    # 4th request raises ExternalRateLimitError
    with pytest.raises(ExternalRateLimitError):
        limiter.check_and_acquire("mock_social", "CREATE_DRAFT", current_time=now)
