"""
Phase 20 - MCP Server & Tool Registry.

Manages registered MCP servers and their declared/approved capabilities.
"""

from typing import Dict, List, Optional
from .models import MCPServerRegistration
from .capability_policy import MCPCapabilityPolicyValidator
from .exceptions import MCPServerNotFoundError


class MCPServerRegistry:
    """Registry maintaining approved external MCP server manifests."""

    def __init__(self, policy_validator: Optional[MCPCapabilityPolicyValidator] = None):
        self.validator = policy_validator or MCPCapabilityPolicyValidator()
        self._servers: Dict[str, MCPServerRegistration] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        # Register sandbox trend research MCP server
        self.register_server(MCPServerRegistration(
            server_id="mcp_fashion_trends",
            provider="fashion_trends_inc",
            environment="SANDBOX",
            declared_capabilities=["read_fashion_trends", "search_lookbooks"],
            approved_capabilities=["read_fashion_trends", "search_lookbooks"],
            risk_class="LOW"
        ))

    def register_server(self, registration: MCPServerRegistration) -> None:
        self.validator.validate_server_registration(registration)
        self._servers[registration.server_id] = registration

    def get_server(self, server_id: str) -> MCPServerRegistration:
        if server_id not in self._servers:
            raise MCPServerNotFoundError(f"MCP Server '{server_id}' not found in registry.")
        return self._servers[server_id]

    def list_servers(self) -> List[MCPServerRegistration]:
        return list(self._servers.values())

    def set_server_enabled(self, server_id: str, enabled: bool) -> MCPServerRegistration:
        server = self.get_server(server_id)
        server.enabled = enabled
        return server
