"""
FastAPI Routes for Model Context Protocol (MCP) and Pinterest Inspiration Engine.
"""

from fastapi import APIRouter, HTTPException, Depends, Header, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from src.agent_runtime.mcp.mcp_client import MCPGatewayClient
from src.agent_runtime.mcp.oauth_vault import OAuthVault, OAuthCredential
from src.agent_runtime.mcp.pinterest_mcp_server import PinterestMCPServer


router = APIRouter(prefix="/api/v1/mcp", tags=["Model Context Protocol & External Gateways"])
mcp_client = MCPGatewayClient()
oauth_vault = OAuthVault()
pinterest_server = PinterestMCPServer(oauth_vault=oauth_vault)


class IngestMoodboardRequest(BaseModel):
    board_id: str = "board_bridal_heritage"
    tenant_id: Optional[str] = "tenant_vyren_luxury_01"


class ConnectOAuthRequest(BaseModel):
    service_name: str
    access_token: str
    refresh_token: Optional[str] = None
    scopes: List[str] = Field(default_factory=list)
    tenant_id: Optional[str] = "tenant_vyren_luxury_01"


from src.api.routes.vyren_room_routes import get_tenant_id


@router.get("/servers")
async def list_mcp_servers():
    """List registered and connected MCP servers."""
    return {
        "status": "SUCCESS",
        "servers": mcp_client.list_servers()
    }


@router.get("/tools")
async def list_discovered_mcp_tools():
    """Discover tools exposed across all connected MCP gateways."""
    tools = mcp_client.discover_tools()
    return {
        "status": "SUCCESS",
        "count": len(tools),
        "tools": [t.model_dump() for t in tools]
    }


@router.get("/pinterest/boards")
async def get_pinterest_boards(
    tenant_id: str = Depends(get_tenant_id)
):
    """List moodboards for the specified tenant."""
    return await pinterest_server.list_boards(tenant_id=tenant_id)


@router.post("/pinterest/ingest")
async def ingest_pinterest_moodboard(
    request: IngestMoodboardRequest,
    tenant_id: str = Depends(get_tenant_id)
):
    """Ingest a Pinterest moodboard and extract aesthetic tokens & color palettes."""
    active_tenant = tenant_id if tenant_id != "tenant_default" else (request.tenant_id or "tenant_default")
    return await pinterest_server.ingest_moodboard(tenant_id=active_tenant, board_id=request.board_id)


@router.get("/pinterest/trends")
async def get_pinterest_trends(
    query: str = Query("luxury couture", description="Search query"),
    category: str = Query("fashion", description="Category")
):
    """Discover luxury and fashion editorial trends from Pinterest."""
    return await pinterest_server.search_trends(query=query, category=category)


@router.post("/oauth/connect")
async def connect_oauth_service(
    request: ConnectOAuthRequest,
    tenant_id: str = Depends(get_tenant_id)
):
    """Store encrypted credentials in tenant OAuth vault."""
    active_tenant = tenant_id if tenant_id != "tenant_default" else (request.tenant_id or "tenant_default")
    cred = OAuthCredential(
        tenant_id=active_tenant,
        service_name=request.service_name.lower(),
        access_token=request.access_token,
        refresh_token=request.refresh_token,
        scopes=request.scopes
    )
    oauth_vault.store_credential(cred)
    return {
        "status": "SUCCESS",
        "message": f"Successfully stored encrypted credential for service '{request.service_name}'.",
        "tenant_id": active_tenant,
        "service": request.service_name
    }


@router.get("/oauth/status")
async def get_oauth_status(
    tenant_id: str = Depends(get_tenant_id)
):
    """Check connection status for all creative and social gateways."""
    services = ["pinterest", "instagram", "threads", "x", "meta"]
    status_map = {}
    for s in services:
        cred = oauth_vault.get_credential(tenant_id, s)
        status_map[s] = {
            "connected": bool(cred),
            "scopes": cred.scopes if cred else [],
            "service": s
        }
    return {
        "status": "SUCCESS",
        "tenant_id": tenant_id,
        "gateways": status_map
    }
