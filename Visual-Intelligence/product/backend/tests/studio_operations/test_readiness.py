"""
Unit tests for Phase 15 Production Readiness Engine.
"""

import pytest
from src.studio_operations.readiness import ProductionReadinessEngine
from src.studio_operations.studio_models import Deliverable, DeliverableStatus, ClientOperatingPolicy

def test_production_readiness_checklist():
    engine = ProductionReadinessEngine()
    d = Deliverable("del_001", "ws_001", "camp_001", "client_nocap", "Hero Post", status=DeliverableStatus.APPROVED)
    pol = ClientOperatingPolicy("pol_001", "client_nocap", require_human_approval=True)

    report = engine.evaluate_readiness("client_nocap", "client_nocap", "camp_001", d, pol, has_approval=True)
    assert report.is_ready is True
    assert report.readiness_score == 1.0

    # Missing approval
    report_unapproved = engine.evaluate_readiness("client_nocap", "client_nocap", "camp_001", d, pol, has_approval=False)
    assert report_unapproved.is_ready is False
    assert "APPROVAL_REQUIREMENTS_MISSING" in report_unapproved.checks_failed
