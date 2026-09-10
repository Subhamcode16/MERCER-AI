"""
Phase 28 Learning Governance & Policy Guardrails Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


class LearningPolicySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKING = "BLOCKING"


@dataclass
class LearningPolicyEvaluation:
    is_compliant: bool
    policy_name: str
    violations: List[str]
    severity: LearningPolicySeverity
    invariants_checked: List[str]


class LearningGovernanceEngine:
    """Enforces foundational learning governance policies and mathematical invariants."""

    INVARIANTS = [
        "Outcome ≠ Causation",
        "Correlation ≠ Causal Proof",
        "Learning ≠ Policy Mutation",
        "Learning ≠ Authority",
        "Performance ≠ Truth",
        "Failure ≠ Universal Invalidity",
        "Evidence ≠ Interpretation",
        "Historical Record ≠ Current Recommendation",
        "Optimization ≠ Self-Authorization",
        "Model Confidence ≠ Empirical Confidence",
        "Institutional Learning ≠ Cross-Client Leakage",
        "Unknown Must Survive",
    ]

    def evaluate_learning_claim(self, claim_text: str) -> LearningPolicyEvaluation:
        violations = []
        lower = claim_text.lower()

        # Check for ungrounded causal assertions
        if "proves causality" in lower or "caused 100% of sales" in lower or "guarantees success" in lower:
            violations.append("Claim violates Invariant: Correlation ≠ Causal Proof. Must qualify causal status.")

        # Check for absolute universal claims without scope
        if "universally true for all clients" in lower or "applies to all brands globally without exception" in lower:
            violations.append("Claim violates Invariant: Performance ≠ Truth. Scope must be bounded.")

        is_compliant = len(violations) == 0
        severity = LearningPolicySeverity.BLOCKING if not is_compliant else LearningPolicySeverity.INFO

        return LearningPolicyEvaluation(
            is_compliant=is_compliant,
            policy_name="CausalIntegrityPolicy",
            violations=violations,
            severity=severity,
            invariants_checked=["Correlation ≠ Causal Proof", "Performance ≠ Truth"],
        )

    def evaluate_policy_mutation_attempt(self, operator: OperatorContext, proposed_action: str) -> LearningPolicyEvaluation:
        violations = []
        lower = proposed_action.lower()

        if "modify security policy" in lower or "grant admin role" in lower or "bypass rbac" in lower:
            violations.append("Action violates Invariant: Learning ≠ Policy Mutation / Learning ≠ Authority.")

        allowed_roles = {OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.STUDIO_ADMIN, OperatorRole.SUPER_ADMIN}
        if operator.role not in allowed_roles:
            violations.append(f"Operator role '{operator.role}' lacks execution authority for governed knowledge updates.")

        is_compliant = len(violations) == 0
        severity = LearningPolicySeverity.BLOCKING if not is_compliant else LearningPolicySeverity.INFO

        return LearningPolicyEvaluation(
            is_compliant=is_compliant,
            policy_name="AuthorityBoundaryPolicy",
            violations=violations,
            severity=severity,
            invariants_checked=["Learning ≠ Policy Mutation", "Learning ≠ Authority", "Optimization ≠ Self-Authorization"],
        )
