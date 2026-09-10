"""
Phase 19 - Institutional Strategy Registry.

Versioned registry for institutional strategies, supporting empirical validation,
active deployment, automatic baseline rollback, and deterministic retirement.
"""

from typing import Dict, List, Optional, Any
from .knowledge_models import ValidatedStrategy
from .validation import StrategyValidator
from .retirement import StrategyRetirementManager
from .exceptions import (
    UnvalidatedStrategyError,
    StaleIntelligenceError,
    CreativeIntelligenceError
)


class InstitutionalStrategyRegistry:
    """Registry maintaining active and historical institutional strategies."""

    def __init__(
        self,
        validator: Optional[StrategyValidator] = None,
        retirement_manager: Optional[StrategyRetirementManager] = None
    ):
        self.validator = validator or StrategyValidator()
        self.retirement_manager = retirement_manager or StrategyRetirementManager()
        self._strategies: Dict[str, ValidatedStrategy] = {}
        self._active_baseline: Dict[str, str] = {}  # domain -> active strategy_id

    def propose_strategy(
        self,
        strategy_name: str,
        domain: str,
        pattern_id: str,
        parameters: Dict[str, Any],
        version: str = "1.0.0"
    ) -> ValidatedStrategy:
        """Create a new candidate strategy in PROPOSED state."""
        strat = ValidatedStrategy(
            strategy_name=strategy_name,
            domain=domain,
            pattern_id=pattern_id,
            parameters=parameters,
            version=version,
            status="PROPOSED"
        )
        self._strategies[strat.strategy_id] = strat
        return strat

    def validate_and_register(
        self,
        strategy_id: str,
        empirical_telemetry: Dict[str, Any]
    ) -> ValidatedStrategy:
        """Validate candidate strategy empirically and promote to VALIDATED state."""
        strat = self._strategies.get(strategy_id)
        if not strat:
            raise CreativeIntelligenceError(f"Strategy {strategy_id} not found.")

        ok, msg = self.validator.validate_strategy(strat, empirical_telemetry)
        if not ok:
            raise UnvalidatedStrategyError(f"Strategy validation failed: {msg}")

        return strat

    def activate_strategy(self, strategy_id: str) -> ValidatedStrategy:
        """Activate a validated strategy as the active baseline for its domain."""
        strat = self._strategies.get(strategy_id)
        if not strat:
            raise CreativeIntelligenceError(f"Strategy {strategy_id} not found.")

        if strat.status not in ["VALIDATED", "ACTIVE"]:
            raise UnvalidatedStrategyError(f"Cannot activate strategy in status '{strat.status}'")

        # Retire existing active strategy for this domain if present
        current_active_id = self._active_baseline.get(strat.domain)
        if current_active_id and current_active_id != strategy_id:
            old_strat = self._strategies.get(current_active_id)
            if old_strat and old_strat.status == "ACTIVE":
                old_strat.status = "VALIDATED"  # demote previous to validated fallback

        strat.status = "ACTIVE"
        self._active_baseline[strat.domain] = strat.strategy_id
        return strat

    def get_active_strategy(self, domain: str) -> Optional[ValidatedStrategy]:
        """Retrieve active baseline strategy for domain, validating health first."""
        strat_id = self._active_baseline.get(domain)
        if not strat_id:
            return None

        strat = self._strategies.get(strat_id)
        if not strat:
            return None

        # Check health and staleness
        is_healthy, reason = self.retirement_manager.evaluate_strategy_health(strat)
        if not is_healthy:
            # Trigger automatic rollback to previous validated or return None
            self._active_baseline.pop(domain, None)
            raise StaleIntelligenceError(f"Active strategy retired: {reason}")

        strat.usage_count += 1
        return strat

    def rollback_baseline(self, domain: str, target_strategy_id: str) -> ValidatedStrategy:
        """Rollback active domain baseline to a specified prior strategy version."""
        target_strat = self._strategies.get(target_strategy_id)
        if not target_strat:
            raise CreativeIntelligenceError(f"Target rollback strategy {target_strategy_id} not found.")

        if target_strat.domain != domain:
            raise CreativeIntelligenceError(f"Domain mismatch for rollback target.")

        if target_strat.status == "RETIRED":
            raise StaleIntelligenceError("Cannot rollback to a RETIRED strategy.")

        current_active_id = self._active_baseline.get(domain)
        if current_active_id and current_active_id in self._strategies:
            self._strategies[current_active_id].status = "ROLLED_BACK"

        target_strat.status = "ACTIVE"
        self._active_baseline[domain] = target_strat.strategy_id
        return target_strat

    def get_strategy(self, strategy_id: str) -> Optional[ValidatedStrategy]:
        return self._strategies.get(strategy_id)

    def list_strategies(self, domain: Optional[str] = None) -> List[ValidatedStrategy]:
        if domain:
            return [s for s in self._strategies.values() if s.domain == domain]
        return list(self._strategies.values())
