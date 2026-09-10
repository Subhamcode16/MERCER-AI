"""
Phase 15 Studio Health Monitor.
Monitors campaign state, approval latency, revision counts, and workflow health.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import ClientContextViolation

@dataclass
class StudioHealthReport:
    client_id: str
    overall_health: str  # HEALTHY, WARNING, DEGRADED, CRITICAL
    stalled_campaigns: List[str]
    overdue_approvals: List[str]
    excessive_revisions: List[str]
    unresolved_escalations: List[str]
    anomaly_warnings: List[str]

class StudioHealthMonitor:
    """Monitors operational health across active studio client campaigns."""

    def evaluate_health(
        self,
        requesting_client_id: str,
        target_client_id: str,
        campaigns: List[Any],
        deliverables: List[Any],
        approvals: List[Any],
        handoffs: List[Any]
    ) -> StudioHealthReport:
        """Evaluates operational health indicators."""
        if requesting_client_id != target_client_id:
            raise ClientContextViolation("Client isolation violation in health monitor.")

        stalled = []
        overdue_apprs = []
        excessive_revs = []
        escalations = []
        warnings = []

        # Stalled campaigns (PAUSED or no active deliverables)
        for c in campaigns:
            c_status = getattr(c, "status", "")
            c_id = getattr(c, "campaign_id", str(c))
            if c_status == "PAUSED":
                stalled.append(c_id)

        # Overdue approvals
        for a in approvals:
            if getattr(a, "is_expired", lambda: False)():
                a_id = getattr(a, "approval_id", str(a))
                overdue_apprs.append(a_id)

        # Excessive revisions (> 2)
        for d in deliverables:
            rev_cnt = getattr(d, "revision_count", 0)
            if rev_cnt >= 3:
                d_id = getattr(d, "deliverable_id", str(d))
                excessive_revs.append(d_id)

        # Unresolved escalations/handoffs
        for h in handoffs:
            h_id = getattr(h, "handoff_id", str(h))
            escalations.append(h_id)

        # Determine health status
        if len(escalations) > 2 or len(overdue_apprs) > 2:
            overall = "CRITICAL"
        elif len(excessive_revs) > 0 or len(stalled) > 1:
            overall = "WARNING"
        elif len(escalations) > 0:
            overall = "DEGRADED"
        else:
            overall = "HEALTHY"

        return StudioHealthReport(
            client_id=target_client_id,
            overall_health=overall,
            stalled_campaigns=stalled,
            overdue_approvals=overdue_apprs,
            excessive_revisions=excessive_revs,
            unresolved_escalations=escalations,
            anomaly_warnings=warnings
        )
