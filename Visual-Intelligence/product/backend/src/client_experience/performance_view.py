"""
Phase 16 Performance & Outcome View.
Provides projections of turnaround time, revision rates, and execution success metrics.
"""

from typing import Any
from src.client_experience.workspace_models import PerformanceSummaryDTO
from src.client_experience.access_models import UserIdentity

class PerformanceOutcomeView:
    """View provider for performance and outcome metrics."""

    def get_performance_summary(self, user: UserIdentity, studio_orchestrator: Any) -> PerformanceSummaryDTO:
        """Retrieves and projects performance metrics for a client."""
        user.verify_capability("view_performance")
        client_id = user.assigned_client_id

        campaigns = studio_orchestrator.campaign_manager.list_campaigns(client_id)
        deliverables = []
        for c in campaigns:
            deliverables.extend(studio_orchestrator.deliverable_manager.list_deliverables_for_campaign(client_id, c.campaign_id))
        approvals = studio_orchestrator.approval_queue.list_pending_approvals(client_id)

        metrics = studio_orchestrator.performance_engine.calculate_metrics(
            requesting_client_id=client_id,
            target_client_id=client_id,
            deliverables=deliverables,
            approvals=approvals
        )

        return PerformanceSummaryDTO(
            client_id=client_id,
            total_deliverables=metrics.total_deliverables,
            completed_deliverables=metrics.completed_deliverables,
            revision_rate=metrics.average_revision_count,
            execution_success_rate=metrics.execution_success_rate,
            efficiency_score=metrics.workflow_efficiency_score
        )
