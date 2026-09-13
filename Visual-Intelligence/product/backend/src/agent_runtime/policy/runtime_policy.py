"""
Runtime Execution Policy & Security Invariants.
Validates authority boundaries, detects adversarial inputs, and sanitizes tool outputs.
"""

import re
from typing import Dict, List, Any
from src.agent_runtime.errors.exceptions import (
    TenantTraversalError,
    UnauthorizedToolError,
    AuthorityEscalationError,
    PromptInjectionDetectedError,
    UnverifiedEvidenceError
)
from src.agent_runtime.interfaces.agent_runtime import ToolRegistration, WorkerDefinition, AgentSession


class RuntimePolicyValidator:
    """Enforces fail-closed security policies on agent execution."""

    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s*:\s*you\s+are\s+now",
        r"override\s+security\s+policy",
        r"grant\s+(me\s+)?admin\s+privilege",
        r"bypass\s+governance",
        r"exfiltrate\s+tenant",
        r"self-authorize\s+budget",
        r"<script.*?>",
        r"__import__",
        r"os\.system"
    ]

    @classmethod
    def sanitize_and_check_prompt(cls, prompt: str) -> str:
        """Inspects prompt for prompt-injection attacks."""
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                raise PromptInjectionDetectedError(pattern=pattern)
        return prompt.strip()

    @classmethod
    def validate_tenant_boundary(cls, session: AgentSession, target_tenant_id: str):
        """Strict tenant isolation check."""
        if session.tenant_id != target_tenant_id:
            raise TenantTraversalError(
                message=f"Session tenant '{session.tenant_id}' cannot access target tenant '{target_tenant_id}'.",
                tenant_id=target_tenant_id
            )

    @classmethod
    def validate_tool_access(cls, worker: WorkerDefinition, tool: ToolRegistration):
        """Verifies if worker role and authority allow invoking the tool."""
        if worker.role not in tool.allowed_roles and "all" not in tool.allowed_roles:
            raise UnauthorizedToolError(
                tool_id=tool.tool_id,
                role=worker.role,
                required_authority=tool.required_authority
            )
        
        # Check tenant scope
        if tool.tenant_scope != "global" and tool.tenant_scope != worker.tenant_scope:
            raise TenantTraversalError(
                message=f"Worker tenant '{worker.tenant_scope}' cannot access tool scoped to '{tool.tenant_scope}'.",
                tenant_id=tool.tenant_scope
            )

    @classmethod
    def validate_authority_elevation(cls, worker: WorkerDefinition, proposed_action: str):
        """Prevents worker from executing actions beyond its authority scope."""
        privileged_actions = [
            "commit_budget",
            "publish_to_ad_network",
            "dispatch_to_print",
            "mutate_security_policy",
            "override_human_decision",
            "invalidate_ledger"
        ]
        if proposed_action in privileged_actions and worker.authority_scope != "human_authorized":
            raise AuthorityEscalationError(worker_id=worker.worker_id, action=proposed_action)

    @classmethod
    def validate_tool_output(cls, tool_id: str, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures external data is marked as untrusted and preserves epistemic status."""
        if not isinstance(raw_output, dict):
            return {
                "data": raw_output,
                "epistemic_status": "UNTRUSTED_EXTERNAL",
                "is_verified": False
            }
        
        # Ensure epistemic status is preserved
        status = raw_output.get("epistemic_status", "INFERRED")
        if status not in ["KNOWN", "INFERRED", "USER_CONFIRMED", "UNKNOWN", "CONFLICTED", "OBSERVED", "SUPPORTED"]:
            status = "INFERRED"
            
        return {
            **raw_output,
            "epistemic_status": status,
            "source_type": raw_output.get("source_type", "external_tool"),
            "tool_id": tool_id
        }
