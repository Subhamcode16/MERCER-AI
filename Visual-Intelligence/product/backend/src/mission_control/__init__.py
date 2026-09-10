"""
Phase 11 Mission Control & Operational Autonomy Layer.

Provides long-running mission orchestration, bounded autonomy policies,
scheduling, SHA-256 HMAC checkpoints, 8-point safe resumption, bounded retries,
structured escalations, resource budgets, and append-only operational ledgers.
"""

from .exceptions import (
    MissionControlError,
    InvalidMissionStateError,
    InvalidMissionGraphError,
    MissionPolicyViolationError,
    MissionBudgetExceededError,
    AuthorizationRequiredError,
    CheckpointError,
    CheckpointTamperedError,
    ResumptionFailedError,
    RetryExhaustedError,
    MissionCancelledError,
    SecurityBoundaryViolation,
)

from .mission_models import (
    Mission,
    MissionObjective,
    MissionConstraints,
    MissionBudget,
    MissionAuthorizationContext,
    MissionOutcome,
)

from .mission_state import MissionState, MissionStateMachine
from .mission_graph import MissionGraph, MissionTaskNode
from .scheduler import MissionScheduler, ScheduleMode, ScheduledItem
from .checkpoint import CheckpointManager, MissionCheckpoint
from .resume import MissionResumeEngine, ResumptionResult
from .retry_policy import RetryPolicy, BackoffStrategy
from .escalation import EscalationManager, EscalationReason, EscalationTicket
from .budget import MissionBudgetTracker, BudgetUsage
from .autonomy_policy import AutonomyPolicyEngine, AutonomyTier, AutonomyClass
from .operational_events import OperationalEvent, OperationalEventType
from .mission_ledger import MissionLedger, LedgerEntry
from .cancellation import MissionCancellationManager, CancellationReason, CancellationRecord
from .coordinator import MissionCoordinator

__all__ = [
    "MissionControlError",
    "InvalidMissionStateError",
    "InvalidMissionGraphError",
    "MissionPolicyViolationError",
    "MissionBudgetExceededError",
    "AuthorizationRequiredError",
    "CheckpointError",
    "CheckpointTamperedError",
    "ResumptionFailedError",
    "RetryExhaustedError",
    "MissionCancelledError",
    "SecurityBoundaryViolation",
    "Mission",
    "MissionObjective",
    "MissionConstraints",
    "MissionBudget",
    "MissionAuthorizationContext",
    "MissionOutcome",
    "MissionState",
    "MissionStateMachine",
    "MissionGraph",
    "MissionTaskNode",
    "MissionScheduler",
    "ScheduleMode",
    "ScheduledItem",
    "CheckpointManager",
    "MissionCheckpoint",
    "MissionResumeEngine",
    "ResumptionResult",
    "RetryPolicy",
    "BackoffStrategy",
    "EscalationManager",
    "EscalationReason",
    "EscalationTicket",
    "MissionBudgetTracker",
    "BudgetUsage",
    "AutonomyPolicyEngine",
    "AutonomyTier",
    "AutonomyClass",
    "OperationalEvent",
    "OperationalEventType",
    "MissionLedger",
    "LedgerEntry",
    "MissionCancellationManager",
    "CancellationReason",
    "CancellationRecord",
    "MissionCoordinator",
]
