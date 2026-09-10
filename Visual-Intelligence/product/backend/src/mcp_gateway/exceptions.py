"""
Phase 20 - MCP Gateway Exceptions.

Defines custom exception hierarchy for Model Context Protocol (MCP) server & tool operations.
"""


class MCPGatewayError(Exception):
    """Base exception for all Phase 20 MCP Gateway errors."""
    pass


class MCPServerNotFoundError(MCPGatewayError):
    """Raised when an requested MCP server is not registered or supported."""
    pass


class MCPToolNotFoundError(MCPGatewayError):
    """Raised when an requested MCP tool is not found in server manifest."""
    pass


class MCPCapabilityPolicyViolationError(MCPGatewayError):
    """Raised when an MCP tool invocation requests unauthorized capabilities or wildcards."""
    pass


class MCPCredentialLeakageError(MCPGatewayError):
    """Raised when credentials or sensitive tokens leak into MCP tool payloads or outputs."""
    pass


class MCPCircuitBreakerOpenError(MCPGatewayError):
    """Raised when MCP circuit breaker is open due to prior service failures."""
    pass


class MCPRateLimitExceededError(MCPGatewayError):
    """Raised when tool invocation frequency exceeds allowed rate limits."""
    pass


class MCPEnvironmentViolationError(MCPGatewayError):
    """Raised when an MCP tool is invoked in an unauthorized environment (e.g. prod mutation in dev)."""
    pass
