"""
Phase 11 Hierarchical Mission Budget Engine.

Tracks runtime, task count, retries, sandbox execution count, generated assets, external requests,
and token consumption across parent missions and child workflows. Traps exhaustion in real time.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

from .mission_models import MissionBudget
from .exceptions import MissionBudgetExceededError


@dataclass
class BudgetUsage:
    """Current consumption counters for a mission."""
    elapsed_seconds: float = 0.0
    task_count: int = 0
    retry_count: int = 0
    execution_count: int = 0
    generated_assets: int = 0
    external_requests: int = 0
    tokens_consumed: int = 0


class MissionBudgetTracker:
    """Real-time budget exhaustion tracker and trap engine."""

    def __init__(self, budget: MissionBudget):
        self.budget = budget
        self.usage = BudgetUsage()

    def record_task_start(self) -> None:
        """Records a task start and checks task_count limit."""
        if self.usage.task_count + 1 > self.budget.max_tasks:
            raise MissionBudgetExceededError(
                f"Task limit exceeded ({self.usage.task_count + 1} > {self.budget.max_tasks})."
            )
        self.usage.task_count += 1

    def record_retry(self) -> None:
        """Records a retry attempt and checks retry limit."""
        if self.usage.retry_count + 1 > self.budget.max_retries:
            raise MissionBudgetExceededError(
                f"Retry budget exceeded ({self.usage.retry_count + 1} > {self.budget.max_retries})."
            )
        self.usage.retry_count += 1

    def record_execution(self) -> None:
        """Records a sandbox action execution and checks limit."""
        if self.usage.execution_count + 1 > self.budget.max_executions:
            raise MissionBudgetExceededError(
                f"Execution budget exceeded ({self.usage.execution_count + 1} > {self.budget.max_executions})."
            )
        self.usage.execution_count += 1

    def record_tokens(self, tokens: int) -> None:
        """Records token consumption and checks token budget limit."""
        if tokens < 0:
            raise ValueError("Token consumption cannot be negative.")
        if self.usage.tokens_consumed + tokens > self.budget.token_budget:
            raise MissionBudgetExceededError(
                f"Token budget exceeded ({self.usage.tokens_consumed + tokens} > {self.budget.token_budget})."
            )
        self.usage.tokens_consumed += tokens

    def record_asset_generation(self) -> None:
        """Records generated asset creation."""
        if self.usage.generated_assets + 1 > self.budget.max_generated_assets:
            raise MissionBudgetExceededError(
                f"Asset generation budget exceeded ({self.usage.generated_assets + 1} > {self.budget.max_generated_assets})."
            )
        self.usage.generated_assets += 1

    def record_external_request(self) -> None:
        """Records an external API request."""
        if self.usage.external_requests + 1 > self.budget.max_external_requests:
            raise MissionBudgetExceededError(
                f"External request budget exceeded ({self.usage.external_requests + 1} > {self.budget.max_external_requests})."
            )
        self.usage.external_requests += 1

    def update_runtime(self, elapsed_seconds: float) -> None:
        """Updates elapsed runtime and checks runtime budget."""
        self.usage.elapsed_seconds = elapsed_seconds
        if self.usage.elapsed_seconds > self.budget.max_runtime_seconds:
            raise MissionBudgetExceededError(
                f"Runtime limit exceeded ({self.usage.elapsed_seconds:.1f}s > {self.budget.max_runtime_seconds}s)."
            )
