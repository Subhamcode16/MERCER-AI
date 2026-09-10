"""
Phase 28 Decision Ledger Models and Data Structures.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
import hashlib
import json
from datetime import datetime, timezone


class DecisionType(str, Enum):
    AUDIENCE_SELECTION = "AUDIENCE_SELECTION"
    CREATIVE_TERRITORY = "CREATIVE_TERRITORY"
    VISUAL_DIRECTION = "VISUAL_DIRECTION"
    CHANNEL_SELECTION = "CHANNEL_SELECTION"
    COPY_DIRECTION = "COPY_DIRECTION"
    ASSET_VARIANT = "ASSET_VARIANT"
    LAUNCH_TIMING = "LAUNCH_TIMING"
    TOKEN_LOCK = "TOKEN_LOCK"
    MODEL_SELECTION = "MODEL_SELECTION"


@dataclass
class DecisionAlternative:
    alternative_id: str
    description: str
    rejection_rationale: str
    estimated_risk: float = 0.5


@dataclass
class DecisionContextSnapshot:
    snapshot_id: str
    tenant_id: str
    client_id: str
    brand_id: str
    campaign_id: str
    market_context: Dict[str, Any] = field(default_factory=dict)
    brand_guideline_version: str = "v1.0"
    active_skills: List[str] = field(default_factory=list)


@dataclass
class CampaignDecisionRecord:
    decision_id: str
    campaign_id: str
    decision_type: DecisionType
    decision_version: int
    actor_id: str
    worker_id: Optional[str]
    timestamp: datetime
    context_snapshot: DecisionContextSnapshot
    decision: str
    rationale: str
    evidence_refs: List[str]
    alternatives: List[DecisionAlternative]
    confidence: float
    assumptions: List[str]
    unknowns: List[str]
    expected_impact: str
    parent_hash: Optional[str] = None
    record_hash: str = ""
    status: str = "COMMITTED"  # COMMITTED, CORRECTED, SUPERSEDED
