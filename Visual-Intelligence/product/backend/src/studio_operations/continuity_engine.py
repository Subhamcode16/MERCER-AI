"""
Phase 15 Operational Continuity Engine.
Evaluates active campaign state and determines inspectable next bounded operational steps without initiating side effects.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import ContinuityViolation, ClientContextViolation
from src.studio_operations.studio_models import DeliverableStatus, CampaignStatus

@dataclass
class ContinuityStep:
    step_id: str
    action_type: str  # DRAFT_CONTENT, SELF_CRITIQUE, INDEPENDENT_REVIEW, REVISE_ARTIFACT, ENQUEUE_APPROVAL, WAIT_FOR_APPROVAL, OBSERVE_OUTCOME, ESCALATE
    target_id: str
    description: str
    requires_human_decision: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContinuityActionPlan:
    campaign_id: str
    client_id: str
    recommended_steps: List[ContinuityStep]
    pending_human_decisions: List[str]
    waiting_conditions: List[str]
    status: str = "VALID"

class OperationalContinuityEngine:
    """Evaluates campaign/workstream progression and synthesizes bounded next steps."""

    def determine_next_steps(
        self,
        requesting_client_id: str,
        client_id: str,
        campaign_id: str,
        campaign_status: CampaignStatus,
        deliverables: List[Any],
        pending_approvals: List[Any]
    ) -> ContinuityActionPlan:
        """Determines the next bounded operational steps for a campaign."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot evaluate continuity for client '{client_id}' from context '{requesting_client_id}'."
            )

        if campaign_status in [CampaignStatus.PAUSED, CampaignStatus.CANCELLED, CampaignStatus.COMPLETED]:
            return ContinuityActionPlan(
                campaign_id=campaign_id,
                client_id=client_id,
                recommended_steps=[],
                pending_human_decisions=[],
                waiting_conditions=[f"Campaign status is {campaign_status.value}. No actions generated."],
                status="PAUSED" if campaign_status == CampaignStatus.PAUSED else "INACTIVE"
            )

        recommended_steps: List[ContinuityStep] = []
        pending_decisions: List[str] = []
        waiting_conditions: List[str] = []

        # Analyze deliverables and generate deterministic next steps
        for d in deliverables:
            d_id = getattr(d, "deliverable_id", str(d))
            d_status = getattr(d, "status", DeliverableStatus.PLANNED)

            if d_status == DeliverableStatus.PLANNED:
                recommended_steps.append(ContinuityStep(
                    step_id=f"step_{d_id}_draft",
                    action_type="DRAFT_CONTENT",
                    target_id=d_id,
                    description=f"Draft content for deliverable '{d_id}'."
                ))
            elif d_status == DeliverableStatus.DRAFT:
                recommended_steps.append(ContinuityStep(
                    step_id=f"step_{d_id}_critique",
                    action_type="SELF_CRITIQUE",
                    target_id=d_id,
                    description=f"Run self-critique on deliverable '{d_id}'."
                ))
            elif d_status == DeliverableStatus.CRITIQUE:
                recommended_steps.append(ContinuityStep(
                    step_id=f"step_{d_id}_review",
                    action_type="INDEPENDENT_REVIEW",
                    target_id=d_id,
                    description=f"Submit deliverable '{d_id}' to double-blind independent review."
                ))
            elif d_status == DeliverableStatus.REVISION:
                recommended_steps.append(ContinuityStep(
                    step_id=f"step_{d_id}_revise",
                    action_type="REVISE_ARTIFACT",
                    target_id=d_id,
                    description=f"Perform bounded revision cycle on deliverable '{d_id}'."
                ))
            elif d_status == DeliverableStatus.REVIEW:
                recommended_steps.append(ContinuityStep(
                    step_id=f"step_{d_id}_approval_prep",
                    action_type="ENQUEUE_APPROVAL",
                    target_id=d_id,
                    description=f"Prepare human approval package for deliverable '{d_id}'."
                ))
            elif d_status == DeliverableStatus.APPROVED:
                # Waiting for execution authorization / schedule
                waiting_conditions.append(f"Deliverable '{d_id}' is APPROVED, pending execution window.")
            elif d_status == DeliverableStatus.READY_FOR_EXECUTION:
                # Requires Phase 10 authorization
                pending_decisions.append(f"Execution authorization required for '{d_id}'.")
            elif d_status == DeliverableStatus.EXECUTED:
                recommended_steps.append(ContinuityStep(
                    step_id=f"step_{d_id}_observe",
                    action_type="OBSERVE_OUTCOME",
                    target_id=d_id,
                    description=f"Collect post-execution outcomes for deliverable '{d_id}'."
                ))

        # Check pending approval queue
        for appr in pending_approvals:
            appr_id = getattr(appr, "approval_id", str(appr))
            pending_decisions.append(f"Human decision pending for approval '{appr_id}'.")

        return ContinuityActionPlan(
            campaign_id=campaign_id,
            client_id=client_id,
            recommended_steps=recommended_steps,
            pending_human_decisions=pending_decisions,
            waiting_conditions=waiting_conditions,
            status="VALID"
        )
