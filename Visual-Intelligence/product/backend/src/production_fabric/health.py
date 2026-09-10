"""
Phase 17 Production Fabric Health Monitor.
Tracks operational health indicators, queue depth, recovery events, approval latency, and provider metrics.
"""

from typing import Dict, Any, List
from src.production_fabric.production_models import ProductionHealth, ProductionWorkItem, ProductionState

class ProductionFabricHealthMonitor:
    """Health monitor evaluating operational fabric health indicators."""

    def evaluate_health(
        self,
        active_clients_count: int,
        active_campaigns_count: int,
        work_items: List[ProductionWorkItem],
        recovery_count: int
    ) -> ProductionHealth:
        """Evaluates health summary across active work items and recovery events."""
        pending = sum(1 for i in work_items if i.state in (ProductionState.PENDING, ProductionState.ADMITTED))
        blocked = sum(1 for i in work_items if i.state in (ProductionState.BLOCKED, ProductionState.FAILED))
        executing = sum(1 for i in work_items if i.state in (ProductionState.EXECUTING, ProductionState.READY_FOR_EXECUTION))

        status = "HEALTHY"
        if blocked > 5 or recovery_count > 10:
            status = "DEGRADED"

        return ProductionHealth(
            active_clients=active_clients_count,
            active_campaigns=active_campaigns_count,
            pending_items=pending,
            blocked_items=blocked,
            executing_items=executing,
            recovery_count=recovery_count,
            status=status
        )
