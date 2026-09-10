"""
Unit tests for Phase 15 Operational Continuity Engine.
"""

import pytest
from src.studio_operations.continuity_engine import OperationalContinuityEngine
from src.studio_operations.studio_models import Deliverable, DeliverableStatus, CampaignStatus

def test_continuity_engine_evaluation():
    engine = OperationalContinuityEngine()
    d1 = Deliverable("del_001", "ws_001", "camp_001", "client_nocap", "Hero Post", status=DeliverableStatus.PLANNED)
    d2 = Deliverable("del_002", "ws_001", "camp_001", "client_nocap", "Secondary Post", status=DeliverableStatus.DRAFT)

    plan = engine.determine_next_steps(
        requesting_client_id="client_nocap",
        client_id="client_nocap",
        campaign_id="camp_001",
        campaign_status=CampaignStatus.ACTIVE,
        deliverables=[d1, d2],
        pending_approvals=[]
    )

    assert plan.status == "VALID"
    assert len(plan.recommended_steps) == 2
    assert plan.recommended_steps[0].action_type == "DRAFT_CONTENT"
    assert plan.recommended_steps[1].action_type == "SELF_CRITIQUE"
