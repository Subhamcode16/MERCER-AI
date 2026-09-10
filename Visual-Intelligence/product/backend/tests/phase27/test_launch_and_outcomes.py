"""
Tests for Phase 27 Launch Manager and Outcomes Analytics.
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.campaign_studio.launch import LaunchManager, LaunchState
from src.campaign_studio.outcomes import OutcomesManager


def test_staging_and_authorized_launch():
    mgr = LaunchManager()
    campaign_id = "camp_launch_01"

    manifest = mgr.stage_launch(
        campaign_id=campaign_id,
        channel_allocations={"E-commerce Hero": ["ast_01"], "Instagram": ["ast_02", "ast_03"]},
        verified_assets=["ast_01", "ast_02", "ast_03"],
    )
    assert manifest.state == LaunchState.STAGED
    assert manifest.pre_launch_checks_passed is True

    # Unauthorized operator fails to execute launch
    unauth_op = OperatorContext(operator_id="op_intern_01", role=OperatorRole.STAFF_OPERATOR, department="Ops")
    with pytest.raises(PermissionError):
        mgr.execute_launch(campaign_id, unauth_op)

    # Authorized operator succeeds
    auth_op = OperatorContext(operator_id="op_exec_01", role=OperatorRole.BRAND_EXECUTIVE, department="Executive")
    launched = mgr.execute_launch(campaign_id, auth_op)
    assert launched.state == LaunchState.LAUNCHED
    assert launched.launched_by == "op_exec_01"


def test_outcomes_and_postmortem_insights():
    outcomes = OutcomesManager()
    campaign_id = "camp_outcomes_01"

    metrics = outcomes.record_outcomes(
        campaign_id=campaign_id,
        impressions=250000,
        click_through_rate=0.051,
        conversion_lift_percent=22.4,
    )
    assert metrics.impressions == 250000
    assert "Correlational - Not Causal Proof" in metrics.attribution_model

    postmortems = outcomes.generate_postmortem(campaign_id)
    assert len(postmortems) == 1
    assert "raking_monolithic_late_sun" in postmortems[0].advisory_recommendation
