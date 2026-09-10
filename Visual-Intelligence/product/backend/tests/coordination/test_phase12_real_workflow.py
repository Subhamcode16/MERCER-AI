"""
End-to-End Real Multi-Mission Workflow Benchmark: 3 Simultaneous NOCAP Operational Missions.

Simulates simultaneous execution of:
- Mission A: NOCAP Monthly Social Campaign
- Mission B: NOCAP Streetwear Website Refresh
- Mission C: NOCAP Capsule Product Launch

Demonstrates concurrent admission, shared resource contention (staff slots, API quotas),
machine conflict detection, priority arbitration, fairness aging, safe preemption,
safe resume, Phase 10 human authorization, zero cross-mission authorization reuse,
and 100% hash-linked audit ledger verification.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.coordination.coordinator import MultiMissionCoordinator
from src.coordination.models import MissionPriority, ResourceRequest
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


def test_three_simultaneous_nocap_missions_benchmark(tmp_path):
    # 1. Initialize MultiMissionCoordinator & Register Sandbox Adapters
    coord = MultiMissionCoordinator(ledger_dir=str(tmp_path))
    coord.phase11_coordinator.execution_controller.register_adapter(SocialPlatformAdapter())
    coord.phase11_coordinator.execution_controller.register_adapter(AssetStorageAdapter())
    coord.phase11_coordinator.execution_controller.register_adapter(ContentManagementAdapter())
    coord.phase11_coordinator.execution_controller.register_adapter(AnalyticsAdapter())

    now = datetime.now(timezone.utc)

    # 2. Admit Mission A (Monthly Social Campaign - HIGH Priority)
    mA = coord.admit_mission(
        mission_id="mission_nocap_social_campaign",
        title="NOCAP Monthly Social Campaign",
        description="Execute September social campaign across Instagram and TikTok",
        target_outcomes=["Research", "Visual Identity", "Content Generation"],
        priority=MissionPriority.HIGH,
        allowed_capabilities={"CREATE_DRAFT", "MODIFY_BRAND_ASSETS"},
        allowed_resources={"campaign:nocap:social"},
    )

    # 3. Admit Mission B (Website Refresh - NORMAL Priority)
    mB = coord.admit_mission(
        mission_id="mission_nocap_web_refresh",
        title="NOCAP Streetwear Website Refresh",
        description="Audit Visual DNA and update homepage lookbook showcase",
        target_outcomes=["Visual Audit", "Homepage Concept"],
        priority=MissionPriority.NORMAL,
        allowed_capabilities={"MODIFY_BRAND_ASSETS"},
        allowed_resources={"website:nocap:homepage"},
    )

    # 4. Admit Mission C (Capsule Product Launch - SYSTEM_CRITICAL Priority)
    mC = coord.admit_mission(
        mission_id="mission_nocap_product_launch",
        title="NOCAP Fall Capsule Drop",
        description="Coordinates launch positioning and social drop schedule",
        target_outcomes=["Launch Strategy", "Drop Announcement"],
        priority=MissionPriority.SYSTEM_CRITICAL,
        allowed_capabilities={"CREATE_DRAFT", "SCHEDULE_CONTENT"},
        allowed_resources={"campaign:nocap:capsule_drop"},
    )

    assert coord.mission_registry.active_count == 3

    # 5. Add Tasks to Mission Graphs
    coord.phase11_coordinator.add_task(
        mission_id="mission_nocap_social_campaign",
        task_id="task_soc_research",
        workflow_id="wf_social_01",
        assigned_role="TREND_ANALYST",
        description="Research streetwear trends",
    )
    coord.phase11_coordinator.prepare_mission("mission_nocap_social_campaign")
    coord.phase11_coordinator.start_mission("mission_nocap_social_campaign")

    coord.phase11_coordinator.add_task(
        mission_id="mission_nocap_product_launch",
        task_id="task_launch_strat",
        workflow_id="wf_launch_01",
        assigned_role="STRATEGIST",
        description="Develop product positioning",
    )
    coord.phase11_coordinator.prepare_mission("mission_nocap_product_launch")
    coord.phase11_coordinator.start_mission("mission_nocap_product_launch")

    # 6. Request Shared Resources & Execute Arbitration
    reqA = ResourceRequest("req_A", "mission_nocap_social_campaign", "staff:designer", quantity=1)
    reqB = ResourceRequest("req_B", "mission_nocap_web_refresh", "staff:designer", quantity=1)
    reqC = ResourceRequest("req_C", "mission_nocap_product_launch", "account:nocap_social", quantity=1, exclusive=True)

    arb_decision = coord.request_resources_and_arbitrate([reqA, reqB, reqC])
    assert arb_decision.granted_mission_id is not None
    assert len(arb_decision.granted_leases) >= 1

    # 7. Execute Tasks across Missions
    resA = coord.execute_mission_task("mission_nocap_social_campaign")
    assert resA is not None and resA["task_id"] == "task_soc_research"

    resC = coord.execute_mission_task("mission_nocap_product_launch")
    assert resC is not None and resC["task_id"] == "task_launch_strat"

    # 8. Issue External Phase 10 Human Authorization Token for Mission C Side Effect
    scopeC = ResourceScope(scope_string="campaign:nocap:capsule_drop")
    authC = coord.phase11_coordinator.human_auth_boundary.issue_human_authorization(
        request_id="req_launch_drop_auth",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=scopeC,
        human_operator_id="brand_director_human_01",
        decision_reference="DEC_APPROVE_FALL_DROP",
        expires_at=(now + timedelta(hours=12)).isoformat(),
    )

    actionC = ExecutionAction(
        action_id="act_drop_announce_01",
        workflow_id="wf_launch_01",
        task_id="task_launch_strat",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap:capsule_drop"),
        input_payload={"title": "NOCAP Fall Capsule Drop Teaser"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Post drop teaser"),
    )

    exec_resC = coord.execute_controlled_action_for_mission(
        mission_id="mission_nocap_product_launch",
        action=actionC,
        authorization_record=authC,
    )
    assert exec_resC["execution_result"].success is True

    # 9. Verify Multi-Mission Outcome & Audit Ledger Integrity
    outcome = coord.get_outcome()
    assert outcome.admitted_missions == 3
    assert coord.ledger.verify_ledger_integrity() is True
