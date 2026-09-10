"""
Intelligence-to-Execution Bridge Module (Phase 30).
Connects Strategic Decisions & Initiatives to Phase 29 Creative Intelligence and Phase 28 Outcome Learning.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
import hashlib
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class CampaignProposalFromStrategy(BaseModel):
    proposal_id: str = Field(default_factory=lambda: f"prop_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    initiative_id: str
    decision_id: str
    campaign_title: str
    scope_description: str
    is_human_approved: bool = False
    approved_by: Optional[str] = None
    approval_token: Optional[str] = None
    approval_timestamp: Optional[datetime] = None
    created_at: datetime = Field(default_factory=utc_now)


class OutcomeIngestRecord(BaseModel):
    ingest_id: str = Field(default_factory=lambda: f"ing_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    campaign_id: str
    initiative_id: str
    observed_metrics: Dict[str, Any]
    phase28_learning_summary: str
    phase29_signal_updates: List[str] = Field(default_factory=list)
    received_at: datetime = Field(default_factory=utc_now)


class StrategicExecutionBridge:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._proposals: Dict[str, CampaignProposalFromStrategy] = {}
        self._outcomes: List[OutcomeIngestRecord] = []

    def create_campaign_proposal(self, initiative_id: str, decision_id: str, campaign_title: str, scope: str) -> CampaignProposalFromStrategy:
        proposal = CampaignProposalFromStrategy(
            tenant_id=self.tenant_id,
            initiative_id=initiative_id,
            decision_id=decision_id,
            campaign_title=campaign_title,
            scope_description=scope
        )
        self._proposals[proposal.proposal_id] = proposal
        return proposal

    def approve_proposal_by_human(self, proposal_id: str, approver_actor: str, auth_token: str) -> CampaignProposalFromStrategy:
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found.")
        
        # T30-021: Human approval spoofing check
        if not auth_token or len(auth_token) < 16:
            raise GovernanceInvariantViolation(
                ThreatID.T30_021,
                "Invalid or spoofed human authorization token.",
                {"proposal_id": proposal_id, "actor": approver_actor}
            )

        proposal.is_human_approved = True
        proposal.approved_by = approver_actor
        proposal.approval_token = auth_token
        proposal.approval_timestamp = utc_now()
        return proposal

    def execute_campaign(self, proposal_id: str, caller_agent: str) -> Dict[str, Any]:
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found.")
        
        # T30-003: Recommendation-to-execution escalation prevention
        if not proposal.is_human_approved:
            raise GovernanceInvariantViolation(
                ThreatID.T30_003,
                f"Cannot execute campaign proposal '{proposal_id}' without explicit human approval.",
                {"proposal_id": proposal_id, "caller": caller_agent}
            )
        
        return {
            "status": "FORWARDED_TO_EXECUTION_GATEWAY",
            "proposal_id": proposal.proposal_id,
            "campaign_title": proposal.campaign_title,
            "approved_by": proposal.approved_by
        }

    def ingest_phase28_outcome(self, campaign_id: str, initiative_id: str, metrics: Dict[str, Any], learning: str) -> OutcomeIngestRecord:
        record = OutcomeIngestRecord(
            tenant_id=self.tenant_id,
            campaign_id=campaign_id,
            initiative_id=initiative_id,
            observed_metrics=metrics,
            phase28_learning_summary=learning
        )
        self._outcomes.append(record)
        return record
