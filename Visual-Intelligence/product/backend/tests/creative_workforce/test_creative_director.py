"""
Phase 14 Test Creative Workforce Director
------------------------------------------
Tests CreativeWorkforceDirector plan formulation and campaign management.
"""

import pytest
from src.creative_workforce import CreativeWorkforceDirector, InvalidWorkforceRequestError

def test_formulate_workforce_plan():
    director = CreativeWorkforceDirector()
    plan = director.formulate_workforce_plan(
        client_id="nocap",
        brand_id="nocap-apparel",
        campaign_title="September Lookbook Campaign",
        objective="Launch autumn collection",
    )
    assert plan.plan_id.startswith("plan-")
    assert plan.client_id == "nocap"
    assert len(plan.assignments) == 7

def test_missing_client_fields_rejection():
    director = CreativeWorkforceDirector()
    with pytest.raises(InvalidWorkforceRequestError):
        director.formulate_workforce_plan("", "brand", "title", "obj")
