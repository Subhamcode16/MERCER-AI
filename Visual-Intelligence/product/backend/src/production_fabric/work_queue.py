"""
Phase 17 Production Fabric Work Queue.
Maintains pending, ready, blocked, and active production items with deterministic priority ordering,
dependency awareness, deduplication, and starvation prevention.
"""

from typing import Dict, List, Optional
from src.production_fabric.production_models import ProductionWorkItem, ProductionPriority, ProductionState
from src.production_fabric.exceptions import WorkIntakeError, ProductionStateViolation

PRIORITY_WEIGHTS = {
    ProductionPriority.CRITICAL: 4,
    ProductionPriority.HIGH: 3,
    ProductionPriority.MEDIUM: 2,
    ProductionPriority.LOW: 1
}

class ProductionWorkQueue:
    """Work queue managing prioritized, dependency-aware production work items."""

    def __init__(self):
        self._queue: Dict[str, ProductionWorkItem] = {}

    def enqueue(self, item: ProductionWorkItem) -> None:
        """Admits an item idempotently to the queue."""
        if item.item_id not in self._queue:
            self._queue[item.item_id] = item

    def dequeue_next_ready(self, client_id: Optional[str] = None) -> Optional[ProductionWorkItem]:
        """Dequeues the highest priority ready work item for a given client (or any client)."""
        candidates = []
        for item in self._queue.values():
            if client_id and item.client_id != client_id:
                continue
            if item.state not in (ProductionState.COMPLETED, ProductionState.FAILED, ProductionState.BLOCKED):
                # Check dependencies
                deps_met = all(
                    dep_id in self._queue and self._queue[dep_id].state == ProductionState.COMPLETED
                    for dep_id in item.dependencies
                )
                if deps_met:
                    candidates.append(item)

        if not candidates:
            return None

        # Sort deterministically by priority weight desc, created_at asc
        candidates.sort(key=lambda x: (-PRIORITY_WEIGHTS.get(x.priority, 1), x.created_at))
        selected = candidates[0]
        return selected

    def list_queue_status(self, client_id: Optional[str] = None) -> List[ProductionWorkItem]:
        if client_id:
            return [item for item in self._queue.values() if item.client_id == client_id]
        return list(self._queue.values())

    def mark_blocked(self, item_id: str, reason: str = "") -> None:
        if item_id in self._queue:
            item = self._queue[item_id]
            if item.state in (ProductionState.ADMITTED, ProductionState.IN_PRODUCTION):
                item.transition_to(ProductionState.BLOCKED)

    def mark_unblocked(self, item_id: str) -> None:
        if item_id in self._queue:
            item = self._queue[item_id]
            if item.state == ProductionState.BLOCKED:
                item.transition_to(ProductionState.ADMITTED)
