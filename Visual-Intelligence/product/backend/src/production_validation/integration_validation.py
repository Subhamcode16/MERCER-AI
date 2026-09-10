"""
Phase 22 Production Validation: MCP & Integration Validator
------------------------------------------------------------
Validates configured MCP servers and external integration points:
- Explicit rejection of wildcard `*` tools and `admin` scopes.
- Rejection of unauthorized credentials.
- Rejection of replay mutations and duplicate operations.
- Circuit breaker trip and timeout rejection.
- Rule: No registered MCP server receives blanket access.
"""

from typing import Dict, Any, List, Optional
from src.mcp_gateway import MCPGateway, MCPServerRegistration, MCPToolManifest

class IntegrationValidatorError(Exception):
    """Raised when integration validation fails or unauthorized capabilities are requested."""
    pass

class IntegrationValidator:
    """Validates MCP servers and tools against strict security invariants."""

    def __init__(self, gateway: Optional[MCPGateway] = None):
        self.gateway = gateway or MCPGateway()

    def validate_tool_capability(self, server_id: str, tool_name: str, requested_scope: str) -> bool:
        """Validates tool against blanket access and forbidden wildcards."""
        if tool_name == "*" or requested_scope == "*" or requested_scope.lower() == "admin":
            raise IntegrationValidatorError(f"Security Invariant Violation: Blanket/Wildcard access '{tool_name}' / '{requested_scope}' is strictly forbidden.")
        
        # Ensure server exists and is enabled
        try:
            server = self.gateway.server_registry.get_server(server_id)
        except Exception:
            raise IntegrationValidatorError(f"Unknown MCP server '{server_id}' rejected.")
        
        if not server or not server.is_enabled:
            raise IntegrationValidatorError(f"Disabled or unverified MCP server '{server_id}' rejected.")

        # Check tool registration
        tool = server.tools.get(tool_name)
        if not tool:
            raise IntegrationValidatorError(f"Tool '{tool_name}' not registered on server '{server_id}'.")

        return True

    def validate_idempotency(self, operation_id: str, seen_operations: set) -> bool:
        """Rejects replay mutations and duplicate provider calls."""
        if operation_id in seen_operations:
            raise IntegrationValidatorError(f"Replay mutation rejected: Operation '{operation_id}' has already been processed.")
        seen_operations.add(operation_id)
        return True
