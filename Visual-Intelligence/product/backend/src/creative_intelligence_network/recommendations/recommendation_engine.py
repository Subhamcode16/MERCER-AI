"""
Strategic Recommendation Engine synthesizing hypotheses, scenarios, and evidence into human-actionable recommendations.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
import json
from .recommendation_models import StrategicRecommendation, RecommendationStatus, ReversibilityRating
from .quality_contract import RecommendationQualityContract
from ..graph.models import IntelligenceClassification, GraphEntity, GraphRelationship, EntityType, RelationType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph
from ..signals.signal_types import EpistemicStatus


class StrategicRecommendationEngine:
    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._recommendations: Dict[str, StrategicRecommendation] = {}

    def generate_recommendation(
        self,
        tenant_id: str,
        title: str,
        action_statement: str,
        why_now: str,
        scope: str,
        epistemic_status: EpistemicStatus,
        initial_confidence: float,
        supporting_evidence: List[str],
        contradicting_evidence: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        unknowns: Optional[List[str]] = None,
        alternatives: Optional[List[str]] = None,
        expected_consequences: Optional[List[str]] = None,
        reversibility: ReversibilityRating = ReversibilityRating.MODERATELY_REVERSIBLE,
        proposed_experiment: Optional[str] = None,
        required_human_authority: str = "STRATEGIC_OPERATOR",
        classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE,
    ) -> StrategicRecommendation:
        count = contradicting_evidence or []
        assump = assumptions or []
        unkn = unknowns or ["Unobserved counterfactual dynamics remain unknown."]
        alts = alternatives or ["Maintain status quo baseline strategy."]
        conseq = expected_consequences or ["Potential incremental lift vs platform volatility."]

        rec_id = f"REC-{hashlib.sha256(f'{tenant_id}:{title}:{action_statement}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"

        rec = StrategicRecommendation(
            recommendation_id=rec_id,
            tenant_id=tenant_id,
            classification=classification,
            title=title,
            action_statement=action_statement,
            why_now=why_now,
            scope=scope,
            status=RecommendationStatus.PROPOSED,
            epistemic_status=epistemic_status,
            confidence=initial_confidence,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=count,
            assumptions=assump,
            unknowns=unkn,
            alternatives=alts,
            expected_consequences=conseq,
            reversibility=reversibility,
            proposed_experiment=proposed_experiment,
            required_human_authority=required_human_authority,
        )

        # Apply Quality Contract Audit
        audit = RecommendationQualityContract.audit_recommendation(rec)
        rec.confidence = audit.adjusted_confidence
        rec.status = audit.final_status

        # Compute provenance hash
        payload = {
            "rec_id": rec.recommendation_id,
            "tenant_id": rec.tenant_id,
            "title": rec.title,
            "action": rec.action_statement,
            "scope": rec.scope,
            "confidence": rec.confidence,
            "evidence": rec.supporting_evidence,
        }
        rec.provenance_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

        self._recommendations[rec_id] = rec

        # Sync with Graph
        entity = GraphEntity(
            entity_id=rec_id,
            entity_type=EntityType.RECOMMENDATION,
            tenant_id=tenant_id,
            classification=classification,
            name=title,
            properties={
                "action": action_statement,
                "confidence": rec.confidence,
                "status": rec.status.value,
                "reversibility": rec.reversibility.value,
                "scope": scope,
            },
            provenance_hashes=[rec.provenance_hash],
        )
        self.graph.add_entity(entity)

        # Link supporting evidence
        for ev_id in supporting_evidence:
            if self.graph.get_entity(ev_id):
                self.graph.add_relationship(
                    GraphRelationship(
                        relationship_id=f"REL-{ev_id}-{rec_id}",
                        source_id=ev_id,
                        target_id=rec_id,
                        relation_type=RelationType.SUPPORTS,
                        tenant_id=tenant_id,
                        classification=classification,
                        scope=scope,
                    )
                )

        return rec

    def challenge_recommendation(
        self,
        recommendation_id: str,
        operator_notes: str,
        new_counterevidence: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
    ) -> StrategicRecommendation:
        rec = self._recommendations.get(recommendation_id)
        if not rec:
            raise ValueError(f"Recommendation '{recommendation_id}' not found.")
        if tenant_id and rec.tenant_id != tenant_id:
            raise ValueError(f"Access denied for tenant '{tenant_id}'.")

        rec.status = RecommendationStatus.CHALLENGED
        rec.challenge_notes.append(operator_notes)

        if new_counterevidence:
            for c in new_counterevidence:
                if c not in rec.contradicting_evidence:
                    rec.contradicting_evidence.append(c)

        # Re-audit and apply downgrade
        audit = RecommendationQualityContract.audit_recommendation(rec)
        rec.confidence = audit.adjusted_confidence
        if audit.final_status == RecommendationStatus.DOWNGRADED:
            rec.status = RecommendationStatus.DOWNGRADED

        return rec

    def get_recommendation(self, rec_id: str, tenant_id: Optional[str] = None) -> Optional[StrategicRecommendation]:
        rec = self._recommendations.get(rec_id)
        if not rec:
            return None
        if tenant_id and rec.classification == IntelligenceClassification.CLIENT_PRIVATE:
            if rec.tenant_id != tenant_id:
                return None
        return rec

    def list_recommendations(self, tenant_id: str, status: Optional[RecommendationStatus] = None) -> List[StrategicRecommendation]:
        return [
            r for r in self._recommendations.values()
            if (r.tenant_id == tenant_id or r.classification != IntelligenceClassification.CLIENT_PRIVATE)
            and (status is None or r.status == status)
            and r.is_active
        ]
