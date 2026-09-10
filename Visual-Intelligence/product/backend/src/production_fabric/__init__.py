"""
Phase 17 ILYREN Creative Studio Production Fabric Package.
Production fabric layer coordinating intake, work queueing, delivery, bounded continuation,
approval orchestration, outcome loops, health monitoring, policy enforcement, and audit ledgers.
"""

from src.production_fabric.exceptions import (
    ProductionFabricError,
    WorkIntakeError,
    ProductionStateViolation,
    ApprovalOrchestrationError,
    ContinuationBoundaryError,
    OutcomeObservationError,
    OperationalRecoveryError,
    FabricPolicyViolation,
    CrossClientFabricViolation,
    StaleProductionStateError,
    ProductionReplayError,
    FabricInvariantViolation,
)

from src.production_fabric.production_models import (
    ProductionState,
    ProductionPriority,
    ProductionRequest,
    ProductionObjective,
    ProductionWorkItem,
    ProductionDependency,
    ProductionCheckpoint,
    ProductionRun,
    ProductionOutcome,
    ProductionHealth,
    ProductionCycle,
)

from src.production_fabric.intake import ProductionIntakeManager
from src.production_fabric.work_queue import ProductionWorkQueue
from src.production_fabric.continuation import BoundedContinuationEngine
from src.production_fabric.delivery import DeliveryCoordinator
from src.production_fabric.approval_orchestrator import ProductionApprovalOrchestrator
from src.production_fabric.outcome_loop import ProductionOutcomeLoop
from src.production_fabric.recovery import ProductionRecoveryEngine
from src.production_fabric.health import ProductionFabricHealthMonitor
from src.production_fabric.observability import ProductionObservabilityStream, ObservabilityEvent
from src.production_fabric.production_policy import ProductionPolicyEngine
from src.production_fabric.autonomy_controller import BoundedAutonomyController
from src.production_fabric.learning_loop import ProductionLearningLoop
from src.production_fabric.optimization import ProductionOptimizationEngine
from src.production_fabric.client_runtime import ClientProductionRuntime
from src.production_fabric.studio_runtime import StudioProductionRuntime
from src.production_fabric.production_ledger import ProductionFabricLedger, ProductionLedgerEntry
from src.production_fabric.orchestrator import ProductionFabricOrchestrator

__all__ = [
    # Exceptions
    "ProductionFabricError",
    "WorkIntakeError",
    "ProductionStateViolation",
    "ApprovalOrchestrationError",
    "ContinuationBoundaryError",
    "OutcomeObservationError",
    "OperationalRecoveryError",
    "FabricPolicyViolation",
    "CrossClientFabricViolation",
    "StaleProductionStateError",
    "ProductionReplayError",
    "FabricInvariantViolation",
    # Models
    "ProductionState",
    "ProductionPriority",
    "ProductionRequest",
    "ProductionObjective",
    "ProductionWorkItem",
    "ProductionDependency",
    "ProductionCheckpoint",
    "ProductionRun",
    "ProductionOutcome",
    "ProductionHealth",
    "ProductionCycle",
    # Engines & Managers
    "ProductionIntakeManager",
    "ProductionWorkQueue",
    "BoundedContinuationEngine",
    "DeliveryCoordinator",
    "ProductionApprovalOrchestrator",
    "ProductionOutcomeLoop",
    "ProductionRecoveryEngine",
    "ProductionFabricHealthMonitor",
    "ProductionObservabilityStream",
    "ObservabilityEvent",
    "ProductionPolicyEngine",
    "BoundedAutonomyController",
    "ProductionLearningLoop",
    "ProductionOptimizationEngine",
    "ClientProductionRuntime",
    "StudioProductionRuntime",
    "ProductionFabricLedger",
    "ProductionLedgerEntry",
    "ProductionFabricOrchestrator",
]
