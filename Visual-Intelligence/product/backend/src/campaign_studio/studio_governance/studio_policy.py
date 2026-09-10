"""
Phase 27 Studio Governance, Policy & Invariant Verification Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


class PolicyViolationSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKING = "BLOCKING"


@dataclass
class StudioPolicyEvaluation:
    is_compliant: bool
    policy_name: str
    violations: List[str]
    severity: PolicyViolationSeverity
    invariants_checked: List[str]


class StudioGovernanceEngine:
    """Enforces foundational studio governance policies and phase 27 invariants."""

    INVARIANTS = [
        "Intelligence ≠ Authorization ≠ Execution Authority ≠ Security Policy",
        "Projection ≠ Source of Authority",
        "Natural Language Command ≠ Permission",
        "Attribution ≠ Causal Proof",
        "Visual Similarity ≠ Strategic Correctness",
    ]

    def evaluate_campaign_transition(
        self,
        campaign_status: str,
        target_status: str,
        operator: OperatorContext,
        is_approved: bool = False,
    ) -> StudioPolicyEvaluation:
        violations = []

        # Enforce human authorization for production releases
        if target_status in {"READY_FOR_LAUNCH", "LAUNCHED"}:
            if not is_approved:
                violations.append("Production release requires explicit, signed human approval. Cannot infer approval from state.")
            
            allowed_roles = {OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.SUPER_ADMIN}
            if operator.role not in allowed_roles:
                violations.append(f"Operator role '{operator.role}' lacks execution authority for status '{target_status}'.")

        is_compliant = len(violations) == 0
        severity = PolicyViolationSeverity.BLOCKING if not is_compliant else PolicyViolationSeverity.INFO

        return StudioPolicyEvaluation(
            is_compliant=is_compliant,
            policy_name="StudioReleaseGovernancePolicy",
            violations=violations,
            severity=severity,
            invariants_checked=self.INVARIANTS,
        )

    def evaluate_attribution_assertion(self, claim_text: str) -> StudioPolicyEvaluation:
        """Validates that outcomes claims do not equate correlation with causal proof."""
        violations = []
        lower_claim = claim_text.lower()
        if "proves causality" in lower_claim or "caused 100% of sales" in lower_claim:
            violations.append("Outcome claim violates Invariant: Attribution ≠ Causal Proof. Must classify as correlational attribution.")

        is_compliant = len(violations) == 0
        severity = PolicyViolationSeverity.BLOCKING if not is_compliant else PolicyViolationSeverity.INFO

        return StudioPolicyEvaluation(
            is_compliant=is_compliant,
            policy_name="AttributionIntegrityPolicy",
            violations=violations,
            severity=severity,
            invariants_checked=["Attribution ≠ Causal Proof"],
        )
