"""
Strategic Recommendation Models for Phase 29.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..graph.models import IntelligenceClassification
from ..signals.signal_types import EpistemicStatus


class RecommendationStatus(str, Enum):
    PROPOSED = "PROPOSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    CHALLENGED = "CHALLENGED"
    DOWNGRADED = "DOWNGRADED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"


class ReversibilityRating(str, Enum):
    HIGHLY_REVERSIBLE = "HIGHLY_REVERSIBLE"      # Low-cost experiment, easily halted
    MODERATELY_REVERSIBLE = "MODERATELY_REVERSIBLE"  # Campaign direction shift with moderate budget impact
    IRREVERSIBLE = "IRREVERSIBLE"              # Permanent brand positioning overhaul, massive multi-quarter spend


class StrategicRecommendation(BaseModel):
    recommendation_id: str
    tenant_id: str
    classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE
    title: str
    action_statement: str
    why_now: str
    scope: str
    status: RecommendationStatus = RecommendationStatus.PROPOSED
    epistemic_status: EpistemicStatus
    confidence: float
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    alternatives: List[str] = Field(default_factory=list)
    expected_consequences: List[str] = Field(default_factory=list)
    reversibility: ReversibilityRating
    proposed_experiment: Optional[str] = None
    required_human_authority: str = "STRATEGIC_OPERATOR"
    expiration_conditions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    provenance_hash: str = ""
    is_active: bool = True
    challenge_notes: List[str] = Field(default_factory=list)
