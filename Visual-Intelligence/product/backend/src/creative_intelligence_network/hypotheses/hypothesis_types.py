"""
Hypothesis Lifecycle Models and Enums for Phase 29.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..graph.models import IntelligenceClassification


class HypothesisStatus(str, Enum):
    PROPOSED = "PROPOSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    TESTABLE = "TESTABLE"
    TESTING = "TESTING"
    SUPPORTED = "SUPPORTED"
    WEAKENED = "WEAKENED"
    CONTRADICTED = "CONTRADICTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


class StrategicHypothesis(BaseModel):
    hypothesis_id: str
    tenant_id: str
    classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE
    statement: str
    scope: str
    origin_signals: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    counterevidence: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    confidence: float = 0.5
    falsification_criteria: str
    required_experiment: Optional[str] = None
    owner: str = "SYSTEM_INTELLIGENCE"
    status: HypothesisStatus = HypothesisStatus.PROPOSED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    related_decisions: List[str] = Field(default_factory=list)
    provenance_hash: str = ""
    is_active: bool = True
