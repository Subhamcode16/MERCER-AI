"""
Strategic Signal Types and Epistemic Definitions for Phase 29.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..graph.models import IntelligenceClassification


class SignalClass(str, Enum):
    EMERGING_PATTERN = "EMERGING_PATTERN"
    DECLINING_PATTERN = "DECLINING_PATTERN"
    PERFORMANCE_SHIFT = "PERFORMANCE_SHIFT"
    CREATIVE_FATIGUE = "CREATIVE_FATIGUE"
    AUDIENCE_SHIFT = "AUDIENCE_SHIFT"
    PRODUCT_OPPORTUNITY = "PRODUCT_OPPORTUNITY"
    MARKET_SIGNAL = "MARKET_SIGNAL"
    VISUAL_SHIFT = "VISUAL_SHIFT"
    KNOWLEDGE_CONTRADICTION = "KNOWLEDGE_CONTRADICTION"
    KNOWLEDGE_DECAY = "KNOWLEDGE_DECAY"
    ENVIRONMENT_DRIFT = "ENVIRONMENT_DRIFT"
    MODEL_DRIFT = "MODEL_DRIFT"
    RISK_SIGNAL = "RISK_SIGNAL"
    EXPERIMENT_OPPORTUNITY = "EXPERIMENT_OPPORTUNITY"
    UNCERTAINTY_CLUSTER = "UNCERTAINTY_CLUSTER"


class EpistemicStatus(str, Enum):
    OBSERVATIONAL_CORRELATION = "OBSERVATIONAL_CORRELATION"
    CONFOUNDED_OBSERVATION = "CONFOUNDED_OBSERVATION"
    EXPERIMENTAL_EVIDENCE = "EXPERIMENTAL_EVIDENCE"
    THEORETICAL_INFERENCE = "THEORETICAL_INFERENCE"
    HYPOTHETICAL = "HYPOTHETICAL"
    UNVERIFIED_EXTERNAL = "UNVERIFIED_EXTERNAL"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class SignalLifecycle(str, Enum):
    OBSERVED = "OBSERVED"
    NORMALIZED = "NORMALIZED"
    CORRELATED = "CORRELATED"
    CONTEXTUALIZED = "CONTEXTUALIZED"
    HYPOTHESIS = "HYPOTHESIS"
    VALIDATED = "VALIDATED"
    UNRESOLVED = "UNRESOLVED"
    REJECTED = "REJECTED"
    STRATEGIC_SIGNAL = "STRATEGIC_SIGNAL"
    SCENARIO_ANALYSIS = "SCENARIO_ANALYSIS"
    RECOMMENDATION = "RECOMMENDATION"
    EXPIRED = "EXPIRED"


class StrategicSignal(BaseModel):
    signal_id: str
    tenant_id: str
    classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE
    signal_class: SignalClass
    lifecycle_state: SignalLifecycle = SignalLifecycle.OBSERVED
    scope: str
    observed_pattern: str
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    method: str
    confidence: float
    epistemic_status: EpistemicStatus
    freshness: float = 1.0
    assumptions: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    provenance_hash: str = ""
    is_active: bool = True
