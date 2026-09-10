"""
Hypothesis Lifecycle Engine managing state transitions, evidence bindings, and falsification rules.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
import json
from .hypothesis_types import StrategicHypothesis, HypothesisStatus
from ..graph.models import IntelligenceClassification, GraphEntity, GraphRelationship, EntityType, RelationType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class HypothesisEngine:
    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._hypotheses: Dict[str, StrategicHypothesis] = {}

    def propose_hypothesis(
        self,
        tenant_id: str,
        statement: str,
        scope: str,
        falsification_criteria: str,
        origin_signals: Optional[List[str]] = None,
        supporting_evidence: Optional[List[str]] = None,
        counterevidence: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        required_experiment: Optional[str] = None,
        initial_confidence: float = 0.5,
        classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE,
    ) -> StrategicHypothesis:
        orig = origin_signals or []
        supp = supporting_evidence or []
        count = counterevidence or []
        assump = assumptions or []

        hypo_id = f"HYP-{hashlib.sha256(f'{tenant_id}:{statement}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"

        hypo = StrategicHypothesis(
            hypothesis_id=hypo_id,
            tenant_id=tenant_id,
            classification=classification,
            statement=statement,
            scope=scope,
            origin_signals=orig,
            supporting_evidence=supp,
            counterevidence=count,
            assumptions=assump,
            confidence=max(0.0, min(1.0, initial_confidence)),
            falsification_criteria=falsification_criteria,
            required_experiment=required_experiment,
            status=HypothesisStatus.PROPOSED,
        )

        # Compute provenance hash
        payload = {
            "hypothesis_id": hypo.hypothesis_id,
            "tenant_id": hypo.tenant_id,
            "statement": hypo.statement,
            "scope": hypo.scope,
            "falsification": hypo.falsification_criteria,
            "origin_signals": hypo.origin_signals,
        }
        hypo.provenance_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

        self._hypotheses[hypo_id] = hypo

        # Sync with Graph
        entity = GraphEntity(
            entity_id=hypo_id,
            entity_type=EntityType.HYPOTHESIS,
            tenant_id=tenant_id,
            classification=classification,
            name=f"Hypothesis: {statement[:40]}...",
            properties={
                "status": hypo.status.value,
                "confidence": hypo.confidence,
                "scope": hypo.scope,
                "falsification": hypo.falsification_criteria,
            },
            provenance_hashes=[hypo.provenance_hash],
        )
        self.graph.add_entity(entity)

        # Link origin signals
        for sig_id in orig:
            if self.graph.get_entity(sig_id):
                self.graph.add_relationship(
                    GraphRelationship(
                        relationship_id=f"REL-{sig_id}-{hypo_id}",
                        source_id=sig_id,
                        target_id=hypo_id,
                        relation_type=RelationType.INFORMS,
                        tenant_id=tenant_id,
                        classification=classification,
                        scope=scope,
                    )
                )

        return hypo

    def transition_status(
        self,
        hypothesis_id: str,
        new_status: HypothesisStatus,
        reason: str,
        evidence_ref: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> StrategicHypothesis:
        hypo = self._hypotheses.get(hypothesis_id)
        if not hypo:
            raise ValueError(f"Hypothesis '{hypothesis_id}' not found.")
        if tenant_id and hypo.tenant_id != tenant_id:
            raise ValueError(f"Access denied for tenant '{tenant_id}'.")

        hypo.status = new_status
        hypo.updated_at = datetime.now(timezone.utc)

        if evidence_ref:
            if new_status in (HypothesisStatus.SUPPORTED, HypothesisStatus.TESTABLE):
                if evidence_ref not in hypo.supporting_evidence:
                    hypo.supporting_evidence.append(evidence_ref)
            elif new_status in (HypothesisStatus.CONTRADICTED, HypothesisStatus.WEAKENED, HypothesisStatus.REJECTED):
                if evidence_ref not in hypo.counterevidence:
                    hypo.counterevidence.append(evidence_ref)

        # Invariant: Model confidence cannot arbitrarily promote without experimental support
        if new_status == HypothesisStatus.SUPPORTED and not hypo.supporting_evidence:
            hypo.status = HypothesisStatus.UNKNOWN

        return hypo

    def get_hypothesis(self, hypothesis_id: str, tenant_id: Optional[str] = None) -> Optional[StrategicHypothesis]:
        hypo = self._hypotheses.get(hypothesis_id)
        if not hypo:
            return None
        if tenant_id and hypo.classification == IntelligenceClassification.CLIENT_PRIVATE:
            if hypo.tenant_id != tenant_id:
                return None
        return hypo

    def list_hypotheses(self, tenant_id: str, status: Optional[HypothesisStatus] = None) -> List[StrategicHypothesis]:
        return [
            h for h in self._hypotheses.values()
            if (h.tenant_id == tenant_id or h.classification != IntelligenceClassification.CLIENT_PRIVATE)
            and (status is None or h.status == status)
            and h.is_active
        ]
