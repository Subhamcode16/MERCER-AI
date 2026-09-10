"""
Phase 20 - MCP Capability Policy Enforcer.

Enforces strict allowlisting of declared and approved capabilities.
Rejects wildcard capabilities such as '*', 'admin', or 'full_access'.
"""

from typing import List
from .models import MCPServerRegistration, MCPToolManifest
from .exceptions import MCPCapabilityPolicyViolationError


class MCPCapabilityPolicyValidator:
    """Enforces capability boundaries on MCP server registrations and tool invocations."""

    WILDCARD_PROHIBITIONS = {"*", "admin", "full_access", "all", "root", "superuser"}

    def validate_server_registration(self, registration: MCPServerRegistration) -> None:
        """Reject servers requesting prohibited wildcard or blanket capabilities."""
        for cap in registration.declared_capabilities + registration.approved_capabilities:
            if cap.lower() in self.WILDCARD_PROHIBITIONS or cap.startswith("*"):
                raise MCPCapabilityPolicyViolationError(
                    f"Wildcard capability '{cap}' prohibited for MCP server {registration.server_id}."
                )

    def validate_tool_invocation(self, registration: MCPServerRegistration, tool: MCPToolManifest) -> None:
        """Verify tool required capability is explicitly approved on the server manifest."""
        if tool.required_capability not in registration.approved_capabilities:
            raise MCPCapabilityPolicyViolationError(
                f"Tool '{tool.tool_name}' requires capability '{tool.required_capability}' "
                f"which is not approved for server {registration.server_id}."
            )
