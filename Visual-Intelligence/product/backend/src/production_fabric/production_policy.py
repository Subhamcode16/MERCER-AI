"""
Phase 17 Production Policy Engine.
Enforces strict separation between Security Policy (Immutable), Operational Strategy (Adaptable),
and Creative Preference (Adaptable). Enforces INV-17-004 & INV-17-007.
"""

from typing import Dict, Any, List, Set
from src.production_fabric.exceptions import FabricPolicyViolation

IMMUTABLE_SECURITY_POLICIES: Set[str] = {
    "authorization_origin",
    "security_policy",
    "capability_allowlists",
    "credential_access_rules",
    "client_isolation_rules",
    "execution_boundaries",
    "trust_classification_rules",
    "audit_requirements",
    "mandatory_approval_requirements",
    "cryptographic_verification"
}

ADAPTABLE_OPERATIONAL_STRATEGIES: Set[str] = {
    "task_ordering",
    "workforce_allocation",
    "revision_strategy",
    "creative_workflow",
    "research_prioritization",
    "content_cadence",
    "trend_weighting",
    "operational_scheduling",
    "resource_efficiency",
    "prompt_templates",
    "benchmark_targets"
}

class ProductionPolicyEngine:
    """Policy engine rejecting any attempt to mutate immutable security policies via learning or operational loops."""

    def validate_policy_mutation(self, target_policy_key: str, proposed_value: Any) -> bool:
        """Checks whether a policy key is adaptable or immutable."""
        if target_policy_key in IMMUTABLE_SECURITY_POLICIES:
            raise FabricPolicyViolation(
                f"Policy key '{target_policy_key}' belongs to the Immutable Security Plane and CANNOT be mutated."
            )
        if target_policy_key not in ADAPTABLE_OPERATIONAL_STRATEGIES:
            raise FabricPolicyViolation(
                f"Unknown or unapproved policy key '{target_policy_key}' cannot be mutated."
            )
        return True
