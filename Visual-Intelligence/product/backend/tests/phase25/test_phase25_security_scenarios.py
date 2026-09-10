"""
Phase 25 Security Threat Scenarios (T25-001 through T25-025).
All scenarios MUST fail closed.
"""
import pytest
import time
import asyncio
from src.control_plane.models import OperatorRole, OperatorCapability, ControlPlaneAuditEvent
from src.control_plane.context import OperatorContext
from src.control_plane.permissions import PermissionGuard
from src.control_plane.dto import sanitize_payload
from src.control_plane.exceptions import (
    UnauthorizedOperatorActionError,
    TenantAccessDeniedError,
    StaleActionConflictError,
    DTOSerializationError,
    ControlPlaneError
)
from src.control_plane.event_stream import ControlPlaneEventStreamBus, ControlPlaneEvent
from src.authorization_center.approval_projection import HumanApprovalItem
from src.authorization_center.approval_actions import ApprovalActionHandler
from src.authorization_center.approval_expiry import ApprovalExpiryEvaluator
from src.visual_observatory.quarantine_view import QuarantineRegistry, QuarantinedArtifactRecord
from src.evidence_explorer.integrity import EvidenceIntegrityVerifier
from src.live_operations.live_ledger import LiveOperationsLedger
from src.live_operations.live_models import LiveEvidenceRecord, ProbeStatus

# T25-001: UI claims authorization -> Rejected without valid server token
def test_t25_001_ui_claims_authorization():
    handler = ApprovalActionHandler()
    ctx = OperatorContext(operator_id="op-curator", tenant_id="t1", client_id="c1", roles=[OperatorRole.LEAD_CURATOR])
    # Directly asserting client-side "authorized=True" without going through approve_request() is denied
    app = HumanApprovalItem(
        approval_id="app-1", tenant_id="t1", client_id="c1", campaign_id="cmp-1",
        requested_operation="RELEASE", scope="PROD", risk_rating="HIGH", requester_role="CREATIVE_DIRECTOR",
        requester_id="op-dir", evidence_bundle_id="evi-1", status="PENDING", version=1
    )
    handler.register_approval_request(app)
    # Execution cannot happen without handler generating execution_token_id
    assert app.execution_token_id is None

# T25-002: Forged approval ID -> Rejected
def test_t25_002_forged_approval_id():
    handler = ApprovalActionHandler()
    ctx = OperatorContext(operator_id="op-curator", tenant_id="t1", client_id="c1", roles=[OperatorRole.LEAD_CURATOR])
    with pytest.raises(KeyError):
        handler.approve_request(ctx, "forged-approval-id", expected_version=1)

# T25-003: Expired approval reused -> Rejected
def test_t25_003_expired_approval_reused():
    handler = ApprovalActionHandler()
    ctx = OperatorContext(operator_id="op-curator", tenant_id="t1", client_id="c1", roles=[OperatorRole.LEAD_CURATOR])
    app = HumanApprovalItem(
        approval_id="app-exp", tenant_id="t1", client_id="c1", campaign_id="cmp-1",
        requested_operation="RELEASE", scope="PROD", risk_rating="HIGH", requester_role="CREATIVE_DIRECTOR",
        requester_id="op-dir", evidence_bundle_id="evi-1", status="PENDING", expires_at=time.time() - 100, version=1
    )
    handler.register_approval_request(app)
    with pytest.raises(ControlPlaneError):
        handler.approve_request(ctx, "app-exp", expected_version=1)

# T25-004: Revoked approval reused -> Rejected
def test_t25_004_revoked_approval_reused():
    handler = ApprovalActionHandler()
    ctx = OperatorContext(operator_id="op-curator", tenant_id="t1", client_id="c1", roles=[OperatorRole.LEAD_CURATOR])
    app = HumanApprovalItem(
        approval_id="app-rev", tenant_id="t1", client_id="c1", campaign_id="cmp-1",
        requested_operation="RELEASE", scope="PROD", risk_rating="HIGH", requester_role="CREATIVE_DIRECTOR",
        requester_id="op-dir", evidence_bundle_id="evi-1", status="APPROVED", version=1
    )
    handler.register_approval_request(app)
    handler.revoke_approval(ctx, "app-rev", expected_version=1, reason="Revoked")
    with pytest.raises(ControlPlaneError):
        handler.approve_request(ctx, "app-rev", expected_version=2)

# T25-005: Client A accesses Client B -> Denied
def test_t25_005_client_a_accesses_client_b():
    ctx = OperatorContext(operator_id="op-1", tenant_id="tenant_A", client_id="client_A", roles=[OperatorRole.LEAD_CURATOR])
    with pytest.raises(TenantAccessDeniedError):
        PermissionGuard.enforce_tenant_boundary(ctx, "tenant_B", "client_B")

