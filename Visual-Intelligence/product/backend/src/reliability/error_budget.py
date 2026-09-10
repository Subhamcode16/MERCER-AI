"""
Phase 24 Error Budget and Burn Rate Calculator.
"""
import time
import logging
from typing import Dict, Any, List
from src.reliability.slo_models import ErrorBudgetStatus, BurnRateAlert, AlertSeverity

logger = logging.getLogger(__name__)

class ErrorBudgetEngine:
    """Manages error budget consumption, burn rate alerts, and automatic rollback triggers."""

    def __init__(self, target_availability: float = 0.999):
        # For 99.9% target, allowed failure rate is 0.1% (0.001)
        self.allowed_error_rate = 1.0 - target_availability
        self._total_requests = 0
        self._error_count = 0
        self._alerts: List[BurnRateAlert] = []

    def record_outcome(self, is_error: bool) -> None:
        self._total_requests += 1
        if is_error:
            self._error_count += 1

    def calculate_budget_status(self) -> ErrorBudgetStatus:
        if self._total_requests == 0:
            return ErrorBudgetStatus(
                total_budget=self.allowed_error_rate,
                consumed_budget=0.0,
                remaining_budget=self.allowed_error_rate,
                burn_rate_1h=0.0,
                burn_rate_24h=0.0,
                exhausted=False
            )

        actual_error_rate = self._error_count / self._total_requests
        consumed = min(self.allowed_error_rate, actual_error_rate)
        remaining = max(0.0, self.allowed_error_rate - actual_error_rate)
        exhausted = actual_error_rate > self.allowed_error_rate

        # Burn rate = actual_error_rate / allowed_error_rate (1.0 means consuming at exactly budget rate)
        burn_rate = actual_error_rate / self.allowed_error_rate if self.allowed_error_rate > 0 else 0.0

        if burn_rate > 5.0:
            self._alerts.append(BurnRateAlert(
                alert_id=f"alert-{len(self._alerts)+1:03d}",
                severity=AlertSeverity.ROLLBACK_TRIGGER,
                slo_name="AVAILABILITY_SLO",
                burn_rate=round(burn_rate, 2),
                message=f"Critical Error Budget Burn Rate: {burn_rate:.2f}x! Error budget rapidly exhausting.",
                recommended_action="TRIGGER_AUTOMATED_ROLLBACK"
            ))
        elif burn_rate > 2.0:
            self._alerts.append(BurnRateAlert(
                alert_id=f"alert-{len(self._alerts)+1:03d}",
                severity=AlertSeverity.WARNING,
                slo_name="AVAILABILITY_SLO",
                burn_rate=round(burn_rate, 2),
                message=f"Elevated Error Budget Burn Rate: {burn_rate:.2f}x",
                recommended_action="PAGE_ON_CALL"
            ))

        return ErrorBudgetStatus(
            total_budget=self.allowed_error_rate,
            consumed_budget=round(consumed, 6),
            remaining_budget=round(remaining, 6),
            burn_rate_1h=round(burn_rate, 2),
            burn_rate_24h=round(burn_rate, 2),
            exhausted=exhausted
        )

    def list_alerts(self) -> List[BurnRateAlert]:
        return list(self._alerts)
