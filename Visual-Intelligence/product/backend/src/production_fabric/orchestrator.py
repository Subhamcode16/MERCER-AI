"""
Phase 17 Production Fabric Orchestrator.
Primary facade coordinating production intake, work queueing, bounded continuation,
delivery routing, approval orchestration, outcome ingestion, optimization, and audit logging.
"""

from typing import Dict, Any, List, Optional
from src.production_fabric.exceptions import (
    ProductionFabricError, WorkIntakeError, ContinuationBoundaryError, FabricPolicyViolation
)
from src.production_fabric.production_models import (
    ProductionRequest, ProductionWorkItem, ProductionPriority, ProductionState, ProductionOutcome, ProductionHealth
)
from src.production_fabric.intake import ProductionIntakeManager
from src.production_fabric.work_queue import ProductionWorkQueue
from src.production_fabric.continuation import BoundedContinuationEngine
from src.production_fabric.delivery import DeliveryCoordinator
from src.production_fabric.approval_orchestrator import ProductionApprovalOrchestrator
from src.production_fabric.outcome_loop import ProductionOutcomeLoop
from src.production_fabric.recovery import ProductionRecoveryEngine
from src.production_fabric.health import ProductionFabricHealthMonitor
from src.production_fabric.observability import ProductionObservabilityStream
from src.production_fabric.production_policy import ProductionPolicyEngine
from src.production_fabric.autonomy_controller import BoundedAutonomyController
from src.production_fabric.learning_loop import ProductionLearningLoop
from src.production_fabric.optimization import ProductionOptimizationEngine
from src.production_fabric.studio_runtime import StudioProductionRuntime
from src.production_fabric.production_ledger import ProductionFabricLedger
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

class ProductionFabricOrchestrator:
    """Primary facade coordinating Phase 17 Production Fabric operations."""

    def __init__(
        self,
        studio_orchestrator: Optional[StudioOperationsOrchestrator] = None,
        ledger_dir: str = "data/phase17_production_ledger"
    ):
        self.studio_orchestrator = studio_orchestrator or StudioOperationsOrchestrator()
        self.intake_manager = ProductionIntakeManager()
        self.work_queue = ProductionWorkQueue()
        self.continuation_engine = BoundedContinuationEngine()
        self.delivery_coordinator = DeliveryCoordinator()
        self.approval_orchestrator = ProductionApprovalOrchestrator()
        self.outcome_loop = ProductionOutcomeLoop()
        self.recovery_engine = ProductionRecoveryEngine()
        self.health_monitor = ProductionFabricHealthMonitor()
        self.observability_stream = ProductionObservabilityStream()
        self.policy_engine = ProductionPolicyEngine()
        self.autonomy_controller = BoundedAutonomyController()
        self.learning_loop = ProductionLearningLoop()
        self.optimization_engine = ProductionOptimizationEngine()
        self.studio_runtime = StudioProductionRuntime()
        self.ledger = ProductionFabricLedger(ledger_dir=ledger_dir)

    def submit_production_request(self, request: ProductionRequest) -> ProductionWorkItem:
        """Admits a work request into intake and queue, logging the event to audit ledger."""
        item = self.intake_manager.admit_request(request, self.studio_orchestrator)
        self.work_queue.enqueue(item)

        # Register in client runtime
        client_runtime = self.studio_runtime.get_or_create_client_runtime(request.client_id)
        client_runtime.register_work_item(item)

        # Audit log & Telemetry
        self.ledger.record_entry(
            entry_id=f"entry_{request.request_id}",
            client_id=request.client_id,
            action_type="WORK_ADMITTED",
            item_id=item.item_id,
            payload={"title": request.title, "priority": request.priority.value}
        )
        self.observability_stream.emit_event(
            event_id=f"obs_{request.request_id}",
            event_type="WORK_ADMITTED",
            client_id=request.client_id,
            campaign_id=request.campaign_id,
            item_id=item.item_id,
            payload={"title": request.title}
        )
        return item

    def process_next_work_step(
        self,
        client_id: str,
        requires_approval: bool = False,
        has_valid_approval: bool = False
    ) -> Optional[ProductionWorkItem]:
        """Processes the next step for a work item under bounded continuation rules."""
        item = self.work_queue.dequeue_next_ready(client_id)
        if not item:
            return None

        tier = self.autonomy_controller.get_tier(client_id)
        next_step = self.continuation_engine.evaluate_continuation(
            item=item,
            autonomy_tier=tier,
            requires_approval=requires_approval,
            has_valid_approval=has_valid_approval,
            studio_orchestrator=self.studio_orchestrator
        )

        if next_step == "START_PRODUCTION":
            self.delivery_coordinator.advance_production_stage(item, ProductionState.IN_PRODUCTION, self.studio_orchestrator)
        elif next_step == "SUBMIT_CRITIQUE":
            self.delivery_coordinator.advance_production_stage(item, ProductionState.CRITIQUE, self.studio_orchestrator)
        elif next_step == "SUBMIT_REVIEW":
            self.delivery_coordinator.advance_production_stage(item, ProductionState.REVIEW, self.studio_orchestrator)
        elif next_step == "REQUEST_APPROVAL":
            self.approval_orchestrator.prepare_approval_package(
                item=item,
                approval_id=f"appr_{item.item_id}_{item.retry_count}",
                capability="publish_social_post",
                platform="instagram",
                studio_orchestrator=self.studio_orchestrator
            )
        elif next_step == "MARK_APPROVED":
            item.transition_to(ProductionState.APPROVED)
        elif next_step == "PREPARE_EXECUTION":
            item.transition_to(ProductionState.READY_FOR_EXECUTION)
        elif next_step == "DISPATCH_EXECUTION":
            item.transition_to(ProductionState.EXECUTING)
        elif next_step == "OBSERVE_OUTCOME":
            item.transition_to(ProductionState.OBSERVING)
        elif next_step == "TRIGGER_LEARNING":
            item.transition_to(ProductionState.LEARNING)
        elif next_step == "COMPLETE_RUN":
            item.transition_to(ProductionState.COMPLETED)

        self.ledger.record_entry(
            entry_id=f"entry_{item.item_id}_{item.state.value}",
            client_id=client_id,
            action_type=f"STATE_TRANSITION_{next_step}",
            item_id=item.item_id,
            payload={"state": item.state.value}
        )
        return item

    def record_external_outcome(
        self,
        outcome_id: str,
        client_id: str,
        campaign_id: str,
        deliverable_id: str,
        provider: str,
        external_post_id: str,
        reach: int,
        engagement_rate: float
    ) -> ProductionOutcome:
        """Ingests external platform outcome and logs to audit ledger."""
        outcome = self.outcome_loop.ingest_outcome(
            outcome_id=outcome_id,
            client_id=client_id,
            campaign_id=campaign_id,
            deliverable_id=deliverable_id,
            provider=provider,
            external_post_id=external_post_id,
            reach=reach,
            engagement_rate=engagement_rate,
            studio_orchestrator=self.studio_orchestrator
        )
        self.ledger.record_entry(
            entry_id=f"entry_{outcome_id}",
            client_id=client_id,
            action_type="OUTCOME_INGESTED",
            item_id=deliverable_id,
            payload={"reach": reach, "engagement_rate": engagement_rate, "provenance": outcome.provenance}
        )
        return outcome

    def get_health_status(self) -> ProductionHealth:
        items = self.work_queue.list_queue_status()
        clients = len(self.studio_runtime.list_active_clients())
        return self.health_monitor.evaluate_health(
            active_clients_count=clients,
            active_campaigns_count=clients,
            work_items=items,
            recovery_count=0
        )
