"""
Phase 25 Provider & MCP Control Center Tests.
"""
import pytest
from src.control_plane.models import OperatorRole
from src.control_plane.context import OperatorContext
from src.control_plane.exceptions import UnauthorizedOperatorActionError
from src.provider_control.credential_scope_view import CredentialScopeViewer
from src.provider_control.mcp_provider_view import MCPToolCapabilityView
from src.provider_control.provider_actions import ProviderActionHandler

def test_credential_masking_invariant():
    scopes = CredentialScopeViewer.get_masked_credential_scopes(["Google", "Anthropic", "FalAI"])
    assert len(scopes) == 3
    for s in scopes:
        assert s.masked_fingerprint == "***REDACTED***"
        assert "sk-" not in s.masked_fingerprint

def test_mcp_tool_capability_no_wildcards():
    mcp_view = MCPToolCapabilityView(
        server_id="mcp-trend-01",
        server_name="Trend Intelligence",
        tool_name="get_trend_vectors",
        declared_capabilities=["read:trends:luxury"]
    )
    assert mcp_view.wildcard_permitted is False
    assert "*" not in mcp_view.declared_capabilities

def test_provider_circuit_breaker_governed_reset():
    handler = ProviderActionHandler()
    ctx_sre = OperatorContext(
        operator_id="op-sre-01",
        tenant_id="*",
        client_id="*",
        roles=[OperatorRole.SRE_ENGINEER]
    )

    res = handler.reset_circuit_breaker(ctx_sre, "google_gemini", "Outage resolved by upstream provider")
    assert res["status"] == "RESET_TO_HALF_OPEN"

    # Non-SRE role cannot reset circuit breaker
    ctx_curator = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )
    with pytest.raises(UnauthorizedOperatorActionError):
        handler.reset_circuit_breaker(ctx_curator, "google_gemini", "Unauthorized reset")
