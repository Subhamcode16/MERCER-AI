"""
Phase 24 Reliability Dashboard Snapshot Aggregator.
"""
import time
import logging
from typing import Dict, Any
from src.reliability.latency_slo import LatencySLOEvaluator
from src.reliability.availability_slo import AvailabilitySLOEvaluator
from src.reliability.error_budget import ErrorBudgetEngine
from src.reliability.provider_health import ProviderHealthEngine
from src.reliability.workflow_reliability import WorkflowReliabilityTracker

logger = logging.getLogger(__name__)

class ReliabilityDashboard:
    """Aggregates all reliability metrics into a single real-time operational dashboard snapshot."""

    def __init__(
        self,
        latency_eval: LatencySLOEvaluator,
        availability_eval: AvailabilitySLOEvaluator,
        budget_engine: ErrorBudgetEngine,
        health_engine: ProviderHealthEngine,
        workflow_tracker: WorkflowReliabilityTracker
    ):
        self.latency_eval = latency_eval
        self.availability_eval = availability_eval
        self.budget_engine = budget_engine
        self.health_engine = health_engine
        self.workflow_tracker = workflow_tracker

    def get_dashboard_snapshot(self) -> Dict[str, Any]:
        lat_res = self.latency_eval.evaluate_slo()
        avail_res = self.availability_eval.evaluate_slo()
        budget_res = self.budget_engine.calculate_budget_status()
        wf_res = self.workflow_tracker.get_reliability_summary()

        overall_healthy = (
            lat_res["passed"] and
            avail_res["passed"] and
            not budget_res.exhausted
        )

        return {
            "timestamp": time.time(),
            "overall_healthy": overall_healthy,
            "availability": avail_res,
            "latency": lat_res,
            "error_budget": {
                "consumed": budget_res.consumed_budget,
                "remaining": budget_res.remaining_budget,
                "burn_rate": budget_res.burn_rate_1h,
                "exhausted": budget_res.exhausted
            },
            "workflow_reliability": wf_res,
            "active_alerts": [a.message for a in self.budget_engine.list_alerts()]
        }
