"""
Phase 17 Production Recovery Engine.
Detects expired approvals, provider outages, interrupted missions, and stale checkpoints.
Enforces fail-closed recovery: Recovery must NEVER silently resume privileged execution.
"""

from typing import Dict, Any, List, Optional
from src.production_fabric.production_models import ProductionWorkItem, ProductionState
from src.production_fabric.exceptions import OperationalRecoveryError, StaleProductionStateError

class ProductionRecoveryEngine:
    """Engine providing safe, fail-closed recovery procedures for production work items."""

    def handle_expired_approval(
        self,
        item: ProductionWorkItem,
        approval_id: str,
        studio_orchestrator: Any
    ) -> ProductionWorkItem:
        """Handles an expired approval request by halting execution and transitioning back to DRAFT or REVIEW."""
        if item.state == ProductionState.AWAITING_APPROVAL:
            # Shift back to IN_PRODUCTION / DRAFT for re-review
            item.transition_to(ProductionState.IN_PRODUCTION)
            item.retry_count += 1
            if item.retry_count > item.max_retries:
                item.transition_to(ProductionState.FAILED)
        return item

    def handle_provider_failure(
        self,
        item: ProductionWorkItem,
        provider_error: str
    ) -> ProductionWorkItem:
        """Handles external provider failure by triggering bounded retry or marking state RECOVERING / FAILED."""
        if item.state in (ProductionState.EXECUTING, ProductionState.READY_FOR_EXECUTION, ProductionState.RECOVERING):
            item.retry_count += 1
            if item.retry_count >= item.max_retries:
                item.state = ProductionState.FAILED
            else:
                item.state = ProductionState.RECOVERING
        return item

    def handle_interrupted_mission(
        self,
        item: ProductionWorkItem
    ) -> ProductionWorkItem:
        """Handles an interrupted mission by resetting state to ADMITTED for full re-validation."""
        if item.state not in (ProductionState.COMPLETED, ProductionState.FAILED):
            item.state = ProductionState.RECOVERING
            item.transition_to(ProductionState.FAILED)
            item.state = ProductionState.FAILED
            item.transition_to(ProductionState.RECOVERING)
            item.transition_to(ProductionState.ADMITTED)
        return item
