"""
Phase 19 - Deterministic Strategy Retirement & Decay Manager.

Monitors active strategy degradation and triggers deterministic retirement
when performance drops below acceptable thresholds or reaches staleness limit.
"""

import time
from typing import Dict, Optional, Tuple, Any
from .knowledge_models import ValidatedStrategy
from .exceptions import StaleIntelligenceError


class StrategyRetirementManager:
    """Manages decay monitoring and deterministic retirement of strategies."""

    def __init__(
        self,
        max_age_seconds: float = 30 * 86400,  # 30-day default staleness limit
        accuracy_floor: float = 0.70,
        max_allowed_failure_rate: float = 0.10
    ):
        self.max_age_seconds = max_age_seconds
        self.accuracy_floor = accuracy_floor
        self.max_allowed_failure_rate = max_allowed_failure_rate

    def evaluate_strategy_health(
        self,
        strategy: ValidatedStrategy,
        current_telemetry: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[str]]:
        """Evaluate if active strategy remains healthy or must be retired."""
        if strategy.status in ["RETIRED", "ROLLED_BACK"]:
            return False, f"Strategy already in terminal state: {strategy.status}"

        # 1. Staleness check based on age
        age = time.time() - strategy.created_at
        if age > self.max_age_seconds:
            self.retire_strategy(strategy, reason=f"Staleness limit reached ({age/86400:.1f} days old)")
            return False, f"Stale intelligence: strategy exceeds max age"

        # 2. Performance degradation check if telemetry available
        if current_telemetry:
            acc = current_telemetry.get("accuracy", strategy.accuracy_score)
            fail_rate = current_telemetry.get("failure_rate", strategy.failure_rate)

            if acc < self.accuracy_floor:
                self.retire_strategy(strategy, reason=f"Accuracy decayed to {acc:.2f} below floor {self.accuracy_floor}")
                return False, f"Performance decay: accuracy below floor"

            if fail_rate > self.max_allowed_failure_rate:
                self.retire_strategy(strategy, reason=f"Failure rate spiked to {fail_rate:.3f}")
                return False, f"Reliability failure: high error rate"

        return True, None

    def retire_strategy(self, strategy: ValidatedStrategy, reason: str) -> None:
        """Mark strategy as RETIRED with timestamp and reason."""
        strategy.status = "RETIRED"
        strategy.retired_at = time.time()
        strategy.retirement_reason = reason
