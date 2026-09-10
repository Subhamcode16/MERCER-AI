"""
Foresight & Scenario Models for Phase 29.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..graph.models import IntelligenceClassification


class ScenarioArchetype(str, Enum):
    BASELINE = "BASELINE"
    UPSIDE = "UPSIDE"
    DOWNSIDE = "DOWNSIDE"
    DISRUPTION = "DISRUPTION"
    UNKNOWN = "UNKNOWN"


class StrategicScenario(BaseModel):
    scenario_id: str
    tenant_id: str
    classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE
    archetype: ScenarioArchetype
    title: str
    description: str
    scope: str
    initiating_signals: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    contradictory_evidence: List[str] = Field(default_factory=list)
    bounded_likelihood: Optional[float] = None
    uncertainty_score: float = 0.5
    leading_indicators: List[str] = Field(default_factory=list)
    lagging_indicators: List[str] = Field(default_factory=list)
    potential_consequences: List[str] = Field(default_factory=list)
    monitoring_actions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
