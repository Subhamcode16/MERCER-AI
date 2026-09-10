"""
Phase 10 — Capability Models & Risk Allowlist

Defines explicit, fine-grained operational capabilities and enforces zero-trust prohibitions
against generic administrative, bypass, or self-authorization capability strings.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set

from src.execution_control.exceptions import CapabilityViolationError


class ExecutionCapability(str, Enum):
    """Explicit Allowlist of 8 Fine-Grained Operational Capabilities."""

    CREATE_DRAFT = "CREATE_DRAFT"
    EDIT_DRAFT = "EDIT_DRAFT"
    GENERATE_ASSET = "GENERATE_ASSET"
    READ_ANALYTICS = "READ_ANALYTICS"
    SCHEDULE_CONTENT = "SCHEDULE_CONTENT"
    PUBLISH_CONTENT = "PUBLISH_CONTENT"
    DELETE_CONTENT = "DELETE_CONTENT"
    MODIFY_BRAND_ASSETS = "MODIFY_BRAND_ASSETS"


class CapabilityRiskLevel(str, Enum):
    READ_ONLY = "READ_ONLY"
    LOW_RISK = "LOW_RISK"
    MEDIUM_RISK = "MEDIUM_RISK"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL = "CRITICAL"


# Capability Risk Mapping
CAPABILITY_RISK_MAP: Dict[ExecutionCapability, CapabilityRiskLevel] = {
    ExecutionCapability.READ_ANALYTICS: CapabilityRiskLevel.READ_ONLY,
    ExecutionCapability.CREATE_DRAFT: CapabilityRiskLevel.LOW_RISK,
    ExecutionCapability.EDIT_DRAFT: CapabilityRiskLevel.LOW_RISK,
    ExecutionCapability.GENERATE_ASSET: CapabilityRiskLevel.LOW_RISK,
    ExecutionCapability.SCHEDULE_CONTENT: CapabilityRiskLevel.MEDIUM_RISK,
    ExecutionCapability.PUBLISH_CONTENT: CapabilityRiskLevel.HIGH_RISK,
    ExecutionCapability.MODIFY_BRAND_ASSETS: CapabilityRiskLevel.HIGH_RISK,
    ExecutionCapability.DELETE_CONTENT: CapabilityRiskLevel.CRITICAL,
}

# Forbidden Capability Keywords (Must NEVER be allowed or parsed)
FORBIDDEN_CAPABILITY_PATTERNS: Set[str] = {
    "ALLOW_ALL",
    "ADMIN_EXECUTE",
    "BYPASS_SECURITY",
    "AUTHORIZE",
    "UNLOCK_GATE",
    "ROOT_ACCESS",
    "SUPERUSER",
    "ALL_PERMISSIONS",
}


@dataclass(frozen=True)
class CapabilitySpec:
    """Immutable Specification for an Executable Capability."""

    capability: ExecutionCapability
    description: str
    requires_human_authorization: bool
    requires_dry_run: bool

    def __post_init__(self):
        if not isinstance(self.capability, ExecutionCapability):
            raise CapabilityViolationError(f"Invalid capability: {self.capability}")


def validate_capability_string(cap_str: str) -> ExecutionCapability:
    """Parses and validates a capability string against the explicit allowlist and forbidden patterns."""
    if not cap_str or not isinstance(cap_str, str):
        raise CapabilityViolationError("Capability must be a non-empty string.")

    upper_cap = cap_str.strip().upper()

    if any(forbidden in upper_cap for forbidden in FORBIDDEN_CAPABILITY_PATTERNS):
        raise CapabilityViolationError(
            f"Forbidden administrative or bypass capability requested: '{cap_str}'"
        )

    try:
        return ExecutionCapability(upper_cap)
    except ValueError:
        raise CapabilityViolationError(
            f"Capability '{cap_str}' is not in the explicit Phase 10 ExecutionCapability allowlist."
        )
