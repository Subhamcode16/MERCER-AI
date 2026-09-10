"""
Phase 25 Control Plane Core Tests.
"""
import pytest
import asyncio
from src.control_plane.models import OperatorRole, OperatorCapability
from src.control_plane.context import OperatorContext
from src.control_plane.permissions import PermissionGuard
from src.control_plane.dto import sanitize_payload, CampaignSummaryDTO
from src.control_plane.exceptions import (
    TenantContextMissingError,
    UnauthorizedOperatorActionError,
    TenantAccessDeniedError,
    DTOSerializationError
)
from src.control_plane.event_stream import ControlPlaneEventStreamBus, ControlPlaneEvent
from src.control_plane.service import ControlPlaneService
from src.control_plane.orchestrator import ControlPlaneOrchestrator

def test_operator_context_validation():
    # Valid context
    ctx = OperatorContext(
        operator_id="op-1",
        tenant_id="tenant-alpha",
        client_id="client-alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )
    ctx.validate()

    # Missing operator_id
    invalid_ctx = OperatorContext(
        operator_id="",
        tenant_id="tenant-alpha",
        client_id="client-alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )
    with pytest.raises(TenantContextMissingError):
        invalid_ctx.validate()

def test_permission_guard_enforcement():
    ctx_curator = OperatorContext(
        operator_id="op-curator",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )
    # Permitted
    PermissionGuard.enforce_capability(ctx_curator, OperatorCapability.APPROVE)
    PermissionGuard.enforce_tenant_boundary(ctx_curator, "tenant_atelier", "client_alpha")

    # Unauthorized capability for Curator (e.g. SRE manage circuit breaker)
    with pytest.raises(UnauthorizedOperatorActionError):
        PermissionGuard.enforce_capability(ctx_curator, OperatorCapability.MANAGE_CIRCUIT_BREAKER)

    # Cross-tenant violation
    with pytest.raises(TenantAccessDeniedError):
        PermissionGuard.enforce_tenant_boundary(ctx_curator, "tenant_other", "client_beta")

def test_dto_sanitization_and_secret_blocking():
    safe_data = {"campaign_id": "cmp-1", "title": "Autumn Silk", "score": 0.95}
    sanitized = sanitize_payload(safe_data)
    assert sanitized["title"] == "Autumn Silk"

    # Secret field in payload -> Prohibited
    leaky_data = {"campaign_id": "cmp-1", "api_key": "sk-secret-123456"}
    with pytest.raises(DTOSerializationError):
        sanitize_payload(leaky_data)

    cot_data = {"campaign_id": "cmp-1", "chain_of_thought": "secret reasoning trace"}
    with pytest.raises(DTOSerializationError):
        sanitize_payload(cot_data)

@pytest.mark.asyncio
async def test_event_stream_tenant_isolation():
    bus = ControlPlaneEventStreamBus()
    q_alpha = bus.subscribe("tenant_alpha", "client_alpha")
    q_beta = bus.subscribe("tenant_beta", "client_beta")

    # Publish event for tenant_alpha
    evt = ControlPlaneEvent(
        event_type="CAMPAIGN_UPDATED",
        tenant_id="tenant_alpha",
        client_id="client_alpha",
        payload={"campaign_id": "cmp-alpha-1", "state": "AUTHORIZED"}
    )
    await bus.publish(evt)

    # Alpha receives event
    rec_alpha = await asyncio.wait_for(q_alpha.get(), timeout=1.0)
    assert rec_alpha.event_type == "CAMPAIGN_UPDATED"
    assert rec_alpha.tenant_id == "tenant_alpha"

    # Beta queue remains empty (strict tenant isolation)
    assert q_beta.empty() is True

def test_control_plane_service_and_orchestrator():
    orchestrator = ControlPlaneOrchestrator()
    ctx = OperatorContext(
        operator_id="op-admin",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.STUDIO_ADMIN]
    )
    snapshot = orchestrator.service.get_dashboard_snapshot(ctx, "tenant_atelier", "client_alpha")
    assert snapshot.system_health == "HEALTHY"
    assert snapshot.tenant_id == "tenant_atelier"
    assert snapshot.client_id == "client_alpha"
    assert snapshot.evidence_ledger_intact is True
