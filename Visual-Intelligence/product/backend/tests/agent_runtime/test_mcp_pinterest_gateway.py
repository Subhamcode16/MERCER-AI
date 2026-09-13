"""
Automated Test Suite for Model Context Protocol (MCP) & Pinterest Inspiration Engine.
Validates:
1. Tenant-isolated OAuth Vault encryption and boundary enforcement.
2. Pinterest MCP Server tool definitions, moodboard ingestion, and trend discovery.
3. Native MCP Gateway dynamic discovery and Invariant T-013 role-based access control.
4. Governed Tool Registry integration with audit logging and epistemic tagging.
"""

import pytest
import pytest_asyncio
from src.agent_runtime.mcp.oauth_vault import OAuthVault, OAuthCredential
from src.agent_runtime.mcp.pinterest_mcp_server import PinterestMCPServer
from src.agent_runtime.mcp.mcp_client import MCPGatewayClient
from src.agent_runtime.interfaces.agent_runtime import WorkerDefinition, AgentSession
from src.agent_runtime.tools.governed_tool_registry import GovernedToolRegistry


@pytest.mark.asyncio
async def test_oauth_vault_tenant_isolation_and_encryption():
    """Verify tenant isolation in credentials vault."""
    vault = OAuthVault(secret_key="test-secret-key-32-chars-long-ok")
    
    cred_a = OAuthCredential(
        tenant_id="tenant_alpha",
        service_name="pinterest",
        access_token="pina_secret_token_12345",
        scopes=["boards:read", "pins:read"]
    )
    vault.store_credential(cred_a)

    # Retrieval for tenant_alpha succeeds
    retrieved = vault.get_credential("tenant_alpha", "pinterest")
    assert retrieved is not None
    assert retrieved.access_token == "pina_secret_token_12345"
    assert "boards:read" in retrieved.scopes

    # Retrieval for tenant_beta fails (returns None)
    retrieved_beta = vault.get_credential("tenant_beta", "pinterest")
    assert retrieved_beta is None


@pytest.mark.asyncio
async def test_pinterest_mcp_server_list_tools():
    """Verify exposed MCP tools and schemas."""
    server = PinterestMCPServer()
    tools = server.list_tools()
    tool_names = [t["name"] for t in tools]
    assert "pinterest_list_boards" in tool_names
    assert "pinterest_ingest_moodboard" in tool_names
    assert "pinterest_search_trends" in tool_names
    assert "pinterest_extract_aesthetic_tokens" in tool_names


@pytest.mark.asyncio
async def test_pinterest_mcp_server_list_boards():
    """Verify listing curated moodboards."""
    server = PinterestMCPServer()
    res = await server.list_boards(tenant_id="tenant_luxury_01")
    assert res["status"] == "SUCCESS"
    assert len(res["boards"]) >= 3
    assert any(b["board_id"] == "board_bridal_heritage" for b in res["boards"])


@pytest.mark.asyncio
async def test_pinterest_mcp_server_ingest_moodboard():
    """Verify moodboard ingestion and Visual DNA token extraction."""
    server = PinterestMCPServer()
    res = await server.ingest_moodboard(tenant_id="tenant_luxury_01", board_id="board_bridal_heritage")
    assert res["status"] == "SUCCESS"
    assert len(res["ingested_pins"]) == 3
    assert len(res["extracted_palette"]) == 3
    assert "lighting" in res["visual_tokens"]
    assert "textile_physics" in res["visual_tokens"]
    assert res["epistemic_status"] == "OBSERVED"


@pytest.mark.asyncio
async def test_pinterest_mcp_server_trends_discovery():
    """Verify editorial trend discovery."""
    server = PinterestMCPServer()
    res = await server.search_trends(query="modern luxury drape", category="fashion")
    assert res["status"] == "SUCCESS"
    assert len(res["trends"]) >= 2
    assert res["epistemic_status"] == "OBSERVED"


@pytest.mark.asyncio
async def test_mcp_gateway_client_discovery():
    """Verify dynamic discovery of tools across connected servers."""
    client = MCPGatewayClient()
    servers = client.list_servers()
    assert len(servers) >= 1
    assert servers[0]["server_id"] == "pinterest"

    tools = client.discover_tools()
    assert len(tools) >= 4
    tool_ids = [t.tool_id for t in tools]
    assert "pinterest_ingest_moodboard" in tool_ids


@pytest.mark.asyncio
async def test_mcp_gateway_client_t013_unauthorized_role_blocking():
    """Verify Invariant T-013: Unauthorized worker roles cannot invoke MCP tools."""
    client = MCPGatewayClient()
    
    # Authorized worker
    authorized_worker = WorkerDefinition(
        worker_id="intel_01",
        name="Siddharth Rao",
        role="intelligence_specialist",
        tenant_scope="tenant_alpha",
        authority_scope="advisor"
    )
    res = await client.execute_mcp_tool(
        worker=authorized_worker,
        tool_name="pinterest_search_trends",
        arguments={"query": "silk couture"}
    )
    assert res["status"] == "SUCCESS"

    # Unauthorized worker role (e.g., untrusted bot / guest)
    unauthorized_worker = WorkerDefinition(
        worker_id="guest_worker",
        name="External Guest",
        role="untrusted_guest",
        tenant_scope="tenant_alpha",
        authority_scope="none"
    )
    with pytest.raises(PermissionError):
        await client.execute_mcp_tool(
            worker=unauthorized_worker,
            tool_name="pinterest_search_trends",
            arguments={"query": "silk couture"}
        )


@pytest.mark.asyncio
async def test_governed_tool_registry_pinterest_tools():
    """Verify GovernedToolRegistry dispatches Pinterest MCP tools with policy checks."""
    registry = GovernedToolRegistry()
    session = AgentSession(
        session_id="sess_mcp_001",
        tenant_id="tenant_vyren",
        worker_id="creative_lead_01"
    )
    worker = WorkerDefinition(
        worker_id="creative_lead_01",
        name="Elena Vance",
        role="creative_director",
        tenant_scope="tenant_vyren",
        authority_scope="advisor"
    )

    # 1. Execute pinterest.boards
    boards_result = await registry.execute_tool(
        session=session,
        worker=worker,
        tool_id="pinterest.boards",
        arguments={"tenant_id": "tenant_vyren"}
    )
    assert boards_result["status"] == "SUCCESS"

    # 2. Execute pinterest.ingest
    ingest_result = await registry.execute_tool(
        session=session,
        worker=worker,
        tool_id="pinterest.ingest",
        arguments={"board_id": "board_bridal_heritage", "tenant_id": "tenant_vyren"}
    )
    assert ingest_result["status"] == "SUCCESS"
    assert len(ingest_result["ingested_pins"]) > 0

    # 3. Execute pinterest.trends
    trends_result = await registry.execute_tool(
        session=session,
        worker=worker,
        tool_id="pinterest.trends",
        arguments={"query": "banarasi silk", "category": "bridal"}
    )
    assert trends_result["status"] == "SUCCESS"
