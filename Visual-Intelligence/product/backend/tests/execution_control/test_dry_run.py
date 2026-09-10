"""
Phase 10 — Dry-Run Engine Unit Tests
"""

from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.approval import ApprovalState
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.dry_run import DryRunEngine
from src.execution_control.resource_scope import ResourceScope


def test_dry_run_plan_generation():
    engine = DryRunEngine()

    act1 = ExecutionAction(
        action_id="act_01",
        workflow_id="wf_dry",
        task_id="t1",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"title": "Lookbook Draft"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_CMS", "Creates lookbook post draft", reversible=True),
    )

    act2 = ExecutionAction(
        action_id="act_02",
        workflow_id="wf_dry",
        task_id="t2",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"draft_id": "draft_01"},
        planned_effect=PlannedEffect("PUBLISH", "SANDBOX_SOCIAL", "Publishes post online", reversible=False),
    )

    plan = engine.generate_plan(
        workflow_id="wf_dry",
        actions=[act1, act2],
        active_approval_state=ApprovalState.APPROVED_FOR_DRY_RUN,
    )

    assert plan.workflow_id == "wf_dry"
    assert len(plan.actions) == 2
    assert "CREATE_DRAFT" in plan.required_capabilities
    assert "PUBLISH_CONTENT" in plan.required_capabilities
    assert plan.approval_status == ApprovalState.APPROVED_FOR_DRY_RUN
    assert "# Execution Plan Dry-Run Simulation Brief" in plan.markdown_brief
    assert "SANDBOX_CMS" in plan.target_systems
    assert "SANDBOX_SOCIAL" in plan.target_systems
