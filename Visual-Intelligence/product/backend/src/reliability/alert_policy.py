"""
Phase 24 Multi-Tier Alert Dispatcher and Policy Engine.
"""
import logging
from typing import List, Dict, Any, Callable
from src.reliability.slo_models import BurnRateAlert, AlertSeverity

logger = logging.getLogger(__name__)

class AlertPolicyEngine:
    """Evaluates metrics and dispatches alerts according to configured severity policies."""

    def __init__(self):
        self._handlers: Dict[AlertSeverity, List[Callable[[BurnRateAlert], None]]] = {
            s: [] for s in AlertSeverity
        }
        self._dispatched_alerts: List[BurnRateAlert] = []

    def register_handler(self, severity: AlertSeverity, handler: Callable[[BurnRateAlert], None]) -> None:
        self._handlers[severity].append(handler)

    def dispatch_alert(self, alert: BurnRateAlert) -> None:
        self._dispatched_alerts.append(alert)
        logger.warning(f"ALERT [{alert.severity.value}]: {alert.message} (Action: {alert.recommended_action})")

        for handler in self._handlers.get(alert.severity, []):
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler for {alert.severity.value}: {e}")

    def list_dispatched(self) -> List[BurnRateAlert]:
        return list(self._dispatched_alerts)
