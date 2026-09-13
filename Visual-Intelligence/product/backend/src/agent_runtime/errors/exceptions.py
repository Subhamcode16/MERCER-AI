"""
Structured exception hierarchy for Agent Runtime Subsystem.
Strict fail-closed error handling according to VYREN security invariants.
"""

class AgentRuntimeError(Exception):
    """Base exception for all agent runtime errors."""
    def __init__(self, message: str, error_code: str = "AGENT_RUNTIME_ERROR", details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class TenantTraversalError(AgentRuntimeError):
    """Attempted cross-tenant data or session access."""
    def __init__(self, message: str = "Cross-tenant access strictly forbidden.", tenant_id: str = None):
        super().__init__(message, error_code="TENANT_TRAVERSAL_BLOCKED", details={"tenant_id": tenant_id})


class UnauthorizedToolError(AgentRuntimeError):
    """Worker attempted to invoke a tool without permitted authority or role binding."""
    def __init__(self, tool_id: str, role: str, required_authority: str):
        super().__init__(
            f"Tool '{tool_id}' denied for role '{role}'. Requires authority '{required_authority}'.",
            error_code="UNAUTHORIZED_TOOL_INVOCATION",
            details={"tool_id": tool_id, "role": role, "required_authority": required_authority}
        )


class AuthorityEscalationError(AgentRuntimeError):
    """Worker attempted to escalate privileges or self-authorize actions."""
    def __init__(self, worker_id: str, action: str):
        super().__init__(
            f"Authority escalation attempt detected for worker '{worker_id}' performing action '{action}'.",
            error_code="AUTHORITY_ESCALATION_BLOCKED",
            details={"worker_id": worker_id, "action": action}
        )


class PromptInjectionDetectedError(AgentRuntimeError):
    """Adversarial prompt or instruction injection detected in input stream."""
    def __init__(self, pattern: str = "Suspicious pattern"):
        super().__init__(
            f"Adversarial prompt injection pattern detected: {pattern}",
            error_code="PROMPT_INJECTION_NEUTRALIZED",
            details={"pattern": pattern}
        )


class UnverifiedEvidenceError(AgentRuntimeError):
    """Tool returned ungrounded or fabricated evidence violating epistemic status."""
    def __init__(self, evidence_id: str, reason: str):
        super().__init__(
            f"Evidence '{evidence_id}' rejected: {reason}",
            error_code="UNVERIFIED_EVIDENCE_REJECTED",
            details={"evidence_id": evidence_id, "reason": reason}
        )


class StaleSessionReplayError(AgentRuntimeError):
    """Attempted to replay a revoked or expired runtime session."""
    def __init__(self, session_id: str):
        super().__init__(
            f"Runtime session '{session_id}' is expired or revoked. Replay denied.",
            error_code="STALE_SESSION_REPLAY_DENIED",
            details={"session_id": session_id}
        )
