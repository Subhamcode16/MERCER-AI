"""
Real Workflow Execution Benchmark Test: Modern Minimalist Fashion Lookbook Campaign.

Validates end-to-end multi-agent orchestration, defect injection, self-critique,
bounded revision loop, independent review, learning signal emission, second-run strategy update,
and strict non-authoritative execution gate lock (ExecutionGate.is_permitted() == False).
"""

from src.security_substrate import ExecutionGate, AssuranceLoopController
from src.agentic_work import WorkOrchestrator, AdaptiveStatus


def test_real_workflow_lookbook_campaign_with_learning_loop():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    orchestrator = WorkOrchestrator(execution_gate=gate)

    # ------------------------------------------------------------------------
    # Run 1: Execute workflow with injected defect (color clash #FF0000)
    # ------------------------------------------------------------------------
    run1_res = orchestrator.execute_workflow(
        objective="Modern Minimalist Fashion Lookbook Campaign 2026",
        brand_params={"aesthetic": "minimalist", "tone": "elevated quiet luxury"},
        inject_defect=True,
    )

    assert run1_res["objective"] == "Modern Minimalist Fashion Lookbook Campaign 2026"
    assert run1_res["status"] == "COMPLETED"
    assert run1_res["revision_count"] == 1  # Self-critique caught defect and revised!
    assert run1_res["review_passed"] is True
    assert run1_res["execution_gate_permitted"] is False

    # Check that learning signal was ingested into learning engine
    active_changes = orchestrator.learning_engine.list_active_changes()
    assert len(active_changes) >= 1
    assert active_changes[0].status == AdaptiveStatus.ACTIVE

    # ------------------------------------------------------------------------
    # Run 2: Execute second workflow utilizing learned strategy improvement
    # ------------------------------------------------------------------------
    run2_res = orchestrator.execute_workflow(
        objective="Modern Minimalist Summer Capsule Campaign 2026",
        brand_params={"aesthetic": "minimalist", "tone": "elevated quiet luxury"},
        inject_defect=False,
    )

    assert run2_res["status"] == "COMPLETED"
    assert run2_res["revision_count"] == 0  # Perfect first-pass execution!
    assert run2_res["review_passed"] is True
    assert run2_res["metrics"]["overall_quality_score"] >= 0.95
    assert run2_res["execution_gate_permitted"] is False

    # ------------------------------------------------------------------------
    # Non-authoritative Invariant Check
    # ------------------------------------------------------------------------
    assert gate.is_permitted() is False
