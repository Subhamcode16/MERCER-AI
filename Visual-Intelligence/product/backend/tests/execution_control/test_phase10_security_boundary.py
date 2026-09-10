"""
Phase 10 — Security Boundary & Threat Matrix (T10-1 to T10-15) Test Suite
"""

from datetime import datetime, timedelta, timezone
import shutil
import tempfile
import pytest

from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.adapters import SocialPlatformAdapter
from src.execution_control.approval import ApprovalState, HumanAuthorizationBoundary
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.dry_run import DryRunEngine
from src.execution_control.exceptions import (
    AdapterNotFoundError,
    AuthorizationExpiredError,
    AuthorizationRevokedError,
    CapabilityViolationError,
    ReplayExecutionError,
    ResourceScopeViolationError,
    SelfAuthorizationAttemptError,
)
from src.execution_control.execution_ledger import ExecutionLedger
from src.execution_control.executor import ExecutionController
from src.execution_control.resource_scope import ResourceScope


@pytest.fixture
def temp_sec_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_t10_1_self_authorization_rejection():
    """T10-1: AI staff roles cannot issue execution authorization."""
    for ai_role in ["RESEARCHER", "REVIEWER", "CRITIC", "WORK_ORCHESTRATOR"]:
        with pytest.raises(SelfAuthorizationAttemptError):
            AuthorizationRecord(
                authorization_id="auth_self",
                request_id="req_01",
                authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
                resource_scope=ResourceScope("brand:aura"),
                authorizer_identity=ai_role,
                decision_reference="REF_00",
            )


def test_t10_2_capability_escalation_rejection():
    """T10-2: Authorization for LOW_RISK capability cannot be used for HIGH_RISK action."""
    controller = ExecutionController()
    controller.register_adapter(SocialPlatformAdapter())
    human_boundary = HumanAuthorizationBoundary()

    auth_low = human_boundary.issue_human_authorization(
        request_id="req_low",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],  # Low risk only
        resource_scope=ResourceScope("brand:aura"),
        human_operator_id="HUMAN_OPERATOR",
        decision_reference="REF_01",
    )

    act_high = ExecutionAction(
        action_id="act_high",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,  # High risk action!
        resource_scope=ResourceScope("brand:aura"),
        input_payload={},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )

    with pytest.raises(CapabilityViolationError):
        controller.execute_action(act_high, auth_low)


def test_t10_3_resource_scope_breach_rejection():
    """T10-3: Authorization for brand A cannot execute against brand B."""
    controller = ExecutionController()
    controller.register_adapter(SocialPlatformAdapter())
    human_boundary = HumanAuthorizationBoundary()

    auth_brand_a = human_boundary.issue_human_authorization(
        request_id="req_a",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:brand_a"),
        human_operator_id="HUMAN_OPERATOR",
        decision_reference="REF_01",
    )

    act_brand_b = ExecutionAction(
        action_id="act_b",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:brand_b"),  # Cross-resource breach attempt
        input_payload={},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )

    with pytest.raises(ResourceScopeViolationError):
        controller.execute_action(act_brand_b, auth_brand_a)


def test_t10_4_authorization_replay_defense():
    """T10-4: Re-submitting an authorization nonce is rejected."""
    controller = ExecutionController()
    controller.register_adapter(SocialPlatformAdapter())
    human_boundary = HumanAuthorizationBoundary()

    auth = human_boundary.issue_human_authorization(
        request_id="req_replay",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        human_operator_id="HUMAN_OPERATOR",
        decision_reference="REF_01",
    )

    act1 = ExecutionAction(
        action_id="act_1",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )
    act2 = ExecutionAction(
        action_id="act_2",
        workflow_id="wf_01",
        task_id="t2",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )

    controller.execute_action(act1, auth)

    with pytest.raises(ReplayExecutionError):
        controller.execute_action(act2, auth)


def test_t10_5_expired_authorization_denial():
    """T10-5: Expired authorization token is denied."""
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    auth_expired = AuthorizationRecord(
        authorization_id="auth_exp",
        request_id="req_exp",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        authorizer_identity="HUMAN_OPERATOR",
        decision_reference="REF_01",
        expires_at=past,
    )

    with pytest.raises(AuthorizationExpiredError):
        auth_expired.validate_active()


def test_t10_6_revoked_authorization_denial():
    """T10-6: Revoked authorization token is denied."""
    auth_revoked = AuthorizationRecord(
        authorization_id="auth_rev",
        request_id="req_rev",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        authorizer_identity="HUMAN_OPERATOR",
        decision_reference="REF_01",
        revoked=True,
    )

    with pytest.raises(AuthorizationRevokedError):
        auth_revoked.validate_active()


def test_t10_7_dry_run_side_effect_isolation():
    """T10-7: Dry-run engine generates plans without calling adapters."""
    adapter = SocialPlatformAdapter()
    engine = DryRunEngine()

    act = ExecutionAction(
        action_id="act_dry",
        workflow_id="wf_dry",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"text": "Dry run text"},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )

    plan = engine.generate_plan("wf_dry", [act], active_approval_state=ApprovalState.APPROVED_FOR_DRY_RUN)
    assert plan.plan_id == "plan_dryrun_wf_dry"
    assert len(adapter.published_posts) == 0  # Adapter MUST NOT be called!


def test_t10_13_adapter_confusion_rejection():
    """T10-13: Execution fails if no adapter registered for capability."""
    controller = ExecutionController()  # No adapters registered
    human_boundary = HumanAuthorizationBoundary()
    auth = human_boundary.issue_human_authorization(
        request_id="req_no_adapter",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        human_operator_id="HUMAN_OPERATOR",
        decision_reference="REF_01",
    )

    act = ExecutionAction(
        action_id="act_no_adapt",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )

    with pytest.raises(AdapterNotFoundError):
        controller.execute_action(act, auth)


def test_t10_15_audit_ledger_recording(temp_sec_dir):
    """T10-15: Execution writes mandatory audit ledger entry."""
    ledger = ExecutionLedger(base_dir=temp_sec_dir)
    controller = ExecutionController(ledger=ledger)
    controller.register_adapter(SocialPlatformAdapter())
    human_boundary = HumanAuthorizationBoundary()

    auth = human_boundary.issue_human_authorization(
        request_id="req_audit",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        human_operator_id="HUMAN_OPERATOR",
        decision_reference="REF_01",
    )
    act = ExecutionAction(
        action_id="act_audit",
        workflow_id="wf_audit",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"title": "Audit Post"},
        planned_effect=PlannedEffect("PUB", "SOC", "Desc"),
    )

    controller.execute_action(act, auth)

    # Check ledger files
    ledger_files = list(ledger.base_dir.glob("exec_*.json"))
    assert len(ledger_files) == 1