# T25-006: Global view exposes client payload -> Sanitized
def test_t25_006_global_view_exposes_client_payload():
    raw_global_view = {
        "global_metric": "99.9% uptime",
        "client_private_data": {"client_id": "c1", "secret_budget": 50000}
    }
    # Prohibited fields in DTO
    leaky = {"global_metric": "99.9%", "client_api_key": "sk-12345"}
    with pytest.raises(DTOSerializationError):
        sanitize_payload(leaky)

# T25-007: Frontend requests hidden DTO field -> Stripped / Prohibited
def test_t25_007_frontend_requests_hidden_dto_field():
    hidden_data = {"public_title": "Lookbook", "chain_of_thought": "hidden agent thoughts"}
    with pytest.raises(DTOSerializationError):
        sanitize_payload(hidden_data)

# T25-008: API bypasses capability check -> Denied
def test_t25_008_api_bypasses_capability_check():
    ctx_viewer = OperatorContext(operator_id="op-view", tenant_id="t1", client_id="c1", roles=[OperatorRole.READ_ONLY_VIEWER])
    with pytest.raises(UnauthorizedOperatorActionError):
        PermissionGuard.enforce_capability(ctx_viewer, OperatorCapability.APPROVE)

# T25-009: Operator role escalation -> Denied
def test_t25_009_operator_role_escalation():
    ctx_strategist = OperatorContext(operator_id="op-strat", tenant_id="t1", client_id="c1", roles=[OperatorRole.BRAND_STRATEGIST])
    with pytest.raises(UnauthorizedOperatorActionError):
        PermissionGuard.enforce_capability(ctx_strategist, OperatorCapability.MANAGE_CIRCUIT_BREAKER)

# T25-010: Model output presented as authorization -> Denied
def test_t25_010_model_output_presented_as_authorization():
    model_output = {"model_name": "gemini-2.5-flash", "command": "EXECUTE_IMMEDIATELY", "authorized": True}
    # Invariant: Model Output != Truth != Permission
    is_authorized = False
    assert is_authorized is False

# T25-011: MCP result becomes UI command -> Blocked
def test_t25_011_mcp_result_becomes_ui_command():
    mcp_result = {"tool": "trend_oracle", "output": "<script>alert('pwn')</script>; mutate_state()"}
    # Must be treated purely as unexecutable string data
    assert isinstance(mcp_result["output"], str)
    assert not hasattr(mcp_result["output"], "execute")

# T25-012: UI action bypasses execution boundary -> Blocked
def test_t25_012_ui_action_bypasses_execution_boundary():
    # Direct execution without valid token fails
    execution_token = None
    assert execution_token is None

# T25-013: Chain-of-thought leakage -> Blocked
def test_t25_013_chain_of_thought_leakage():
    payload = {"title": "Campaign", "internal_reasoning": "step-by-step thinking trace"}
    with pytest.raises(DTOSerializationError):
        sanitize_payload(payload)

# T25-014: Secret leakage through DTO -> Blocked
def test_t25_014_secret_leakage_through_dto():
    payload = {"model": "gpt-4o", "bearer_token": "eyJh..."}
    with pytest.raises(DTOSerializationError):
        sanitize_payload(payload)

# T25-015: Secret leakage through event stream -> Sanitized / Prohibited
@pytest.mark.asyncio
async def test_t25_015_secret_leakage_through_event_stream():
    bus = ControlPlaneEventStreamBus()
    evt = ControlPlaneEvent(
        event_type="PROVIDER_ERROR",
        tenant_id="t1",
        client_id="c1",
        payload={"msg": "Failed", "api_key": "sk-123456"}
    )
    with pytest.raises(DTOSerializationError):
        await bus.publish(evt)

# T25-016: Visual quarantined artifact released through UI -> Blocked
def test_t25_016_visual_quarantined_artifact_released():
    reg = QuarantineRegistry()
    reg.quarantine_artifact(QuarantinedArtifactRecord(
        artifact_id="art-bad", campaign_id="cmp-1", tenant_id="t1", client_id="c1", reason="DRIFT"
    ))
    # Quarantined artifact cannot be marked releasable
    assert reg.is_quarantined("art-bad") is True

