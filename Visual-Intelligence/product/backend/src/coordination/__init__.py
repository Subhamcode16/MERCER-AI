"""
Phase 12 Multi-Mission Coordination & Operational Resource Governance Boundary.

Provides multi-mission admission control, shared logical resource arbitration,
cryptographic lease tokens, machine conflict detection, fairness aging, preemption,
deadlock resolution, global capacity budgets, and append-only coordination ledgers.
"""

from .exceptions import (
    CoordinationException,
    MissionAdmissionDenied,
    ResourceUnavailable,
    ResourceConflict,
    ReservationExpired,
    CoordinationDeadlock,
    StarvationDetected,
    CoordinationBudgetExceeded,
    CrossMissionAuthorizationError,
    CoordinationPolicyViolation,
    CoordinationReplayError,
    CheckpointTamperedError,
    LeaseValidationError,
)

from .models import (
    CoordinationMission,
    MissionPriority,
    ResourceDescriptor,
    ResourceRequest,
    ResourceLease,
    ConflictRecord,
    ArbitrationDecision,
    CoordinationBudget,
    CoordinationOutcome,
)

from .mission_registry import MissionRegistry
from .resource_registry import ResourceRegistry
from .resource_manager import ResourceManager
from .arbitration import ArbitrationEngine
from .conflict import ConflictEngine
from .fairness import FairnessEngine
from .leases import LeaseManager
from .capacity import CapacityTracker
from .preemption import PreemptionEngine
from .deadlock import DeadlockDetector
from .coordination_ledger import CoordinationLedger, CoordinationLedgerEntry
from .coordinator import MultiMissionCoordinator

__all__ = [
    "CoordinationException",
    "MissionAdmissionDenied",
    "ResourceUnavailable",
    "ResourceConflict",
    "ReservationExpired",
    "CoordinationDeadlock",
    "StarvationDetected",
    "CoordinationBudgetExceeded",
    "CrossMissionAuthorizationError",
    "CoordinationPolicyViolation",
    "CoordinationReplayError",
    "CheckpointTamperedError",
    "LeaseValidationError",
    "CoordinationMission",
    "MissionPriority",
    "ResourceDescriptor",
    "ResourceRequest",
    "ResourceLease",
    "ConflictRecord",
    "ArbitrationDecision",
    "CoordinationBudget",
    "CoordinationOutcome",
    "MissionRegistry",
    "ResourceRegistry",
    "ResourceManager",
    "ArbitrationEngine",
    "ConflictEngine",
    "FairnessEngine",
    "LeaseManager",
    "CapacityTracker",
    "PreemptionEngine",
    "DeadlockDetector",
    "CoordinationLedger",
    "CoordinationLedgerEntry",
    "MultiMissionCoordinator",
]
