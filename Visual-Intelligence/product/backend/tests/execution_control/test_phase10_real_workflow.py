"""
Phase 10 — Real Sandbox Workflow Benchmark Test

End-to-End Sandbox Lookbook Publishing Campaign Workflow:
Campaign Brief -> Staff Graph Execution -> Critique -> Review -> Dry-Run -> Human Authorization -> Sandbox Execution -> Ledger Audit -> Phase 9 Learning Signal.
"""

import shutil
import tempfile
import pytest

from src.agentic_work import (
    StaffRole,
    StaffTask,
    TaskStatus,
    WorkOrchestrator,
)
from src.execution_control import (
    AdapterExecutionResult,
    AnalyticsAdapter,
    ApprovalState,
    AssetStorageAdapter,
    ContentManagementAdapter,
    DryRunEngine,
    ExecutionAction,
    ExecutionController,
    ExecutionCapability,
    ExecutionLedger,
    HumanAuthorizationBoundary,
    IdempotencyGuard,
    PlannedEffect,
    ResourceScope,
    SocialPlatformAdapter,
)
from src.security_substrate import AssuranceLoopController, ExecutionGate


@pytest.fixture
def temp_sandbox_env():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_sandbox_lookbook_publishing_workflow(temp_sandbox_env):
    ledger = ExecutionLedger(base_dir=f"{temp_sandbox_env}/ledger")
    controller = ExecutionController(ledger=ledger)

    # 1. Register Mock Sandbox Adapters
    cms_adapter = ContentManagementAdapter()
    asset_adapter = AssetStorageAdapter()
    social_adapter = SocialPlatformAdapter()

    controller.register_adapter(cms_adapter)
    controller.register_adapter(asset_adapter)
    controller.register_adapter(social_adapter)

    # 2. Execute Bounded Phase 8 Workflow (Staff Graph + Orchestration)
    orch = WorkOrchestrator()
    wf_res = orch.execute_workflow(
        objective="Modern Minimalist Fashion Lookbook Campaign 2026",
        brand_params={"aesthetic": "minimalist", "tone": "elevated quiet luxury"},
    )
    assert wf_res["status"] == "COMPLETED"
    assert wf_res["execution_gate_permitted"] is False

    # 3. Construct Executable Actions
    scope = ResourceScope("brand:aura/campaign:fall2026")

    act_draft = ExecutionAction(
        action_id="act_01_create_draft",
        workflow_id="wf_lookbook_p10",
        task_id="t3_content",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=scope,
        input_payload={"title": "AURA Fall 2026 Lookbook", "body": "Minimalist monochrome collection"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_CMS", "Create draft lookbook post", reversible=True),
    )

    act_asset = ExecutionAction(
        action_id="act_02_gen_asset",
        workflow_id="wf_lookbook_p10",
        task_id="t2_design",
        capability=ExecutionCapability.GENERATE_ASSET,
        resource_scope=scope,
        input_payload={"prompt": "Editorial Swiss Typography Grid"},
        planned_effect=PlannedEffect("GENERATE_ASSET", "SANDBOX_ASSET_STORE", "Generate visual asset", reversible=True),
    )

    act_publish = ExecutionAction(
        action_id="act_03_publish",
        workflow_id="wf_lookbook_p10",
        task_id="t3_content",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=scope,
        input_payload={"text": "AURA Fall 2026 Collection Live"},
        planned_effect=PlannedEffect("PUBLISH_CONTENT", "SANDBOX_SOCIAL", "Publish social campaign", reversible=False),
    )

    actions = [act_draft, act_asset, act_publish]

    # 4. Generate Dry-Run Plan
    dry_run_engine = DryRunEngine()
    dry_run_plan = dry_run_engine.generate_plan(
        workflow_id="wf_lookbook_p10",
        actions=actions,
        active_approval_state=ApprovalState.APPROVED_FOR_DRY_RUN,
    )

    assert len(dry_run_plan.actions) == 3
    assert len(cms_adapter.drafts) == 0  # Zero side-effects during dry run!
    assert len(social_adapter.published_posts) == 0

    # 5. Issue Explicit Human Authorization Record
    human_boundary = HumanAuthorizationBoundary()
    auth_record = human_boundary.issue_human_authorization(
        request_id="req_lookbook_publish",
        authorized_capabilities=[
            ExecutionCapability.CREATE_DRAFT,
            ExecutionCapability.GENERATE_ASSET,
            ExecutionCapability.PUBLISH_CONTENT,
        ],
        resource_scope=scope,
        human_operator_id="HUMAN_OPERATOR_CHIEF_EDITOR",
        decision_reference="DECISION_REF_LOOKBOOK_2026",
    )

    # 6. Execute Batch via ExecutionController
    results = controller.execute_batch(actions, authorization_record=auth_record)

    assert len(results) == 3
    assert all(r.success for r in results)
    assert len(cms_adapter.drafts) == 1
    assert len(asset_adapter.stored_assets) == 1
    assert len(social_adapter.published_posts) == 1

    # 7. Verify Execution Ledger Audit Records
    ledger_records = list(ledger.base_dir.glob("exec_*.json"))
    assert len(ledger_records) == 3
