"""
Opportunity Intelligence Engine for Phase 29.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
from pydantic import BaseModel, Field
from ..graph.models import IntelligenceClassification, GraphEntity, GraphRelationship, EntityType, RelationType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class OpportunityTier(str, Enum):
    IMMEDIATE_ACTION = "IMMEDIATE_ACTION"
    EXPERIMENT_REQUIRED = "EXPERIMENT_REQUIRED"
    MONITOR_ONLY = "MONITOR_ONLY"


class StrategicOpportunity(BaseModel):
    opportunity_id: str
    tenant_id: str
    classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE
    title: str
    description: str
    scope: str
    tier: OpportunityTier
    supporting_evidence: List[str] = Field(default_factory=list)
    expected_upside: str
    uncertainty_score: float = 0.5
    prerequisites: List[str] = Field(default_factory=list)
    associated_risks: List[str] = Field(default_factory=list)
    experiment_candidate: Optional[str] = None
    decision_required: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class OpportunityEngine:
    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._opportunities: Dict[str, StrategicOpportunity] = {}

    def register_opportunity(
        self,
        tenant_id: str,
        title: str,
        description: str,
        scope: str,
        tier: OpportunityTier,
        expected_upside: str,
        decision_required: str,
        supporting_evidence: Optional[List[str]] = None,
        prerequisites: Optional[List[str]] = None,
        associated_risks: Optional[List[str]] = None,
        experiment_candidate: Optional[str] = None,
        uncertainty_score: float = 0.5,
        classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE,
    ) -> StrategicOpportunity:
        supp = supporting_evidence or []
        prereqs = prerequisites or []
        risks = associated_risks or []

        opp_id = f"OPP-{hashlib.sha256(f'{tenant_id}:{title}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"

        opp = StrategicOpportunity(
            opportunity_id=opp_id,
            tenant_id=tenant_id,
            classification=classification,
            title=title,
            description=description,
            scope=scope,
            tier=tier,
            supporting_evidence=supp,
            expected_upside=expected_upside,
            uncertainty_score=uncertainty_score,
            prerequisites=prereqs,
            associated_risks=risks,
            experiment_candidate=experiment_candidate,
            decision_required=decision_required,
        )

        self._opportunities[opp_id] = opp

        # Sync with Graph
        entity = GraphEntity(
            entity_id=opp_id,
            entity_type=EntityType.OPPORTUNITY,
            tenant_id=tenant_id,
            classification=classification,
            name=title,
            properties={
                "tier": tier.value,
                "expected_upside": expected_upside,
                "uncertainty": uncertainty_score,
                "scope": scope,
            },
        )
        self.graph.add_entity(entity)

        return opp

    def get_opportunity(self, opp_id: str, tenant_id: Optional[str] = None) -> Optional[StrategicOpportunity]:
        opp = self._opportunities.get(opp_id)
        if not opp:
            return None
        if tenant_id and opp.classification == IntelligenceClassification.CLIENT_PRIVATE:
            if opp.tenant_id != tenant_id:
                return None
        return opp

    def list_opportunities(self, tenant_id: str) -> List[StrategicOpportunity]:
        return [
            o for o in self._opportunities.values()
            if (o.tenant_id == tenant_id or o.classification != IntelligenceClassification.CLIENT_PRIVATE)
            and o.is_active
        ]
