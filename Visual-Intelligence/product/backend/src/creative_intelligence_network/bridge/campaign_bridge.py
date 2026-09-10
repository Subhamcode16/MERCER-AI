"""
Intelligence-to-Campaign Bridge with strict Human Decision Gate.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
from pydantic import BaseModel, Field
from ..recommendations.recommendation_models import StrategicRecommendation, RecommendationStatus
from ..graph.models import IntelligenceClassification, GraphEntity, GraphRelationship, EntityType, RelationType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class HumanDecisionRecord(BaseModel):
    decision_id: str
    tenant_id: str
    decision_maker: str
    decision_maker_role: str
    selected_recommendation_id: str
    action_approved: str
    rejected_alternatives: List[str] = Field(default_factory=list)
    accepted_assumptions: List[str] = Field(default_factory=list)
    operator_rationale: str
    resulting_campaign_id: Optional[str] = None
    resulting_experiment_id: Optional[str] = None
    dissent_or_uncertainty_notes: Optional[str] = None
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class IntelligenceToCampaignBridge:
    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._decisions: Dict[str, HumanDecisionRecord] = {}

    def record_human_decision_and_create_campaign(
        self,
        tenant_id: str,
        decision_maker: str,
        decision_maker_role: str,
        recommendation: StrategicRecommendation,
        operator_rationale: str,
        rejected_alternatives: Optional[List[str]] = None,
        accepted_assumptions: Optional[List[str]] = None,
        campaign_name_override: Optional[str] = None,
        is_experiment: bool = False,
        dissent_notes: Optional[str] = None,
    ) -> HumanDecisionRecord:
        # Invariant: Human authority role required
        if decision_maker_role not in ("STRATEGIC_OPERATOR", "CAMPAIGN_DIRECTOR", "ADMIN", "EXECUTIVE"):
            raise PermissionError(f"Role '{decision_maker_role}' is unauthorized to execute strategic campaign decisions.")

        # Invariant: Recommendation must not be rejected or withdrawn
        if recommendation.status in (RecommendationStatus.REJECTED, RecommendationStatus.WITHDRAWN):
            raise ValueError(f"Cannot execute decision on recommendation with status '{recommendation.status.value}'.")

        rejs = rejected_alternatives or recommendation.alternatives
        assumps = accepted_assumptions or recommendation.assumptions

        decision_id = f"DEC-{hashlib.sha256(f'{tenant_id}:{recommendation.recommendation_id}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"
        
        camp_id = None
        exp_id = None
        if is_experiment or recommendation.proposed_experiment:
            exp_id = f"EXP-{hashlib.sha256(f'{decision_id}:EXP'.encode()).hexdigest()[:10]}"
        else:
            camp_id = f"CAMP-{hashlib.sha256(f'{decision_id}:CAMP'.encode()).hexdigest()[:10]}"

        decision = HumanDecisionRecord(
            decision_id=decision_id,
            tenant_id=tenant_id,
            decision_maker=decision_maker,
            decision_maker_role=decision_maker_role,
            selected_recommendation_id=recommendation.recommendation_id,
            action_approved=recommendation.action_statement,
            rejected_alternatives=rejs,
            accepted_assumptions=assumps,
            operator_rationale=operator_rationale,
            resulting_campaign_id=camp_id,
            resulting_experiment_id=exp_id,
            dissent_or_uncertainty_notes=dissent_notes,
        )

        self._decisions[decision_id] = decision
        recommendation.status = RecommendationStatus.ACCEPTED

        # Sync to graph
        entity = GraphEntity(
            entity_id=decision_id,
            entity_type=EntityType.HUMAN_DECISION,
            tenant_id=tenant_id,
            classification=IntelligenceClassification.CLIENT_PRIVATE,
            name=f"Human Decision: {decision_id}",
            properties={
                "decision_maker": decision_maker,
                "action": decision.action_approved,
                "resulting_campaign": camp_id,
                "resulting_experiment": exp_id,
            },
        )
        self.graph.add_entity(entity)

        # Link Recommendation to Human Decision if recommendation is in graph
        if self.graph.get_entity(recommendation.recommendation_id):
            self.graph.add_relationship(
                GraphRelationship(
                    relationship_id=f"REL-{recommendation.recommendation_id}-{decision_id}",
                    source_id=recommendation.recommendation_id,
                    target_id=decision_id,
                    relation_type=RelationType.DECIDED_BY,
                    tenant_id=tenant_id,
                    classification=IntelligenceClassification.CLIENT_PRIVATE,
                    scope=recommendation.scope,
                )
            )

        return decision

    def get_decision(self, decision_id: str, tenant_id: Optional[str] = None) -> Optional[HumanDecisionRecord]:
        dec = self._decisions.get(decision_id)
        if not dec:
            return None
        if tenant_id and dec.tenant_id != tenant_id:
            return None
        return dec
