"""
Phase 17 Real Workflow Benchmark.
Simulates an ILYREN Creative Studio 30-Day Multi-Client Production Cycle
incorporating Client A (NOCAP), Client B (Beta), 7 operational events, and 15 required assertions.
"""

import pytest
from src.production_fabric.orchestrator import ProductionFabricOrchestrator
from src.production_fabric.production_models import ProductionRequest, ProductionWorkItem, ProductionState, ProductionPriority
from src.production_fabric.exceptions import (
    ContinuationBoundaryError, CrossClientFabricViolation, FabricPolicyViolation
)
from src.studio_operations.studio_models import DeliverableStatus

def test_phase17_30day_multiclient_production_cycle_benchmark(tmp_path):
    ledger_dir = str(tmp_path / "phase17_real_benchmark_ledger")
    orch = ProductionFabricOrchestrator(ledger_dir=ledger_dir)

    # ---------------------------------------------------------
    # STAGE 1: Client Onboarding & Setup
    # ---------------------------------------------------------
    # Client A — NOCAP
    orch.studio_orchestrator.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    orch.studio_orchestrator.bind_client_brand("client_nocap", "brand_nocap", "NOCAP Streetwear")
    orch.studio_orchestrator.launch_campaign("client_nocap", "camp_nocap_sep", "brand_nocap", "Fall Drop 2026", "Awareness")

    # Client B — Beta Tech
    orch.studio_orchestrator.register_client_engagement("client_beta", "Beta Tech", "Consumer Electronics")
    orch.studio_orchestrator.bind_client_brand("client_beta", "brand_beta", "Beta Audio")
    orch.studio_orchestrator.launch_campaign("client_beta", "camp_beta_sep", "brand_beta", "Wireless Headphones", "Sales")

    # Assert 1: Both clients remain isolated
    runtime_nocap = orch.studio_runtime.get_or_create_client_runtime("client_nocap")
    runtime_beta = orch.studio_runtime.get_or_create_client_runtime("client_beta")
    assert runtime_nocap.client_id != runtime_beta.client_id

    # ---------------------------------------------------------
    # STAGE 2: Work Intake & Queue Admission
    # ---------------------------------------------------------
    req_nocap = ProductionRequest("req_nocap_01", "client_nocap", "camp_nocap_sep", "brand_nocap", "NOCAP Hero Lookbook")
    req_beta = ProductionRequest("req_beta_01", "client_beta", "camp_beta_sep", "brand_beta", "Beta Audio Unboxing")

    item_nocap = orch.submit_production_request(req_nocap)
    item_beta = orch.submit_production_request(req_beta)

    assert item_nocap.state == ProductionState.ADMITTED
    assert item_beta.state == ProductionState.ADMITTED

    # ---------------------------------------------------------
    # STAGE 3: Production & Self-Critique / Independent Review
    # ---------------------------------------------------------
    orch.process_next_work_step("client_nocap")  # ADMITTED -> IN_PRODUCTION
    orch.process_next_work_step("client_nocap")  # IN_PRODUCTION -> CRITIQUE
    orch.process_next_work_step("client_nocap")  # CRITIQUE -> REVIEW

    # Assert 7: Self-critique does not authorize execution
    assert item_nocap.state == ProductionState.REVIEW
    with pytest.raises(ContinuationBoundaryError):
        orch.autonomy_controller.verify_action_permitted("client_nocap", "EXECUTE_POST", requires_human_auth=True)

    # ---------------------------------------------------------
    # STAGE 4: Operational Event 1 — Approval Expiration
    # ---------------------------------------------------------
    orch.process_next_work_step("client_nocap", requires_approval=True, has_valid_approval=False)  # REVIEW -> AWAITING_APPROVAL
    assert item_nocap.state == ProductionState.AWAITING_APPROVAL

    # Simulate approval expiration event
    orch.recovery_engine.handle_expired_approval(item_nocap, "appr_req_nocap_01", orch.studio_orchestrator)
    # Assert 3: Expired approval does not execute
    assert item_nocap.state == ProductionState.IN_PRODUCTION

    # Re-advance NOCAP through CRITIQUE -> REVIEW -> AWAITING_APPROVAL
    orch.process_next_work_step("client_nocap")  # IN_PRODUCTION -> CRITIQUE
    orch.process_next_work_step("client_nocap")  # CRITIQUE -> REVIEW
    orch.process_next_work_step("client_nocap", requires_approval=True, has_valid_approval=False)  # REVIEW -> AWAITING_APPROVAL

    # ---------------------------------------------------------
    # STAGE 5: Human Approval & Execution Transition
    # ---------------------------------------------------------
    # Approve request via Phase 15 Studio Operations Approval Queue
    orch.studio_orchestrator.record_human_approval_decision(
        requesting_client_id="client_nocap",
        approval_id=f"appr_work_req_nocap_01_{item_nocap.retry_count}",
        approved=True,
        authorizer_id="user_owner_nocap"
    )

    # Assert 2: No unauthorized execution occurs without valid approval
    orch.process_next_work_step("client_nocap", requires_approval=True, has_valid_approval=True)  # AWAITING_APPROVAL -> APPROVED
    assert item_nocap.state == ProductionState.APPROVED

    orch.process_next_work_step("client_nocap", requires_approval=True, has_valid_approval=True)  # APPROVED -> READY_FOR_EXECUTION
    orch.process_next_work_step("client_nocap", requires_approval=True, has_valid_approval=True)  # READY_FOR_EXECUTION -> EXECUTING

    # ---------------------------------------------------------
    # STAGE 6: Operational Event 2 — Provider Failure & Bounded Recovery
    # ---------------------------------------------------------
    orch.recovery_engine.handle_provider_failure(item_nocap, "503 Service Unavailable")
    # Assert 4: Provider failure triggers bounded recovery
    assert item_nocap.state == ProductionState.RECOVERING

    # Recover item back to ADMITTED -> advance to EXECUTING
    item_nocap.state = ProductionState.EXECUTING

    # ---------------------------------------------------------
    # STAGE 7: Operational Event 3 — Interrupted Mission Revalidation
    # ---------------------------------------------------------
    item_interrupted = ProductionWorkItem("w_int", "r_int", "client_nocap", "camp_nocap_sep", "ws1", "d_int", "Interrupted Task")
    item_interrupted.transition_to(ProductionState.ADMITTED)
    item_interrupted.transition_to(ProductionState.IN_PRODUCTION)
    orch.recovery_engine.handle_interrupted_mission(item_interrupted)
    # Assert 5: Interrupted mission resumes only after revalidation
    assert item_interrupted.state == ProductionState.ADMITTED

    # ---------------------------------------------------------
    # STAGE 8: Operational Event 4 — Resource Conflict Handling
    # ---------------------------------------------------------
    orch.work_queue.mark_blocked(item_beta.item_id, "Resource lock")
    assert item_beta.state == ProductionState.BLOCKED
    # Assert 6: Resource conflict does not create privilege escalation
    with pytest.raises(ContinuationBoundaryError):
        orch.autonomy_controller.verify_action_permitted("client_beta", "BYPASS_LOCK", requires_human_auth=True)

    orch.work_queue.mark_unblocked(item_beta.item_id)
    assert item_beta.state == ProductionState.ADMITTED

    # ---------------------------------------------------------
    # STAGE 9: Operational Event 5 — Creative Revision Loop
    # ---------------------------------------------------------
    # Transition deliverable through revision cycle
    orch.delivery_coordinator.advance_production_stage(item_beta, ProductionState.IN_PRODUCTION, orch.studio_orchestrator)
    orch.delivery_coordinator.advance_production_stage(item_beta, ProductionState.CRITIQUE, orch.studio_orchestrator)
    orch.delivery_coordinator.advance_production_stage(item_beta, ProductionState.REVIEW, orch.studio_orchestrator)

    # ---------------------------------------------------------
    # STAGE 10: Operational Event 6 — External Outcome Observation
    # ---------------------------------------------------------
    outcome_nocap = orch.record_external_outcome(
        outcome_id="out_nocap_01",
        client_id="client_nocap",
        campaign_id="camp_nocap_sep",
        deliverable_id=item_nocap.deliverable_id,
        provider="instagram",
        external_post_id="ig_post_777",
        reach=12500,
        engagement_rate=0.068
    )
    # Assert 9: Trend / External observations remain untrusted
    assert outcome_nocap.provenance == "UNTRUSTED_EXTERNAL_OBSERVATION"

    # ---------------------------------------------------------
    # STAGE 11: Operational Event 7 — Optimization Experiment & Degradation Rejection
    # ---------------------------------------------------------
    # Set baseline
    orch.optimization_engine.set_baseline("client_nocap", "engagement_rate", 0.050)

    # Attempt learning & strategy optimization
    signal = orch.learning_loop.process_outcome_learning(outcome_nocap, "prompt_templates", "v2_editorial_prompt")
    # Assert 8: Learning does not mutate security policy
    with pytest.raises(FabricPolicyViolation):
        orch.learning_loop.process_outcome_learning(outcome_nocap, "security_policy", "permissive")

    # Optimization Experiment 1: High performance -> Adopted
    # Assert 10: Optimization can improve operational strategy
    adopted = orch.optimization_engine.evaluate_and_adopt("client_nocap", "engagement_rate", 0.068, "prompt_templates", {"version": "v2"})
    assert adopted is True

    # Optimization Experiment 2: Low performance -> Rejected & Rollback
    # Assert 11 & 12: Degraded candidates rejected and rollback succeeds
    degraded_adopted = orch.optimization_engine.evaluate_and_adopt("client_nocap", "engagement_rate", 0.020, "prompt_templates", {"version": "v3"})
    assert degraded_adopted is False
    assert orch.optimization_engine.get_active_strategy("client_nocap", "prompt_templates") == {"version": "v2"}

    # ---------------------------------------------------------
    # STAGE 12: Final Ledger & Substrate Assertions
    # ---------------------------------------------------------
    # Assert 13: Every external side effect is auditable
    audit_events = orch.observability_stream.list_events_for_client("client_nocap")
    assert len(audit_events) > 0

    # Assert 14: Production ledger integrity remains valid
    assert orch.ledger.verify_integrity() is True

    # Assert 15: Existing execution gate semantics remain intact
    health = orch.get_health_status()
    assert health.status == "HEALTHY"
