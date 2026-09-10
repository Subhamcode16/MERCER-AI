"""
End-to-End Real Workflow Benchmark: NOCAP Monthly Social Campaign.

Simulates a long-running campaign mission across Day 0 research/planning,
AI staff delegation, quality evaluation, dry-run planning, human authorization,
controlled sandbox execution, safe interruption/checkpointing, 8-point revalidation,
resumption, and Phase 9 learning feedback.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.mission_control.coordinator import MissionCoordinator
from src.mission_control.mission_models import MissionBudget, MissionAuthorizationContext
from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.resource_scope import ResourceScope
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.adapters import (
    SocialPlatformAdapter,
    AssetStorageAdapter,
    ContentManagementAdapter,
    AnalyticsAdapter,
)


def test_nocap_real_workflow_benchmark(tmp_path):
    # 1. Initialize Coordinator & Register Sandbox Adapters
    coord = MissionCoordinator()
    coord.execution_controller.register_adapter(SocialPlatformAdapter())
    coord.execution_controller.register_adapter(AssetStorageAdapter())
    coord.execution_controller.register_adapter(ContentManagementAdapter())
    coord.execution_controller.register_adapter(AnalyticsAdapter())

    mission_id = "mission_nocap_september_2026"
    now = datetime.now(timezone.utc)

    # 2. Create Mission
    mission = coord.create_mission(
        mission_id=mission_id,
        title="NOCAP Monthly Social Campaign",
        description="Execute complete streetwear visual campaign for September 2026",
        target_outcomes=["Research", "Visual Direction", "Content Production", "Sandbox Scheduling"],
        allowed_capabilities={"CREATE_DRAFT", "MODIFY_BRAND_ASSETS", "SCHEDULE_CONTENT"},
        allowed_resources={"campaign:nocap:september_2026"},
        budget=MissionBudget(token_budget=100000, max_tasks=10, max_executions=5),
    )

    coord.prepare_mission(mission_id)

    # 3. Add Workflow Tasks to Mission Graph
    t1 = coord.add_task(
        mission_id=mission_id,
        task_id="task_research",
        workflow_id="wf_nocap_01",
        assigned_role="TREND_ANALYST",
        description="Analyze streetwear visual trends for September 2026",
    )
    t2 = coord.add_task(
        mission_id=mission_id,
        task_id="task_visual_dir",
        workflow_id="wf_nocap_01",
        assigned_role="DESIGNER",
        description="Develop visual identity concepts and lookbook direction",
        dependencies=["task_research"],
    )
    t3 = coord.add_task(
        mission_id=mission_id,
        task_id="task_content_prod",
        workflow_id="wf_nocap_01",
        assigned_role="CONTENT_SPECIALIST",
        description="Generate social campaign copy and draft posts",
        dependencies=["task_visual_dir"],
    )

    coord.start_mission(mission_id)

    # 4. Execute Tasks 1 & 2
    res1 = coord.execute_next_task(mission_id)
    assert res1["task_id"] == "task_research"

    res2 = coord.execute_next_task(mission_id)
    assert res2["task_id"] == "task_visual_dir"

    # 5. Issue Phase 10 External Human Authorization Token
    scope = ResourceScope(scope_string="campaign:nocap:september_2026")
    auth_rec = coord.human_auth_boundary.issue_human_authorization(
        request_id="req_september_launch",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT, ExecutionCapability.SCHEDULE_CONTENT],
        resource_scope=scope,
        human_operator_id="brand_manager_human_01",
        decision_reference="DEC_APPROVE_SEPTEMBER",
        expires_at=(now + timedelta(hours=24)).isoformat(),
    )

    mission.authorization_context = MissionAuthorizationContext(
        authorization_token_id=auth_rec.authorization_id,
        authorized_by=auth_rec.authorizer_identity,
        expires_at=datetime.fromisoformat(auth_rec.expires_at),
        granted_capabilities={"CREATE_DRAFT", "SCHEDULE_CONTENT"},
        granted_resources={"campaign:nocap:september_2026"},
    )

    # 6. Execute Controlled Sandbox Action
    action = ExecutionAction(
        action_id="act_nocap_draft_01",
        workflow_id="wf_nocap_01",
        task_id="task_visual_dir",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap:september_2026"),
        input_payload={"title": "NOCAP Lookbook Launch", "media_url": "asset://lookbook_v1.png"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Create social draft"),
    )

    exec_res = coord.execute_controlled_action(
        mission_id=mission_id,
        action=action,
        authorization_record=auth_rec,
    )
    assert exec_res["execution_result"].success is True

    # 7. Safe Interruption & Checkpoint Creation while RUNNING
    coord.pause_mission(mission_id, reason="SIMULATED_INTERRUPTION")
    assert mission.state == "PAUSED"

    chk_id = f"chk_{mission_id}_{coord.step_counters[mission_id]:04d}"

    # 8. Resume Revalidation & Mission Continuation
    resume_res = coord.resume_mission(
        mission_id=mission_id,
        checkpoint_id=chk_id,
        authorization_context=mission.authorization_context,
    )
    assert resume_res.success is True
    assert mission.state == "RUNNING"

    # 9. Execute Final Task to Complete Mission
    res3 = coord.execute_next_task(mission_id)
    assert res3["task_id"] == "task_content_prod"
    assert mission.state == "COMPLETED"

    # 10. Verify Final Outcome & Ledger Integrity
    outcome = coord.get_outcome(mission_id)
    assert outcome.completed_tasks == 3
    assert outcome.executed_actions == 1
    assert coord.ledger.verify_ledger_integrity() is True
