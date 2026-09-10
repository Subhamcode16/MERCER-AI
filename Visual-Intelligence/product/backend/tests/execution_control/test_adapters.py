"""
Phase 10 — Integration Adapters Unit Tests
"""

from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.adapters import (
    AnalyticsAdapter,
    AssetStorageAdapter,
    ContentManagementAdapter,
    SocialPlatformAdapter,
)
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope


def test_social_platform_adapter():
    adapter = SocialPlatformAdapter()

    act_pub = ExecutionAction(
        action_id="act_pub",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"text": "Hello World"},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )

    res = adapter.execute_action(act_pub)
    assert res.success is True
    assert res.output_data["status"] == "PUBLISHED"
    assert len(adapter.published_posts) == 1


def test_asset_storage_adapter():
    adapter = AssetStorageAdapter()

    act_gen = ExecutionAction(
        action_id="act_gen",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.GENERATE_ASSET,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"prompt": "Lookbook visual"},
        planned_effect=PlannedEffect("GEN", "STORAGE", "Desc"),
    )

    res = adapter.execute_action(act_gen)
    assert res.success is True
    assert "asset_id" in res.output_data
    assert len(adapter.stored_assets) == 1


def test_content_management_adapter():
    adapter = ContentManagementAdapter()

    act_draft = ExecutionAction(
        action_id="act_draft",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"title": "Draft 01"},
        planned_effect=PlannedEffect("DRAFT", "CMS", "Desc"),
    )

    res = adapter.execute_action(act_draft)
    assert res.success is True
    assert res.output_data["status"] == "DRAFT_CREATED"
    assert len(adapter.drafts) == 1


def test_analytics_adapter():
    adapter = AnalyticsAdapter()

    act_read = ExecutionAction(
        action_id="act_read",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.READ_ANALYTICS,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"metrics": ["impressions"]},
        planned_effect=PlannedEffect("READ", "ANALYTICS", "Desc"),
    )

    res = adapter.execute_action(act_read)
    assert res.success is True
    assert "impressions" in res.output_data
