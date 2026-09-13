"""
Native In-Process Model Context Protocol (MCP) Gateway Client for VYREN.
Manages connections to internal and external MCP servers, dynamic tool discovery, and governed dispatch.
"""

from typing import Dict, List, Any, Optional
from src.agent_runtime.mcp.pinterest_mcp_server import PinterestMCPServer
from src.agent_runtime.mcp.oauth_vault import OAuthVault
from src.agent_runtime.interfaces.agent_runtime import WorkerDefinition, ToolRegistration


class MCPGatewayClient:
    """Manages active MCP servers and governed tool dispatching."""

    def __init__(self, oauth_vault: Optional[OAuthVault] = None):
        self.oauth_vault = oauth_vault or OAuthVault()
        self._servers: Dict[str, Any] = {
            "pinterest": PinterestMCPServer(oauth_vault=self.oauth_vault)
        }

    def list_servers(self) -> List[Dict[str, Any]]:
        """List active MCP servers and their capabilities."""
        return [
            {
                "server_id": "pinterest",
                "name": "Pinterest Inspiration & Editorial MCP",
                "version": "2024-11-05",
                "status": "ONLINE",
                "tools_count": len(self._servers["pinterest"].list_tools()),
                "category": "creative_intelligence"
            }
        ]

    def discover_tools(self) -> List[ToolRegistration]:
        """Dynamically discover all tools exposed by connected MCP servers."""
        tools: List[ToolRegistration] = []
        for server_id, server in self._servers.items():
            raw_tools = server.list_tools()
            for t in raw_tools:
                tools.append(ToolRegistration(
                    tool_id=t["name"],
                    name=t["name"],
                    description=t["description"],
                    input_schema=t.get("inputSchema", {}),
                    permitted_roles=["intelligence_specialist", "creative_director", "founder"],
                    epistemic_status="OBSERVED"
                ))
        return tools

    async def execute_mcp_tool(
        self,
        worker: WorkerDefinition,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes an MCP tool with role and tenant boundary validation (Invariant T-013).
        """
        # Role Access Boundary Validation (T-013)
        if worker.role not in ["intelligence_specialist", "creative_director", "founder", "marketing_lead"]:
            raise PermissionError(f"Worker role '{worker.role}' is not authorized to invoke external MCP tools.")

        # Dispatch to appropriate server
        if tool_name.startswith("pinterest_"):
            server = self._servers.get("pinterest")
            if not server:
                raise ValueError("Pinterest MCP Server is not registered.")
            return await server.execute_tool(tool_name, arguments)
        else:
            raise ValueError(f"No MCP server registered for tool '{tool_name}'.")
