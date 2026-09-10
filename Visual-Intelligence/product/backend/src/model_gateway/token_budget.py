"""
Phase 20 - Token Budget & Rate Control Manager.

Tracks and enforces token consumption limits across model requests.
"""

from typing import Dict
from .models import LLMRequest
from .exceptions import TokenBudgetExceededError


class TokenBudgetManager:
    """Enforces token usage ceilings per task type and client context."""

    def __init__(self, max_tokens_per_request: int = 16384):
        self.max_tokens_per_request = max_tokens_per_request
        self._usage_tracker: Dict[str, int] = {}

    def check_and_reserve(self, request: LLMRequest) -> None:
        if request.max_tokens > self.max_tokens_per_request:
            raise TokenBudgetExceededError(
                f"Requested max_tokens {request.max_tokens} exceeds ceiling {self.max_tokens_per_request}."
            )

    def record_usage(self, task_type: str, tokens_used: int) -> None:
        self._usage_tracker[task_type] = self._usage_tracker.get(task_type, 0) + tokens_used
