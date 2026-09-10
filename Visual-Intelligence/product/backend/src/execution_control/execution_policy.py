"""
Phase 10 — Execution Policy Engine

Centralizes operational execution policies (capability risk assessment, dry-run requirements,
human authorization checks, resource boundary enforcement).
Immutable from Phase 9 learning.
"""

from dataclasses import dataclass
from typing import List, Optional

from src.execution_control.action_models import ExecutionAction
from src.execution_control.capability_models import (
    CAPABILITY_RISK_MAP,
    CapabilityRiskLevel,
    ExecutionCapability,
)
from src.execution_control.exceptions import CapabilityViolationError, ResourceScopeViolationError


class ExecutionPolicyEngine:
    """Central policy engine governing execution eligibility and authorization rules."""

    def __init__(self):
        pass

    def get_capability_risk(self, capability: ExecutionCapability) -> CapabilityRiskLevel:
        """Returns risk level for a capability."""
        return CAPABILITY_RISK_MAP.get(capability, CapabilityRiskLevel.HIGH_RISK)

    def requires_human_authorization(self, capability: ExecutionCapability) -> bool:
        """Determines if a capability requires explicit human authorization."""
        risk = self.get_capability_risk(capability)
        # Medium, High, and Critical risk capabilities require explicit human authorization
        return risk in [
            CapabilityRiskLevel.MEDIUM_RISK,
            CapabilityRiskLevel.HIGH_RISK,
            CapabilityRiskLevel.CRITICAL,
        ]

    def requires_dry_run(self, capability: ExecutionCapability) -> bool:
        """Determines if a capability requires prior dry-run simulation."""
        risk = self.get_capability_risk(capability)
        return risk in [
            CapabilityRiskLevel.LOW_RISK,
            CapabilityRiskLevel.MEDIUM_RISK,
            CapabilityRiskLevel.HIGH_RISK,
            CapabilityRiskLevel.CRITICAL,
        ]

    def validate_action_policy(self, action: ExecutionAction) -> None:
        """Validates that action complies with core execution policy."""
        if not action.capability:
            raise CapabilityViolationError("Action missing required capability.")
        if not action.resource_scope:
            raise ResourceScopeViolationError("Action missing required resource scope.")
