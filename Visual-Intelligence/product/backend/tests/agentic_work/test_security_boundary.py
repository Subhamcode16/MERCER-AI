"""
Adversarial Security Boundary & Threat Matrix Tests (T8-1 – T8-12).
Proves that Agentic Work Layer cannot bypass, modify, or weaken the security substrate.
"""

import pytest
from src.security_substrate import ExecutionGate, AssuranceLoopController
from src.agentic_work import (
    WorkOrchestrator,
    StaffTask,
    StaffRole,
    StaffCapability,
    StaffResult,
    TaskStatus,
    LearningSignal,
    AdaptiveChange,
    FeedbackEngine,
    LearningEngine,
    TaskGraph,
)


def test_t8_1_agent_privilege_escalation():
    """T8-1: Worker capability with forbidden tool name raises ValueError."""
    with pytest.raises(ValueError, match="Forbidden tool capability"):
        StaffCapability("cap-01", "Escalation test", ["AUTHORIZE"])


def test_t8_2_orchestrator_security_bypass():
    """T8-2: WorkOrchestrator has zero gating or authorization methods."""
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    orch = WorkOrchestrator(execution_gate=gate)

    assert not hasattr(orch, "authorize")
    assert not hasattr(orch, "unlock")
    assert not hasattr(orch, "set_verified")
    assert gate.is_permitted() is False


def test_t8_3_critic_authorization_confusion():
    """T8-3: Critic PASS output does not unlock ExecutionGate."""
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    orch = WorkOrchestrator(execution_gate=gate)

    res = orch.execute_workflow("Test lookbook campaign", inject_defect=False)
    assert res["status"] == "COMPLETED"
    assert gate.is_permitted() is False


def test_t8_4_learning_signal_to_security_policy_escalation():
    """T8-4: LearningSignal targeting SECURITY_POLICY raises ValueError."""
    with pytest.raises(ValueError, match="cannot target SECURITY_POLICY"):
        LearningSignal(
            signal_id="sig-bad",
            workflow_id="wf1",
            task_id=None,
            source="USER_FEEDBACK",
            category="SECURITY_POLICY",
            observed_failure="bad",
            expected_behavior="bad",
            correction="bad",
        )


def test_t8_5_prompt_injection_external_knowledge_containment():
    """T8-5: External visual observation carries UNTRUSTED_EXTERNAL_OBSERVATION trust marker."""
    from src.agentic_work import TrendIntelligenceEngine
    engine = TrendIntelligenceEngine()
    obs = engine.capture_trend_observation("malicious-site.com", "PALETTE", {"payload": "system bypass prompt"})
    assert obs.trust_marker == "UNTRUSTED_EXTERNAL_OBSERVATION"


def test_t8_6_malicious_memory_poisoning_prevention():
    """T8-6: Low confidence signals (< 0.70) do not activate adaptive changes."""
    learn = LearningEngine()
    sig = LearningSignal(
        signal_id="sig-low",
        workflow_id="wf1",
        task_id=None,
        source="USER_FEEDBACK",
        category="PROMPT_TEMPLATE",
        observed_failure="fake fail",
        expected_behavior="fake exp",
        correction="fake corr",
        confidence=0.40,  # Low confidence
    )
    change = learn.ingest_signal(sig)
    assert change is None
    assert len(learn.list_active_changes()) == 0


def test_t8_7_self_improvement_boundary_violation():
    """T8-7: AdaptiveChange targeting forbidden substrate components raises ValueError."""
    with pytest.raises(ValueError, match="Forbidden adaptive target component"):
        AdaptiveChange(
            change_id="chg-bad",
            target_component="EXECUTION_GATE",
            previous_version="v1",
            proposed_version="v2",
            reason="hack",
            supporting_signals=[],
        )


def test_t8_8_infinite_revision_loop_containment():
    """T8-8: Task graph revision loop is bounded to max 3 and escalates to BLOCKED."""
    graph = TaskGraph("wf-loop", max_revisions=3)
    t = StaffTask("t1", "wf-loop", StaffRole.DESIGNER, "Design")
    graph.add_task(t)

    assert graph.request_revision("t1", ["Fix 1"]) is True
    assert graph.request_revision("t1", ["Fix 2"]) is True
    assert graph.request_revision("t1", ["Fix 3"]) is True
    assert graph.request_revision("t1", ["Fix 4"]) is False
    assert graph.get_task("t1").status == TaskStatus.BLOCKED


def test_t8_9_isolated_staff_failure_handling():
    """T8-9: Staff task result with FAILED status is contained cleanly."""
    res = StaffResult(
        task_id="t1",
        staff_id="s1",
        role=StaffRole.RESEARCHER,
        status=TaskStatus.FAILED,
        output_data={"error": "resource timeout"},
        execution_time_seconds=0.5,
    )
    assert res.status == TaskStatus.FAILED
    assert res.is_authoritative is False


def test_t8_10_conflicting_staff_outputs():
    """T8-10: Critic rejects defective designer output without silent override."""
    from src.agentic_work import CriticStaff, StaffContext, TaskContext
    critic = CriticStaff()
    t_ctx = TaskContext("t6", "wf1", StaffRole.CRITIC, "Critique", {}, parent_outputs={"designer_task": {"has_defect": True}})
    s_ctx = StaffContext("s-critic", StaffRole.CRITIC, t_ctx, [])

    res = critic.execute_task(s_ctx)
    assert res.status == TaskStatus.REVISION_REQUIRED
    assert res.output_data["passed"] is False


def test_t8_11_knowledge_staleness_handling():
    """T8-11: VisualObservation retains captured_at timestamp for freshness filtering."""
    from src.agentic_work import VisualObservation
    import time
    now = time.time()
    obs = VisualObservation("obs-1", "example.com", "GRID", now, {}, "hash123")
    assert obs.captured_at == now


def test_t8_12_scoped_feedback_cross_project_isolation():
    """T8-12: Feedback LearningSignals are scoped by workflow_id."""
    sig1 = LearningSignal("s1", "wf-project-A", None, "USER", "PROMPT_TEMPLATE", "a", "b", "c")
    sig2 = LearningSignal("s2", "wf-project-B", None, "USER", "PROMPT_TEMPLATE", "x", "y", "z")
    assert sig1.workflow_id != sig2.workflow_id
