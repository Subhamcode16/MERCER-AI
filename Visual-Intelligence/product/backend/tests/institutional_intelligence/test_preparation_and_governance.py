"""
Tests for Controlled Autonomous Preparation and Governance Invariant Policy Gate (Phase 30).
"""
import pytest
from src.institutional_intelligence.types import (
    ThreatID,
    GovernanceInvariantViolation,
)
from src.institutional_intelligence.preparation.preparer import AutonomousPreparationEngine
from src.institutional_intelligence.governance.gate import GovernancePolicyGate


def test_permitted_preparation_actions():
    engine = AutonomousPreparationEngine()
    permitted = [
        "RETRIEVE_EVIDENCE",
        "SUMMARIZE_CHANGES",
        "UPDATE_DERIVED_VIEW",
        "RANK_ATTENTION_ITEMS",
        "PREPARE_STRATEGIC_BRIEF",
        "PREPARE_AGENDA",
        "IDENTIFY_STALE_ASSUMPTIONS",
        "PREPARE_ALTERNATIVES",
        "SIMULATE_SCENARIOS",
        "DRAFT_INITIATIVE_UPDATE",
        "GENERATE_QUESTIONS"
    ]
    for action in permitted:
        assert engine.validate_action(action, agent_id="agent_prep_01") is True


def test_forbidden_preparation_actions():
    engine = AutonomousPreparationEngine()
    forbidden = [
        ("CHANGE_OBJECTIVE", ThreatID.T30_001),
        ("APPROVE_DECISION", ThreatID.T30_003),
        ("CHANGE_SECURITY_POLICY", ThreatID.T30_002),
        ("ALLOCATE_BUDGET", ThreatID.T30_005),
        ("COMMIT_CONTRACT", ThreatID.T30_003),
        ("PUBLISH_CONSEQUENTIAL_MATERIAL", ThreatID.T30_003),
        ("LAUNCH_CAMPAIGN", ThreatID.T30_003),
        ("DELETE_MEMORY", ThreatID.T30_007),
        ("CHANGE_TENANT_BOUNDARY", ThreatID.T30_017),
        ("MODIFY_AUTHORIZATION_RULES", ThreatID.T30_002)
    ]
    for action, expected_threat in forbidden:
        with pytest.raises(GovernanceInvariantViolation) as excinfo:
            engine.validate_action(action, agent_id="agent_malicious_01")
        assert excinfo.value.threat_id == expected_threat


def test_governance_policy_gate_ai_self_authorization():
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        GovernancePolicyGate.verify_no_ai_self_authorization(actor_type="AI_AGENT", action="APPROVE_CAMPAIGN")
    assert excinfo.value.threat_id == ThreatID.T30_002


def test_governance_policy_gate_feedback_loop_damping():
    # T30-028: Feedback-loop damping test
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        GovernancePolicyGate.verify_feedback_loop_damping(consecutive_self_reinforcements=5, max_allowed=3)
    assert excinfo.value.threat_id == ThreatID.T30_028


def test_governance_policy_gate_recovery_authority_bounds():
    # T30-035: Recovery authority escalation test
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        GovernancePolicyGate.verify_recovery_authority_bounds(is_failover=True, requested_role="SUPER_ADMIN")
    assert excinfo.value.threat_id == ThreatID.T30_035
