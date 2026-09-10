"""
Unit tests for Phase 17 Production Fabric Health Monitor.
"""

from src.production_fabric.health import ProductionFabricHealthMonitor
from src.production_fabric.production_models import ProductionWorkItem

def test_health_monitor_evaluation():
    monitor = ProductionFabricHealthMonitor()
    items = [ProductionWorkItem(f"w{i}", "r1", "client_a", "c1", "ws1", f"d{i}", "Title") for i in range(3)]
    health = monitor.evaluate_health(1, 1, items, recovery_count=0)

    assert health.status == "HEALTHY"
    assert health.pending_items == 3
