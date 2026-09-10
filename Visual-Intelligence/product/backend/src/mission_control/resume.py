"""
Phase 11 Mission Safe Resumption Revalidation Engine.

Implements INV-11-006: 8-Point mandatory revalidation before resuming any paused,
interrupted, or escalated mission. Prevents silent resumption under invalid or revoked states.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Set

from .checkpoint import MissionCheckpoint
from .mission_models import Mission, MissionAuthorizationContext
from .exceptions import ResumptionFailedError, CheckpointTamperedError


@dataclass
class ResumptionResult:
    """Detailed output of the 8-point resumption revalidation check."""
    success: bool
    revalidated_step: int
    failure_reason: Optional[str] = None
    passed_checks: int = 0


class MissionResumeEngine:
    """8-point mandatory resumption revalidation engine."""

    def revalidate_resumption(
        self,
        mission: Mission,
        checkpoint: MissionCheckpoint,
        current_authorization: MissionAuthorizationContext,
        is_revoked: bool = False,
        is_security_halted: bool = False,
        executed_action_nonces: Optional[Set[str]] = None,
        current_time: Optional[datetime] = None
    ) -> ResumptionResult:
        """Executes the 8-point revalidation check prior to resuming a mission."""
        now = current_time or datetime.now(timezone.utc)
        passed_count = 0

        # Check 1: Checkpoint Integrity & Digest Verification
        try:
            checkpoint.verify_integrity()
            passed_count += 1
        except CheckpointTamperedError as e:
            return ResumptionResult(False, checkpoint.step_number, f"Check 1 Failed: {str(e)}", passed_count)

        # Check 2: Mission Policy Version Alignment
        if checkpoint.policy_version != "v1.0":
            return ResumptionResult(False, checkpoint.step_number, "Check 2 Failed: Policy version mismatch.", passed_count)
        passed_count += 1

        # Check 3: Authorization Token Presence & Expiration
        if not current_authorization.is_valid(now):
            return ResumptionResult(False, checkpoint.step_number, "Check 3 Failed: Authorization token expired or missing.", passed_count)
        passed_count += 1

        # Check 4: Authorization Revocation Check
        if is_revoked:
            return ResumptionResult(False, checkpoint.step_number, "Check 4 Failed: Authorization token has been explicitly revoked.", passed_count)
        passed_count += 1

        # Check 5: Capability Scope Verification
        for req_cap in checkpoint.graph_state.get("required_capabilities", []):
            if req_cap not in current_authorization.granted_capabilities and req_cap not in mission.constraints.allowed_capabilities:
                return ResumptionResult(False, checkpoint.step_number, f"Check 5 Failed: Required capability '{req_cap}' not in granted scope.", passed_count)
        passed_count += 1

        # Check 6: Resource Scope Verification
        for req_res in checkpoint.graph_state.get("resource_targets", []):
            if req_res not in current_authorization.granted_resources and req_res not in mission.constraints.allowed_resources:
                return ResumptionResult(False, checkpoint.step_number, f"Check 6 Failed: Target resource '{req_res}' outside authorized resource boundary.", passed_count)
        passed_count += 1

        # Check 7: Action Idempotency & Replay Verification
        nonces = executed_action_nonces or set()
        for action_id in checkpoint.executed_action_ids:
            if action_id in nonces and checkpoint.mission_state == "RUNNING":
                return ResumptionResult(False, checkpoint.step_number, f"Check 7 Failed: Duplicate action nonce detected for '{action_id}'.", passed_count)
        passed_count += 1

        # Check 8: System Security State Verification
        if is_security_halted:
            return ResumptionResult(False, checkpoint.step_number, "Check 8 Failed: Substrate in EMERGENCY_HALT state.", passed_count)
        passed_count += 1

        return ResumptionResult(
            success=True,
            revalidated_step=checkpoint.step_number,
            failure_reason=None,
            passed_checks=passed_count
        )
