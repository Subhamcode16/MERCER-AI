"""
Unit tests for Phase 15 Studio Performance Engine.
"""

import pytest
from src.studio_operations.performance import StudioPerformanceEngine
from src.studio_operations.studio_models import Deliverable, DeliverableStatus

def test_performance_calculation():
    engine = StudioPerformanceEngine()
    d1 = Deliverable("del_001", "ws_001", "camp_001", "client_nocap", "Post 1", status=DeliverableStatus.EXECUTED, revision_count=1)
    d2 = Deliverable("del_002", "ws_001", "camp_001", "client_nocap", "Post 2", status=DeliverableStatus.OBSERVED, revision_count=0)

    metrics = engine.calculate_metrics(
        requesting_client_id="client_nocap",
        target_client_id="client_nocap",
        deliverables=[d1, d2],
        approvals=[]
    )

    assert metrics.total_deliverables == 2
    assert metrics.completed_deliverables == 2
    assert metrics.average_revision_count == 0.5
    assert metrics.workflow_efficiency_score > 0.0