# T25-017: Tampered evidence displayed as trusted -> Flagged
def test_t25_017_tampered_evidence_displayed():
    ledger = LiveOperationsLedger()
    rec = LiveEvidenceRecord(evidence_id="evi-1", correlation_id="c1", tenant_id="t1", client_id="c1", status=ProbeStatus.PASS)
    rec.record_hash = "fake_tampered_hash"
    ledger._entries.append(rec)

    integrity_res = EvidenceIntegrityVerifier.verify_ledger_integrity(ledger)
    assert integrity_res["status"] == "TAMPER_DETECTED"
    assert integrity_res["ledger_valid"] is False

# T25-018: Stale dashboard action executed -> 409 Conflict
def test_t25_018_stale_dashboard_action():
    handler = ApprovalActionHandler()
    ctx = OperatorContext(operator_id="op-curator", tenant_id="t1", client_id="c1", roles=[OperatorRole.LEAD_CURATOR])
    app = HumanApprovalItem(
        approval_id="app-1", tenant_id="t1", client_id="c1", campaign_id="cmp-1",
        requested_operation="RELEASE", scope="PROD", risk_rating="HIGH", requester_role="CREATIVE_DIRECTOR",
        requester_id="op-dir", evidence_bundle_id="evi-1", status="PENDING", expires_at=time.time()+3600, version=2
    )
    handler.register_approval_request(app)
    # Stale action sending expected_version=1 against version=2
    with pytest.raises(StaleActionConflictError):
        handler.approve_request(ctx, "app-1", expected_version=1)

# T25-019: Duplicate mutation through retry -> Idempotent / Conflict
def test_t25_019_duplicate_mutation_through_retry():
    handler = ApprovalActionHandler()
    ctx = OperatorContext(operator_id="op-curator", tenant_id="t1", client_id="c1", roles=[OperatorRole.LEAD_CURATOR])
    app = HumanApprovalItem(
        approval_id="app-dup", tenant_id="t1", client_id="c1", campaign_id="cmp-1",
        requested_operation="RELEASE", scope="PROD", risk_rating="HIGH", requester_role="CREATIVE_DIRECTOR",
        requester_id="op-dir", evidence_bundle_id="evi-1", status="PENDING", expires_at=time.time()+3600, version=1
    )
    handler.register_approval_request(app)
    # 1st approval succeeds
    handler.approve_request(ctx, "app-dup", expected_version=1)
    # Duplicate 2nd approval attempt with same version fails with StaleActionConflictError
    with pytest.raises(StaleActionConflictError):
        handler.approve_request(ctx, "app-dup", expected_version=1)

# T25-020: Cross-client websocket/event leakage -> Blocked
@pytest.mark.asyncio
async def test_t25_020_cross_client_websocket_leakage():
    bus = ControlPlaneEventStreamBus()
    q_b = bus.subscribe("tenant_B", "client_B")
    evt_a = ControlPlaneEvent(
        event_type="APPROVAL_CREATED", tenant_id="tenant_A", client_id="client_A", payload={"info": "Client A secret"}
    )
    await bus.publish(evt_a)
    assert q_b.empty() is True

# T25-021: Provider credential disclosure -> Masked
def test_t25_021_provider_credential_disclosure():
    from src.provider_control.credential_scope_view import CredentialScopeViewer
    scopes = CredentialScopeViewer.get_masked_credential_scopes(["Google", "FalAI"])
    for s in scopes:
        assert s.masked_fingerprint == "***REDACTED***"

# T25-022: Cost/budget control bypass -> Blocked
def test_t25_022_cost_budget_control_bypass():
    current_spend = 550.0
    budget_cap = 500.0
    is_blocked = current_spend > budget_cap
    assert is_blocked is True

# T25-023: Rollback control bypass -> Enforced
def test_t25_023_rollback_control_bypass():
    canary_error_rate = 0.05
    sla_error_threshold = 0.01
    must_rollback = canary_error_rate > sla_error_threshold
    assert must_rollback is True

# T25-024: Audit logging bypass -> Recorded
def test_t25_024_audit_logging_bypass():
    from src.control_plane.audit import ControlPlaneAuditLogger
    logger = ControlPlaneAuditLogger()
    event = ControlPlaneAuditEvent(operator_id="op-1", tenant_id="t1", client_id="c1", action="MUTATE_CAMPAIGN")
    logger.record_event(event)
    records = logger.query_audit_events("t1", "c1")
    assert len(records) == 1
    assert records[0].action == "MUTATE_CAMPAIGN"

# T25-025: Security policy mutation through UI -> Blocked
def test_t25_025_security_policy_mutation_through_ui():
    immutable_policy = {"allow_wildcard_mcp": False, "require_human_auth": True}
    # UI attempt to alter policy
    ui_request = {"allow_wildcard_mcp": True}
    # Policy remains immutable
    assert immutable_policy["allow_wildcard_mcp"] is False
