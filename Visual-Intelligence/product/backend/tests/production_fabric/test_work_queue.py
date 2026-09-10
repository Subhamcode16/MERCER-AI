"""
Unit tests for Phase 17 Production Work Queue.
"""

from src.production_fabric.work_queue import ProductionWorkQueue
from src.production_fabric.production_models import ProductionWorkItem, ProductionPriority, ProductionState

def test_queue_priority_ordering():
    queue = ProductionWorkQueue()
    item_low = ProductionWorkItem("w_low", "r1", "client_a", "c1", "ws1", "d1", "Low Priority", priority=ProductionPriority.LOW)
    item_crit = ProductionWorkItem("w_crit", "r2", "client_a", "c1", "ws1", "d2", "Critical Priority", priority=ProductionPriority.CRITICAL)

    item_low.transition_to(ProductionState.ADMITTED)
    item_crit.transition_to(ProductionState.ADMITTED)

    queue.enqueue(item_low)
    queue.enqueue(item_crit)

    next_item = queue.dequeue_next_ready("client_a")
    assert next_item is not None
    assert next_item.item_id == "w_crit"
