"""
Phase 11 Operational Autonomy Policy Engine.

Enforces Tiers 0-3 operational autonomy and validates that side-effecting
AUTHORIZED_EXECUTION operations require explicit Phase 10 authorization.
"""

from enum import Enum
from typing import Set

from .exceptions import SecurityBoundaryViolation, AuthorizationRequiredError
from .mission_models import MissionConstraints, MissionAuthorizationContext


class AutonomyTier(Enum):
    """Operational autonomy Tiers 0 through 3."""
    TIER_0_ADVISORY = "TIER_0_ADVISORY"
    TIER_1_BOUNDED_AUTONOMOUS_WORK = "TIER_1_BOUNDED_AUTONOMOUS_WORK"
    TIER_2_PRE_AUTHORIZED_BOUNDED_EXECUTION = "TIER_2_PRE_AUTHORIZED_BOUNDED_EXECUTION"
    TIER_3_HUMAN_ESCALATION = "TIER_3_HUMAN_ESCALATION"


class AutonomyClass(Enum):
    """Classes of mission tasks."""
    AUTONOMOUS_RESEARCH = "AUTONOMOUS_RESEARCH"
    AUTONOMOUS_ANALYSIS = "AUTONOMOUS_ANALYSIS"
    AUTONOMOUS_DRAFTING = "AUTONOMOUS_DRAFTING"
    AUTONOMOUS_REVISION = "AUTONOMOUS_REVISION"
    AUTONOMOUS_CRITIQUE = "AUTONOMOUS_CRITIQUE"
    AUTONOMOUS_REVIEW = "AUTONOMOUS_REVIEW"
    AUTHORIZED_EXECUTION = "AUTHORIZED_EXECUTION"


# Standard autonomous read-only work classes
AUTONOMOUS_WORK_CLASSES: Set[AutonomyClass] = {
    AutonomyClass.AUTONOMOUS_RESEARCH,
    AutonomyClass.AUTONOMOUS_ANALYSIS,
    AutonomyClass.AUTONOMOUS_DRAFTING,
    AutonomyClass.AUTONOMOUS_REVISION,
    AutonomyClass.AUTONOMOUS_CRITIQUE,
    AutonomyClass.AUTONOMOUS_REVIEW,
}


class AutonomyPolicyEngine:
    """Enforces boundaries on autonomous work vs side-effect execution."""

    @staticmethod
    def is_autonomous_allowed(task_class: AutonomyClass) -> bool:
        """Returns True if task_class is permitted to execute autonomously without external authorization."""
        return task_class in AUTONOMOUS_WORK_CLASSES

    @staticmethod
    def validate_execution_request(
        task_class: AutonomyClass,
        requested_capability: str,
        requested_resource: str,
        constraints: MissionConstraints,
        auth_context: MissionAuthorizationContext
    ) -> None:
        """Enforces capability, resource, and authorization boundaries for execution requests."""
        if task_class == AutonomyClass.AUTHORIZED_EXECUTION:
            # 1. Check authorization token presence & validity
            if not auth_context.is_valid():
                raise AuthorizationRequiredError(
                    f"Execution of capability '{requested_capability}' on resource '{requested_resource}' requires valid external authorization."
                )

            # 2. Check granted capability scope
            if (requested_capability not in auth_context.granted_capabilities and
                    requested_capability not in constraints.allowed_capabilities):
                raise SecurityBoundaryViolation(
                    f"Capability '{requested_capability}' is outside permitted capability scope."
                )

            # 3. Check granted resource scope
            if (requested_resource not in auth_context.granted_resources and
                    requested_resource not in constraints.allowed_resources):
                raise SecurityBoundaryViolation(
                    f"Resource '{requested_resource}' is outside permitted resource scope."
                )

        elif task_class in AUTONOMOUS_WORK_CLASSES:
            # Autonomous work cannot execute side effects or attempt privilege elevation
            if requested_capability.startswith("EXECUTE_") or requested_capability.startswith("CREATE_DRAFT_EXTERNAL"):
                raise SecurityBoundaryViolation(
                    f"Autonomous work class {task_class.value} attempted privilege elevation for '{requested_capability}'."
                )
