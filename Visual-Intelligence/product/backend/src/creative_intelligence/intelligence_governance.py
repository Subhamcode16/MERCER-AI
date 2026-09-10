"""
Phase 19 - Institutional Intelligence Boundary & Governance Enforcer.

Enforces strict boundary invariants across all intelligence operations:
1. Knowledge != Truth != Authorization != Execution Authority
2. Institutional Intelligence != Security Policy
3. Cross-Client Pattern != Cross-Client Data
4. Workforce Evolution != Privilege Escalation
"""

from typing import Dict, Any, Optional
from .exceptions import (
    AuthorityEscalationError,
    ImmutablePolicyViolationError,
    ClientDataLeakageError
)
from .generalization import ConfidentialityFilter


class IntelligenceGovernanceBoundary:
    """Governance enforcer validating intelligence action boundaries."""

    def __init__(self, filter_engine: Optional[ConfidentialityFilter] = None):
        self.filter = filter_engine or ConfidentialityFilter()

    def audit_intelligence_output(self, payload: Dict[str, Any], is_global: bool = False) -> bool:
        """Audit intelligence payload before emitting or persisting."""
        
        # 1. Enforce No Execution Authority
        if payload.get("execute") is True or "execute_command" in payload:
            raise AuthorityEscalationError(
                "Intelligence output contains execution flags. Knowledge != Execution Authority."
            )

        # 2. Enforce No Security Policy Mutation
        for restricted in ["security_policy", "autonomy_ceiling", "authorization_override", "allowlist_mutation"]:
            if restricted in payload:
                raise ImmutablePolicyViolationError(
                    f"Intelligence output attempts to modify security policy ({restricted})."
                )

        # 3. If global namespace payload, enforce zero client data leakage
        if is_global:
            self.filter.validate_anonymization(payload)

        return True

    def verify_authorization_isolation(self, requesting_action: str) -> None:
        """Verify that intelligence layer is never caller of authorization or execution APIs."""
        blocked_actions = [
            "authorize_execution", "grant_privilege", "mutate_policy",
            "execute_tool", "dispatch_fabric_task", "override_governance"
        ]
        if requesting_action in blocked_actions:
            raise AuthorityEscalationError(
                f"Action '{requesting_action}' prohibited for Creative Intelligence layer."
            )
