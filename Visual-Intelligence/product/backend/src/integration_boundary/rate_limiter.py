"""
Phase 13 Integration Rate Limiter.

Enforces provider- and capability-scoped rate limits, burst caps, and sliding windows.
Raises ExternalRateLimitError when limits are exceeded.
"""

from datetime import datetime, timezone, timedelta
import threading
from typing import Dict, List
from src.integration_boundary.exceptions import ExternalRateLimitError


class ProviderRateLimiter:
    """Sliding-window token bucket rate limiter for external providers and capabilities."""

    def __init__(
        self,
        default_max_requests_per_minute: int = 60,
        default_burst_limit: int = 10,
    ):
        self.default_max_rpm = default_max_requests_per_minute
        self.default_burst_limit = default_burst_limit

        # key -> List[datetime]
        self._request_timestamps: Dict[str, List[datetime]] = {}
        self._lock = threading.Lock()

    def check_and_acquire(
        self,
        provider_id: str,
        capability_name: str,
        current_time: datetime = None
    ) -> None:
        """
        Validates rate limit for (provider_id, capability_name).
        Raises ExternalRateLimitError if sliding window or burst limit is exceeded.
        """
        now = current_time or datetime.now(timezone.utc)
        key = f"{provider_id}:{capability_name}"
        one_minute_ago = now - timedelta(minutes=1)
        one_second_ago = now - timedelta(seconds=1)

        with self._lock:
            timestamps = self._request_timestamps.get(key, [])
            # Filter timestamps within 1 minute
            timestamps = [ts for ts in timestamps if ts > one_minute_ago]

            # 1. Burst limit check (last 1 second)
            recent_burst = sum(1 for ts in timestamps if ts > one_second_ago)
            if recent_burst >= self.default_burst_limit:
                raise ExternalRateLimitError(
                    f"Provider Burst Rate Limit Exceeded: Burst limit ({self.default_burst_limit}/sec) reached for '{key}'."
                )

            # 2. Sliding window RPM check
            if len(timestamps) >= self.default_max_rpm:
                raise ExternalRateLimitError(
                    f"Provider Rate Limit Exceeded: Max requests per minute ({self.default_max_rpm}/min) reached for '{key}'."
                )

            timestamps.append(now)
            self._request_timestamps[key] = timestamps
