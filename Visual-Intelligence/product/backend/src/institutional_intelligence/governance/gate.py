"""
Governance Invariant Policy Engine (Phase 30).
Enforces non-negotiable institutional invariants and fail-closed security gates across all 35 threats.
"""
from typing import Dict, Any, Optional, List
from ..types import ThreatID, GovernanceInvariantViolation, StrategicHorizon


class GovernancePolicyGate:
    """
    Central gate for validating non-negotiable invariants before state transitions.
    """

    @classmethod
    def verify_no_ai_self_authorization(cls, actor_type: str, action: str):
        if actor_type.upper() in ["AI_AGENT", "MODEL", "CRON_WORKER", "AUTONOMOUS_JOB"]:
            raise GovernanceInvariantViolation(
                ThreatID.T30_002,
                f"AI/automated actor of type '{actor_type}' cannot grant itself execution or decision authority for '{action}'.",
                {"actor_type": actor_type, "action": action}
            )

    @classmethod
    def verify_budget_separation(cls, is_budget_action: bool, has_financial_authority: bool):
        if is_budget_action and not has_financial_authority:
            raise GovernanceInvariantViolation(
                ThreatID.T30_005,
                "Strategic prioritization or ranking cannot be confused with financial/compute budget authorization.",
                {}
            )

    @classmethod
    def verify_unknown_state_preservation(cls, original_state: str, new_state: str, is_automated: bool):
        if is_automated and original_state == "UNKNOWN" and new_state != "UNKNOWN":
            raise GovernanceInvariantViolation(
                ThreatID.T30_012,
                "Automated processes cannot collapse an UNKNOWN state into false certainty.",
                {"original": original_state, "new": new_state}
            )

    @classmethod
    def verify_feedback_loop_damping(cls, consecutive_self_reinforcements: int, max_allowed: int = 3):
        # T30-028 / T30-029: Feedback-loop & confirmation-bias amplification defense
        if consecutive_self_reinforcements > max_allowed:
            raise GovernanceInvariantViolation(
                ThreatID.T30_028,
                f"Feedback loop amplification detected: {consecutive_self_reinforcements} consecutive model inferences without empirical grounding.",
                {"count": consecutive_self_reinforcements}
            )

    @classmethod
    def verify_recovery_authority_bounds(cls, is_failover: bool, requested_role: str):
        # T30-035: Recovery-authority escalation prevention
        if is_failover and requested_role in ["SUPER_ADMIN", "INSTITUTIONAL_OWNER"]:
            raise GovernanceInvariantViolation(
                ThreatID.T30_035,
                f"Failover / recovery mode cannot grant elevated role '{requested_role}'.",
                {"requested_role": requested_role}
            )
