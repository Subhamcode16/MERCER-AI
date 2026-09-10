"""
Phase 16 Client Experience Workspace DTO Models.
Safe, secret-free presentation models projected from internal domain state.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

@dataclass(frozen=True)
class BrandDTO:
    brand_id: str
    client_id: str
    brand_name: str
    visual_dna_summary: Dict[str, Any]
    tone_of_voice: str

@dataclass(frozen=True)
class DeliverableDTO:
    deliverable_id: str
    campaign_id: str
    client_id: str
    title: str
    deliverable_type: str
    status: str
    content_summary: Dict[str, Any]
    revision_count: int
    version: str

@dataclass(frozen=True)
class ApprovalSummaryDTO:
    approval_id: str
    client_id: str
    campaign_id: str
    deliverable_id: str
    proposed_action: str
    target_platform: str
    risk_classification: str
    status: str
    expires_at: str
    nonce: str

@dataclass(frozen=True)
class CampaignDTO:
    campaign_id: str
    client_id: str
    brand_id: str
    title: str
    objective: str
    status: str
    deliverables_count: int
    created_at: str

@dataclass(frozen=True)
class WorkforceActivityDTO:
    staff_id: str
    role: str
    department: str
    current_task: str
    status: str
    revision_count: int

@dataclass(frozen=True)
class TimelineEventDTO:
    event_id: str
    timestamp: str
    client_id: str
    actor_role: str
    event_type: str
    summary: str
    correlation_id: str

@dataclass(frozen=True)
class PerformanceSummaryDTO:
    client_id: str
    total_deliverables: int
    completed_deliverables: int
    revision_rate: float
    execution_success_rate: float
    efficiency_score: float

@dataclass(frozen=True)
class ClientWorkspaceDTO:
    client_id: str
    name: str
    industry: str
    active_campaigns_count: int
    pending_approvals_count: int
    overall_health: str
