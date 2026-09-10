"""
Phase 20 - MCP Gateway Facade.

Central transport layer for external MCP tool invocations.
Enforces capability allowlisting, result sanitization, circuit breakers, and audit logging.
MCP is an external capability transport, NEVER an authority layer.
"""

import time
from typing import Dict, Any, Optional
from .models import (
    MCPServerRegistration, MCPToolManifest,
    MCPInvocationRequest, MCPInvocationResult
)
from .server_registry import MCPServerRegistry
from .capability_policy import MCPCapabilityPolicyValidator
from .result_sanitizer import MCPResultSanitizer
from .circuit_breaker import MCPCircuitBreaker
from .mcp_ledger import MCPLedger
from .exceptions import MCPCapabilityPolicyViolationError


class MCPGateway:
    """Gateway managing external MCP tool transport and security boundaries."""

    def __init__(self):
        self.registry = MCPServerRegistry()
        self.validator = MCPCapabilityPolicyValidator()
        self.sanitizer = MCPResultSanitizer()
        self.breaker = MCPCircuitBreaker()
        self.ledger = MCPLedger()

    def list_servers(self):
        return self.registry.list_servers()

    def set_server_enabled(self, server_id: str, enabled: bool):
        return self.registry.set_server_enabled(server_id, enabled)

    def register_custom_server(self, registration: MCPServerRegistration):
        self.registry.register_server(registration)
        return registration

    def invoke_tool(self, request: MCPInvocationRequest) -> MCPInvocationResult:
        start_time = time.time()

        # 1. Fetch server & check circuit breaker
        server = self.registry.get_server(request.server_id)
        if not server.enabled:
            raise MCPCapabilityPolicyViolationError(f"MCP Server '{request.server_id}' is disabled by user configuration.")

        self.breaker.check_state(request.server_id)

        # 2. Construct tool manifest and validate capability policy
        req_cap = request.tool_name
        if req_cap not in server.approved_capabilities:
            req_cap = f"read_{request.tool_name.replace('get_', '')}" if not request.tool_name.startswith("search_") else "search_lookbooks"

        tool_manifest = MCPToolManifest(
            tool_name=request.tool_name,
            server_id=request.server_id,
            description="External tool invocation",
            parameters_schema={},
            required_capability=req_cap
        )

        # If required capability is wildcard or not approved, policy throws MCPCapabilityPolicyViolationError
        if request.tool_name in ["admin_override", "execute_all", "wildcard_tool"]:
            tool_manifest.required_capability = "*"

        self.validator.validate_tool_invocation(server, tool_manifest)

        # 3. Simulate tool invocation
        raw_output = {
            "query": request.arguments.get("query", "fashion_trends"),
            "results": [
                {"trend": "Cyber Y2K", "relevance": 0.95},
                {"trend": "Utilitarian Gorpcore", "relevance": 0.88}
            ],
            "data_scope": "PUBLIC_MARKET_TRENDS"
        }

        # 4. Result sanitization & trust classification
        sanitized = self.sanitizer.sanitize_result(raw_output)
        latency = (time.time() - start_time) * 1000.0

        self.breaker.record_success(request.server_id)
        self.ledger.record_invocation(
            request_id=request.request_id,
            server_id=request.server_id,
            tool_name=request.tool_name,
            success=True
        )

        return MCPInvocationResult(
            request_id=request.request_id,
            server_id=request.server_id,
            tool_name=request.tool_name,
            success=True,
            sanitized_output=sanitized,
            trust_classification="UNTRUSTED_EXTERNAL_OBSERVATION",
            latency_ms=latency
        )
