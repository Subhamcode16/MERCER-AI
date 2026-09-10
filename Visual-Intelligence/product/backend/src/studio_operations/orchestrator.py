"""
Phase 15 Studio Operations Orchestrator.
Main entry-point facade coordinating client lifecycle, campaigns, workstreams, creative workforce (Phase 14), deliverables, approvals, outcomes, and performance.
"""

from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import ClientContextViolation, StudioOperationError
from src.studio_operations.client_operations import ClientOperationsManager
from src.studio_operations.campaign_manager import CampaignLifecycleManager
from src.studio_operations.workstream import WorkstreamManager
from src.studio_operations.deliverables import DeliverableManager
from src.studio_operations.approval_queue import ApprovalQueue, ApprovalItem
from src.studio_operations.operational_scheduler import StudioOperationalScheduler
from src.studio_operations.continuity_engine import OperationalContinuityEngine, ContinuityActionPlan
from src.studio_operations.handoff import HumanHandoffManager, HandoffPackage
from src.studio_operations.outcomes import OutcomeObservationEngine
from src.studio_operations.performance import StudioPerformanceEngine, StudioPerformanceMetrics
from src.studio_operations.cycle_manager import StudioCycleManager
from src.studio_operations.readiness import ProductionReadinessEngine, ReadinessReport
from src.studio_operations.studio_ledger import StudioOperationsLedger
from src.studio_operations.health import StudioHealthMonitor, StudioHealthReport
from src.creative_workforce.workforce_orchestrator import CreativeWorkforceOrchestrator

