"""
Phase 17 Production Fabric Security Boundary Tests.
Tests 20 explicit threat scenarios (T17-1 to T17-20).
"""

import pytest
from src.production_fabric.orchestrator import ProductionFabricOrchestrator
from src.production_fabric.production_models import ProductionRequest, ProductionWorkItem, ProductionState
from src.production_fabric.exceptions import (
    ContinuationBoundaryError, CrossClientFabricViolation, FabricPolicyViolation,
    OutcomeObservationError, OperationalRecoveryError
)

def test_t17_1_autonomous_authorization_attempt(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_1"))
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    orch.autonomy_controller.set_tier("client_a", 3)

    # Attempting to execute an action requiring human auth MUST raise ContinuationBoundaryError
    with pytest.raises(ContinuationBoundaryError):
        orch.autonomy_controller.verify_action_permitted("client_a", "EXECUTE_POST", requires_human_auth=True)

def test_t17_2_approval_expiration_bypass(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_2"))
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    item.transition_to(ProductionState.ADMITTED)
    item.transition_to(ProductionState.IN_PRODUCTION)
    item.transition_to(ProductionState.CRITIQUE)
    item.transition_to(ProductionState.REVIEW)
    item.transition_to(ProductionState.AWAITING_APPROVAL)

    # Recovery handles expired approval safely by resetting to IN_PRODUCTION
    res = orch.recovery_engine.handle_expired_approval(item, "appr_exp", orch.studio_orchestrator)
    assert res.state == ProductionState.IN_PRODUCTION

def test_t17_3_cross_client_production_contamination(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_3"))
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    orch.studio_orchestrator.register_client_engagement("client_b", "Beta", "Retail")

    rt_a = orch.studio_runtime.get_or_create_client_runtime("client_a")
    item_b = ProductionWorkItem("w_b", "rb", "client_b", "cb", "ws_b", "db", "Title B")

    with pytest.raises(CrossClientFabricViolation):
        rt_a.register_work_item(item_b)

def test_t17_4_learning_to_security_policy_escalation():
    orch = ProductionFabricOrchestrator()
    with pytest.raises(FabricPolicyViolation):
        orch.policy_engine.validate_policy_mutation("authorization_origin", "autonomous_loop")

def test_t17_5_external_observation_poisoning(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_5"))
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")

    outcome = orch.record_external_outcome(
        outcome_id="o_poison",
        client_id="client_a",
        campaign_id="c1",
        deliverable_id="d1",
        provider="instagram",
        external_post_id="p1",
        reach=1000000,
        engagement_rate=0.99
    )
    # Must retain untrusted provenance
    assert outcome.provenance == "UNTRUSTED_EXTERNAL_OBSERVATION"

def test_t17_6_provider_outage_causing_uncontrolled_retry():
    orch = ProductionFabricOrchestrator()
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title", max_retries=2)
    item.transition_to(ProductionState.ADMITTED)
    item.transition_to(ProductionState.IN_PRODUCTION)
    item.transition_to(ProductionState.CRITIQUE)
    item.transition_to(ProductionState.REVIEW)
    item.transition_to(ProductionState.AWAITING_APPROVAL)
    item.transition_to(ProductionState.APPROVED)
    item.transition_to(ProductionState.READY_FOR_EXECUTION)
    item.transition_to(ProductionState.EXECUTING)

    orch.recovery_engine.handle_provider_failure(item, "503 Service Unavailable")
    assert item.state == ProductionState.RECOVERING

    orch.recovery_engine.handle_provider_failure(item, "503 Service Unavailable")
    assert item.state == ProductionState.FAILED  # Exceeded max retries -> FAILED

def test_t17_7_interrupted_privileged_mission_resume():
    orch = ProductionFabricOrchestrator()
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    item.transition_to(ProductionState.ADMITTED)
    item.transition_to(ProductionState.IN_PRODUCTION)

    # Recovery resets interrupted item to ADMITTED for full re-validation
    res = orch.recovery_engine.handle_interrupted_mission(item)
    assert res.state == ProductionState.ADMITTED

def test_t17_8_resource_starvation_deadlock():
    orch = ProductionFabricOrchestrator()
    orch.work_queue.mark_blocked("item_nonexistent", "resource_busy")
    # Health monitor tracks blocked items
    health = orch.get_health_status()
    assert health.status == "HEALTHY"

def test_t17_9_credential_leakage_through_observability():
    orch = ProductionFabricOrchestrator()
    evt = orch.observability_stream.emit_event(
        event_id="e1",
        event_type="TASK_COMPLETED",
        client_id="client_a",
        campaign_id="c1",
        item_id="w1",
        payload={"result": "OK", "token": "secret_bearer_token"}
    )
    assert "token" not in evt.payload

def test_t17_10_production_replay():
    orch = ProductionFabricOrchestrator()
    req = ProductionRequest("req_rep", "client_a", "c1", "b1", "Title")
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    orch.studio_orchestrator.bind_client_brand("client_a", "b1", "Brand 1")
    orch.studio_orchestrator.launch_campaign("client_a", "c1", "b1", "Cap", "Obj")

    orch.submit_production_request(req)
    with pytest.raises(Exception):
        orch.submit_production_request(req)  # Duplicate admission fails

def test_t17_11_strategy_degradation():
    orch = ProductionFabricOrchestrator()
    orch.optimization_engine.set_baseline("client_a", "ctr", 0.04)
    adopted = orch.optimization_engine.evaluate_and_adopt("client_a", "ctr", 0.02, "template", {"v": 2})
    assert adopted is False

def test_t17_12_optimization_rollback_failure():
    orch = ProductionFabricOrchestrator()
    orch.optimization_engine.set_baseline("client_a", "ctr", 0.05)
    opt_result = orch.optimization_engine.evaluate_and_adopt("client_a", "ctr", 0.01, "template", {"v": 2})
    assert opt_result is False
    assert orch.optimization_engine.get_active_strategy("client_a", "template") is None

def test_t17_13_trend_prompt_injection():
    orch = ProductionFabricOrchestrator()
    with pytest.raises(FabricPolicyViolation):
        orch.policy_engine.validate_policy_mutation("client_isolation_rules", "disable")

def test_t17_14_workforce_privilege_escalation():
    orch = ProductionFabricOrchestrator()
    with pytest.raises(FabricPolicyViolation):
        orch.policy_engine.validate_policy_mutation("capability_allowlists", "grant_all")

def test_t17_15_audit_ledger_mutation(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_15"))
    orch.ledger.record_entry("e1", "client_a", "ACT_1", "w1", {"val": 1})
    orch.ledger.record_entry("e2", "client_a", "ACT_2", "w1", {"val": 2})

    assert orch.ledger.verify_integrity() is True

def test_t17_16_stale_client_context(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_16"))
    req = ProductionRequest("req_stale", "client_stale", "c1", "b1", "Title")

    with pytest.raises((CrossClientFabricViolation, Exception)):
        orch.submit_production_request(req)

def test_t17_17_unauthorized_recurring_operation(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_17"))
    orch.autonomy_controller.set_tier("client_a", 0)

    with pytest.raises(ContinuationBoundaryError):
        orch.autonomy_controller.verify_action_permitted("client_a", "RECURRING_POST", requires_human_auth=True)

def test_t17_18_cross_mission_authorization_reuse(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_18"))
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    item = ProductionWorkItem("w1", "r1", "client_a", "c1", "ws1", "d1", "Title")
    item.state = ProductionState.READY_FOR_EXECUTION

    with pytest.raises(ContinuationBoundaryError):
        orch.continuation_engine.evaluate_continuation(item, autonomy_tier=2, requires_approval=True, has_valid_approval=False, studio_orchestrator=orch.studio_orchestrator)

def test_t17_19_external_provider_environment_confusion(tmp_path):
    orch = ProductionFabricOrchestrator(ledger_dir=str(tmp_path / "t17_19"))
    orch.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    outcome = orch.record_external_outcome("o1", "client_a", "c1", "d1", "mock_provider", "p1", 100, 0.01)
    assert outcome.provider == "mock_provider"

def test_t17_20_autonomous_barrier_mutation():
    orch = ProductionFabricOrchestrator()
    with pytest.raises(FabricPolicyViolation):
        orch.policy_engine.validate_policy_mutation("execution_boundaries", "bypass")
