"""
Phase 10 — Controlled Operational Execution Layer Package Exports.
"""

from .exceptions import (
    ExecutionControlException,
    SelfAuthorizationAttemptError,
    CapabilityViolationError,
    ResourceScopeViolationError,
    AuthorizationExpiredError,
    AuthorizationRevokedError,
    ReplayExecutionError,
    DryRunSideEffectError,
    AdapterNotFoundError,
    PartialExecutionError,
)
from .capability_models import (
    ExecutionCapability,
    CapabilityRiskLevel,
    CapabilitySpec,
    CAPABILITY_RISK_MAP,
    validate_capability_string,
)
from .resource_scope import ResourceScope
from .action_models import ExecutionAction, PlannedEffect
from .authorization_models import AuthorizationRecord
from .approval import ApprovalState, HumanAuthorizationBoundary
from .dry_run import ExecutionPlan, DryRunEngine
from .adapters import (
    BaseSandboxAdapter,
    AdapterExecutionResult,
    SocialPlatformAdapter,
    AssetStorageAdapter,
    ContentManagementAdapter,
    AnalyticsAdapter,
)
from .execution_policy import ExecutionPolicyEngine
from .idempotency import IdempotencyGuard
from .execution_ledger import ExecutionLedgerRecord, ExecutionLedger
from .executor import ExecutionController

__all__ = [
    "ExecutionControlException",
    "SelfAuthorizationAttemptError",
    "CapabilityViolationError",
    "ResourceScopeViolationError",
    "AuthorizationExpiredError",
    "AuthorizationRevokedError",
    "ReplayExecutionError",
    "DryRunSideEffectError",
    "AdapterNotFoundError",
    "PartialExecutionError",
    "ExecutionCapability",
    "CapabilityRiskLevel",
    "CapabilitySpec",
    "CAPABILITY_RISK_MAP",
    "validate_capability_string",
    "ResourceScope",
    "ExecutionAction",
    "PlannedEffect",
    "AuthorizationRecord",
    "ApprovalState",
    "HumanAuthorizationBoundary",
    "ExecutionPlan",
    "DryRunEngine",
    "BaseSandboxAdapter",
    "AdapterExecutionResult",
    "SocialPlatformAdapter",
    "AssetStorageAdapter",
    "ContentManagementAdapter",
    "AnalyticsAdapter",
    "ExecutionPolicyEngine",
    "IdempotencyGuard",
    "ExecutionLedgerRecord",
    "ExecutionLedger",
    "ExecutionController",
]
