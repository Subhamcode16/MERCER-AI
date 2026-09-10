"""
Phase 15 ILYREN Creative Studio Operations Package.
Control plane continuity layer managing real client engagements, campaigns, workstreams, deliverables, approvals, outcomes, and operational health.
"""

from src.studio_operations.exceptions import (
    StudioOperationError,
    ClientContextViolation,
    CampaignStateViolation,
    DeliverableStateViolation,
    ApprovalRequiredError,
    ApprovalExpiredError,
    OperationalPolicyViolation,
    ContinuityViolation,
    ScheduleConflictError,
    ProductionReadinessError,
    ExternalOutcomeValidationError,
)

from src.studio_operations.studio_models import (
    OperationalPriority,
    CampaignCadence,
    DeliverableType,
    DeliverableStatus,
    CampaignStatus,
    StudioClient,
    StudioBrand,
    ClientOperatingPolicy,
    Campaign,
    Workstream,
    Deliverable,
    StudioCycle,
    OperationalObjective,
)

from src.studio_operations.client_operations import ClientOperationsManager
from src.studio_operations.campaign_manager import CampaignLifecycleManager
from src.studio_operations.workstream import WorkstreamManager
from src.studio_operations.deliverables import DeliverableManager
from src.studio_operations.approval_queue import ApprovalQueue, ApprovalItem
from src.studio_operations.operational_scheduler import StudioOperationalScheduler, ScheduledTask
from src.studio_operations.continuity_engine import OperationalContinuityEngine, ContinuityActionPlan, ContinuityStep
from src.studio_operations.handoff import HumanHandoffManager, HandoffPackage
from src.studio_operations.outcomes import OutcomeObservationEngine, ExternalOutcomeRecord
from src.studio_operations.performance import StudioPerformanceEngine, StudioPerformanceMetrics
from src.studio_operations.cycle_manager import StudioCycleManager
from src.studio_operations.operational_policy import StudioOperationalPolicyEngine
from src.studio_operations.readiness import ProductionReadinessEngine, ReadinessReport
from src.studio_operations.studio_ledger import StudioOperationsLedger, StudioLedgerEntry
from src.studio_operations.health import StudioHealthMonitor, StudioHealthReport
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

__all__ = [
    # Exceptions
    "StudioOperationError",
    "ClientContextViolation",
    "CampaignStateViolation",
    "DeliverableStateViolation",
    "ApprovalRequiredError",
    "ApprovalExpiredError",
    "OperationalPolicyViolation",
    "ContinuityViolation",
    "ScheduleConflictError",
    "ProductionReadinessError",
    "ExternalOutcomeValidationError",
    # Models
    "OperationalPriority",
    "CampaignCadence",
    "DeliverableType",
    "DeliverableStatus",
    "CampaignStatus",
    "StudioClient",
    "StudioBrand",
    "ClientOperatingPolicy",
    "Campaign",
    "Workstream",
    "Deliverable",
    "StudioCycle",
    "OperationalObjective",
    # Managers & Engines
    "ClientOperationsManager",
    "CampaignLifecycleManager",
    "WorkstreamManager",
    "DeliverableManager",
    "ApprovalQueue",
    "ApprovalItem",
    "StudioOperationalScheduler",
    "ScheduledTask",
    "OperationalContinuityEngine",
    "ContinuityActionPlan",
    "ContinuityStep",
    "HumanHandoffManager",
    "HandoffPackage",
    "OutcomeObservationEngine",
    "ExternalOutcomeRecord",
    "StudioPerformanceEngine",
    "StudioPerformanceMetrics",
    "StudioCycleManager",
    "StudioOperationalPolicyEngine",
    "ProductionReadinessEngine",
    "ReadinessReport",
    "StudioOperationsLedger",
    "StudioLedgerEntry",
    "StudioHealthMonitor",
    "StudioHealthReport",
    "StudioOperationsOrchestrator",
]
