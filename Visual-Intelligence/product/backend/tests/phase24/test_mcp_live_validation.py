"""
Tests for Phase 24 MCP Live Contract Validation.
"""
import pytest
from src.live_operations.mcp_smoke import MCPSmokeProbe
from src.live_operations.live_models import ProbeStatus

@pytest.mark.asyncio
async def test_mcp_smoke_probe_valid_tool():
    probe = MCPSmokeProbe()
    res = await probe.execute_probe({"server_id": "render_mcp", "tool_name": "list_services", "scope": "read"})
    assert res.status == ProbeStatus.PASS
    assert res.details["schema_conformant"] is True

@pytest.mark.asyncio
async def test_mcp_smoke_probe_wildcard_rejection():
    probe = MCPSmokeProbe()
    res = await probe.execute_probe({"server_id": "render_mcp", "tool_name": "*", "scope": "*"})
    assert res.status == ProbeStatus.DENIED
    assert "Wildcard/admin" in res.message
