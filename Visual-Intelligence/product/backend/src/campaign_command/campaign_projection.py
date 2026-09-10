"""
Phase 25 Campaign Lifecycle State Machine and Projection Models.
Distinguishes granular lifecycle states: PROPOSED, REVIEW_REQUIRED, APPROVAL_REQUIRED, AUTHORIZED, EXECUTING, EXECUTED, OBSERVED, LEARNED.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

class DetailedCampaignState(str, Enum):
    PROPOSED = "PROPOSED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    AUTHORIZED = "AUTHORIZED"
    EXECUTING = "EXECUTING"
    EXECUTED = "EXECUTED"
    OBSERVED = "OBSERVED"
    LEARNED = "LEARNED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"

@dataclass
class CampaignDetailedProjection:
    campaign_id: str
    tenant_id: str
    client_id: str
    name: str
    objective: Dict[str, Any]
    state: DetailedCampaignState
    version: int
    active_workstreams: List[str] = field(default_factory=list)
    deliverables: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[Dict[str, Any]] = field(default_factory=list)
    workforce_activity: List[Dict[str, Any]] = field(default_factory=list)
    reviews: List[Dict[str, Any]] = field(default_factory=list)
    approvals: List[Dict[str, Any]] = field(default_factory=list)
    execution_receipt: Optional[Dict[str, Any]] = None
    outcomes: Optional[Dict[str, Any]] = None
    learning_signals: List[Dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