class StudioOperationsOrchestrator:
    """Primary control-plane facade for ILYREN Creative Studio operations."""

    def __init__(
        self,
        workforce_orchestrator: Optional[CreativeWorkforceOrchestrator] = None,
        ledger_dir: str = "data/phase15_studio_ledger"
    ):
        self.workforce_orchestrator = workforce_orchestrator or CreativeWorkforceOrchestrator()
        self.client_manager = ClientOperationsManager(
            workforce_context_manager=self.workforce_orchestrator.context_manager
        )
        self.campaign_manager = CampaignLifecycleManager()
        self.workstream_manager = WorkstreamManager()
        self.deliverable_manager = DeliverableManager()
        self.approval_queue = ApprovalQueue()
        self.scheduler = StudioOperationalScheduler()
        self.continuity_engine = OperationalContinuityEngine()
        self.handoff_manager = HumanHandoffManager()
        self.outcome_engine = OutcomeObservationEngine()
        self.performance_engine = StudioPerformanceEngine()
        self.cycle_manager = StudioCycleManager()
        self.readiness_engine = ProductionReadinessEngine()
        self.ledger = StudioOperationsLedger(ledger_dir=ledger_dir)
        self.health_monitor = StudioHealthMonitor()

    def register_client_engagement(self, client_id: str, name: str, industry: str) -> Dict:
        """Initializes a client engagement."""
        client = self.client_manager.create_client(client_id, name, industry)
        self.ledger.record_event(client_id, "CLIENT_REGISTERED", {"client_id": client_id, "name": name})
        return {"client_id": client.client_id, "name": client.name, "status": client.status}

    def bind_client_brand(self, requesting_client_id: str, brand_id: str, brand_name: str, visual_dna_summary: Optional[Dict] = None) -> Dict:
        """Binds a brand to a client."""
        brand = self.client_manager.bind_brand(brand_id, requesting_client_id, brand_name, visual_dna_summary)
        self.ledger.record_event(requesting_client_id, "BRAND_BOUND", {"brand_id": brand_id, "name": brand_name})
        return {"brand_id": brand.brand_id, "client_id": brand.client_id, "name": brand.brand_name}

    def launch_campaign(
        self,
        requesting_client_id: str,
        campaign_id: str,
        brand_id: str,
        title: str,
        objective: str
    ) -> Dict:
        """Launches a campaign under client isolation."""
        campaign = self.campaign_manager.create_campaign(
            requesting_client_id=requesting_client_id,
            campaign_id=campaign_id,
            client_id=requesting_client_id,
            brand_id=brand_id,
            title=title,
            objective=objective
        )
        self.campaign_manager.transition_campaign(requesting_client_id, campaign_id, campaign.status.ACTIVE)
        self.ledger.record_event(requesting_client_id, "CAMPAIGN_LAUNCHED", {"campaign_id": campaign_id, "title": title})
        return {"campaign_id": campaign.campaign_id, "status": campaign.status.value}

    def evaluate_continuity(self, requesting_client_id: str, campaign_id: str) -> ContinuityActionPlan:
        """Evaluates next steps for an active campaign."""
        campaign = self.campaign_manager.get_campaign(requesting_client_id, campaign_id)
        deliverables = self.deliverable_manager.list_deliverables_for_campaign(requesting_client_id, campaign_id)
        pending_apprs = self.approval_queue.list_pending_approvals(requesting_client_id)

        plan = self.continuity_engine.determine_next_steps(
            requesting_client_id=requesting_client_id,
            client_id=requesting_client_id,
            campaign_id=campaign_id,
            campaign_status=campaign.status,
            deliverables=deliverables,
            pending_approvals=pending_apprs
        )
        self.ledger.record_event(requesting_client_id, "CONTINUITY_EVALUATED", {"campaign_id": campaign_id, "steps": len(plan.recommended_steps)})
        return plan

    def submit_deliverable_for_human_approval(
        self,
        requesting_client_id: str,
        approval_id: str,
        campaign_id: str,
        workstream_id: str,
        deliverable_id: str,
        proposed_action: str,
        capability: str,
        target_platform: str
    ) -> ApprovalItem:
        """Submits a deliverable for human approval."""
        item = self.approval_queue.enqueue_request(
            requesting_client_id=requesting_client_id,
            approval_id=approval_id,
            client_id=requesting_client_id,
            campaign_id=campaign_id,
            workstream_id=workstream_id,
            deliverable_id=deliverable_id,
            proposed_action=proposed_action,
            capability=capability,
            target_platform=target_platform
        )
        self.ledger.record_event(requesting_client_id, "APPROVAL_ENQUEUED", {"approval_id": approval_id, "deliverable_id": deliverable_id})
        return item

    def record_human_approval_decision(
        self,
        requesting_client_id: str,
        approval_id: str,
        approved: bool,
        authorizer_id: str
    ) -> ApprovalItem:
        """Records human decision on pending approval."""
        item = self.approval_queue.record_human_decision(
            requesting_client_id=requesting_client_id,
            approval_id=approval_id,
            approved=approved,
            authorizer_id=authorizer_id
        )
        self.ledger.record_event(
            requesting_client_id,
            "HUMAN_DECISION_RECORDED",
            {"approval_id": approval_id, "approved": approved, "authorizer_id": authorizer_id}
        )
        return item

    def get_studio_health(self, requesting_client_id: str) -> StudioHealthReport:
        """Returns health report for studio client."""
        campaigns = self.campaign_manager.list_campaigns(requesting_client_id)
        deliverables = []
        for c in campaigns:
            deliverables.extend(self.deliverable_manager.list_deliverables_for_campaign(requesting_client_id, c.campaign_id))
        approvals = self.approval_queue.list_pending_approvals(requesting_client_id)
        handoffs = self.handoff_manager.list_handoffs_for_client(requesting_client_id)

        return self.health_monitor.evaluate_health(
            requesting_client_id=requesting_client_id,
            target_client_id=requesting_client_id,
            campaigns=campaigns,
            deliverables=deliverables,
            approvals=approvals,
            handoffs=handoffs
        )

    def verify_ledger_integrity(self) -> bool:
        """Verifies the append-only SHA-256 audit ledger."""
        return self.ledger.verify_integrity()
