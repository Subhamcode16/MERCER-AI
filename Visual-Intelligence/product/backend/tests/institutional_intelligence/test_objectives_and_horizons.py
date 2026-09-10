"""
Tests for Strategic Objectives and Horizons (Phase 30).
"""
import pytest
from src.institutional_intelligence.types import (
    StrategicHorizon,
    ThreatID,
    GovernanceInvariantViolation,
)
from src.institutional_intelligence.objectives.models import StrategicObjective
from src.institutional_intelligence.horizons.models import StrategicHorizonMapping, HorizonPortfolioView


def test_strategic_objective_creation_valid():
    obj = StrategicObjective(
        tenant_id="tenant_01",
        owner="human_director_42",
        creation_authority="AUTH_TOKEN_CORP_2026",
        title="Establish Global Haute Couture Footprint",
        description="Expand reach into European luxury hubs.",
        scope="GLOBAL_HAUTE_COUTURE",
        time_horizon=StrategicHorizon.NOW,
        priority=9
    )
    obj.validate_human_authority(obj.owner, is_automated_agent=False)
    assert obj.is_human_authorized is True
    assert obj.status == "ACTIVE"
    assert obj.time_horizon == StrategicHorizon.NOW


def test_t30_001_automated_agent_cannot_create_objective():
    obj = StrategicObjective(
        tenant_id="tenant_01",
        owner="ai_bot_007",
        creation_authority="AUTOMATED_GENAI_OUTPUT",
        title="AI Generated Direction",
        description="Autonomous objective without human authority.",
        scope="GLOBAL"
    )
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        obj.validate_human_authority(obj.owner, is_automated_agent=True)
    assert excinfo.value.threat_id == ThreatID.T30_001


def test_t30_001_automated_agent_cannot_mutate_objective_scope():
    obj = StrategicObjective(
        tenant_id="tenant_01",
        owner="human_director_42",
        creation_authority="AUTH_TOKEN_CORP_2026",
        title="Valid Objective",
        description="Valid description",
        scope="REGIONAL_PARIS"
    )
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        obj.mutate_scope("UNAUTHORIZED_GLOBAL_EXPANSION", modifier_actor="ai_strategy_worker", is_automated_agent=True)
    assert excinfo.value.threat_id == ThreatID.T30_001


def test_human_can_mutate_objective_scope():
    obj = StrategicObjective(
        tenant_id="tenant_01",
        owner="human_director_42",
        creation_authority="AUTH_TOKEN_CORP_2026",
        title="Valid Objective",
        description="Valid description",
        scope="REGIONAL_PARIS"
    )
    obj.mutate_scope("REGIONAL_EUROPE", modifier_actor="human_director_42", is_automated_agent=False, rationale="Board approval")
    assert obj.scope == "REGIONAL_EUROPE"
    assert len(obj.revision_history) == 1
    assert obj.revision_history[0]["previous_scope"] == "REGIONAL_PARIS"


def test_horizon_mapping_transitions():
    mapping = StrategicHorizonMapping(
        tenant_id="tenant_01",
        target_id="obj_123",
        target_type="OBJECTIVE",
        horizon=StrategicHorizon.LATER,
        assigned_by="human_director_42"
    )
    assert mapping.horizon == StrategicHorizon.LATER

    mapping.transition_horizon(StrategicHorizon.NOW, actor="human_director_42", is_automated=False, rationale="Prioritized")
    assert mapping.horizon == StrategicHorizon.NOW
    assert len(mapping.transition_history) == 1


def test_t30_012_unknown_horizon_collapse_blocked_for_automated():
    mapping = StrategicHorizonMapping(
        tenant_id="tenant_01",
        target_id="obj_unknown",
        target_type="OBJECTIVE",
        horizon=StrategicHorizon.UNKNOWN,
        assigned_by="human_director_42"
    )
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        mapping.transition_horizon(StrategicHorizon.NOW, actor="ai_auto_scheduler", is_automated=True)
    assert excinfo.value.threat_id == ThreatID.T30_012


def test_horizon_portfolio_view_aggregation():
    view = HorizonPortfolioView(tenant_id="tenant_01")
    view.add_item("obj_1", StrategicHorizon.NOW)
    view.add_item("obj_2", StrategicHorizon.NEXT)
    view.add_item("obj_3", StrategicHorizon.LATER)
    view.add_item("obj_4", StrategicHorizon.FUTURE)
    view.add_item("obj_5", StrategicHorizon.UNKNOWN)

    assert "obj_1" in view.now
    assert "obj_2" in view.next
    assert "obj_3" in view.later
    assert "obj_4" in view.future
    assert "obj_5" in view.unknown


def test_objective_priority_bounds():
    obj = StrategicObjective(
        tenant_id="tenant_01",
        owner="human_director_42",
        creation_authority="AUTH_TOKEN_CORP_2026",
        title="High Priority Objective",
        description="Desc",
        scope="GLOBAL",
        priority=10
    )
    assert obj.priority == 10
    with pytest.raises(Exception):
        StrategicObjective(
            tenant_id="tenant_01",
            owner="human_director_42",
            creation_authority="AUTH_TOKEN_CORP_2026",
            title="Invalid Priority Objective",
            description="Desc",
            scope="GLOBAL",
            priority=15  # Out of range 1-10
        )


def test_horizon_unknown_first_class_status():
    mapping = StrategicHorizonMapping(
        tenant_id="tenant_01",
        target_id="obj_unknown_status",
        target_type="OBJECTIVE",
        horizon=StrategicHorizon.UNKNOWN,
        assigned_by="human_director_42"
    )
    assert mapping.horizon.value == "UNKNOWN"

