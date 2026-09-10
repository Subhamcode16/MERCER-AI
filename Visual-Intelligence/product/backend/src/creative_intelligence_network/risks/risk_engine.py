"""
Risk Intelligence Engine for Phase 29.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
from pydantic import BaseModel, Field
from ..graph.models import IntelligenceClassification, GraphEntity, GraphRelationship, EntityType, RelationType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class StrategicRisk(BaseModel):
    risk_id: str
    tenant_id: str
    classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE
    title: str
    description: str
    scope: str
    severity: RiskSeverity
    supporting_evidence: List[str] = Field(default_factory=list)
    uncertainty_score: float = 0.5
    leading_indicators: List[str] = Field(default_factory=list)
    mitigation_options: List[str] = Field(default_factory=list)
    escalation_required: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class RiskEngine:
    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._risks: Dict[str, StrategicRisk] = {}

    def register_risk(
        self,
        tenant_id: str,
        title: str,
        description: str,
        scope: str,
        severity: RiskSeverity,
        mitigation_options: List[str],
        supporting_evidence: Optional[List[str]] = None,
        leading_indicators: Optional[List[str]] = None,
        uncertainty_score: float = 0.5,
        escalation_required: bool = False,
        classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE,
    ) -> StrategicRisk:
        supp = supporting_evidence or []
        indicators = leading_indicators or []

        risk_id = f"RSK-{hashlib.sha256(f'{tenant_id}:{title}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"

        risk = StrategicRisk(
            risk_id=risk_id,
            tenant_id=tenant_id,
            classification=classification,
            title=title,
            description=description,
            scope=scope,
            severity=severity,
            supporting_evidence=supp,
            uncertainty_score=uncertainty_score,
            leading_indicators=indicators,
            mitigation_options=mitigation_options,
            escalation_required=escalation_required,
        )

        self._risks[risk_id] = risk

        # Sync with Graph
        entity = GraphEntity(
            entity_id=risk_id,
            entity_type=EntityType.RISK,
            tenant_id=tenant_id,
            classification=classification,
            name=title,
            properties={
                "severity": severity.value,
                "escalation_required": escalation_required,
                "uncertainty": uncertainty_score,
                "scope": scope,
            },
        )
        self.graph.add_entity(entity)

        return risk

    def get_risk(self, risk_id: str, tenant_id: Optional[str] = None) -> Optional[StrategicRisk]:
        rsk = self._risks.get(risk_id)
        if not rsk:
            return None
        if tenant_id and rsk.classification == IntelligenceClassification.CLIENT_PRIVATE:
            if rsk.tenant_id != tenant_id:
                return None
        return rsk

    def list_risks(self, tenant_id: str) -> List[StrategicRisk]:
        return [
            r for r in self._risks.values()
            if (r.tenant_id == tenant_id or r.classification != IntelligenceClassification.CLIENT_PRIVATE)
            and r.is_active
        ]
