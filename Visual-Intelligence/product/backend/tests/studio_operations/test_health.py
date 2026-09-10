"""
Unit tests for Phase 15 Studio Health Monitor.
"""

import pytest
from src.studio_operations.health import StudioHealthMonitor
from src.studio_operations.studio_models import Campaign, Deliverable, DeliverableStatus

def test_health_monitor_evaluation():
    monitor = StudioHealthMonitor()
    c1 = Campaign("camp_001", "client_nocap", "brand_nocap", "Fall Drop", "Objective")
    d1 = Deliverable("del_001", "ws_001", "camp_001", "client_nocap", "Hero Post", status=DeliverableStatus.DRAFT, revision_count=1)

    report = monitor.evaluate_health(
        requesting_client_id="client_nocap",
        target_client_id="client_nocap",
        campaigns=[c1],
        deliverables=[d1],
        approvals=[],
        handoffs=[]
    )

    assert report.overall_health == "HEALTHY"
    assert len(report.stalled_campaigns) == 0
