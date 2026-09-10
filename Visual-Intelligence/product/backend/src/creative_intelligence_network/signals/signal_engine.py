"""
Strategic Signal Engine for synthesizing cross-campaign and governed evidence into bounded signals.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
import json
from .signal_types import StrategicSignal, SignalClass, EpistemicStatus, SignalLifecycle
from ..graph.models import IntelligenceClassification, GraphEntity, GraphRelationship, EntityType, RelationType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class StrategicSignalEngine:
    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._signals: Dict[str, StrategicSignal] = {}

    def emit_signal(
        self,
        tenant_id: str,
        signal_class: SignalClass,
        scope: str,
        observed_pattern: str,
        method: str,
        confidence: float,
        epistemic_status: EpistemicStatus,
        supporting_evidence: Optional[List[str]] = None,
        contradicting_evidence: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        unknowns: Optional[List[str]] = None,
        classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE,
        expires_at: Optional[datetime] = None,
    ) -> StrategicSignal:
        supporting = supporting_evidence or []
        contradicting = contradicting_evidence or []
        assump = assumptions or []
        unkn = unknowns or ["Unobserved counterfactual states remain unmeasured."]

        if isinstance(signal_class, str):
            signal_class = SignalClass(signal_class)
        if isinstance(epistemic_status, str):
            epistemic_status = EpistemicStatus(epistemic_status)

        # Core Invariant: Epistemic status must not claim experimental evidence without controlled experiment backing
        if epistemic_status == EpistemicStatus.EXPERIMENTAL_EVIDENCE and not any("exp" in ev.lower() for ev in supporting):
            epistemic_status = EpistemicStatus.OBSERVATIONAL_CORRELATION

        signal_id = f"SIG-{hashlib.sha256(f'{tenant_id}:{signal_class}:{observed_pattern}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"
        
        signal = StrategicSignal(
            signal_id=signal_id,
            tenant_id=tenant_id,
            classification=classification,
            signal_class=signal_class,
            lifecycle_state=SignalLifecycle.STRATEGIC_SIGNAL,
            scope=scope,
            observed_pattern=observed_pattern,
            supporting_evidence=supporting,
            contradicting_evidence=contradicting,
            method=method,
            confidence=max(0.0, min(1.0, confidence)),
            epistemic_status=epistemic_status,
            freshness=1.0,
            assumptions=assump,
            unknowns=unkn,
            generated_at=datetime.now(timezone.utc),
            expires_at=expires_at,
        )

        # Compute provenance hash
        payload = {
            "signal_id": signal.signal_id,
            "tenant_id": signal.tenant_id,
            "class": signal.signal_class.value,
            "scope": signal.scope,
            "pattern": signal.observed_pattern,
            "evidence": signal.supporting_evidence,
            "epistemic": signal.epistemic_status.value,
        }
        signal.provenance_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

        self._signals[signal_id] = signal

        # Sync with Organizational Intelligence Graph
        entity = GraphEntity(
            entity_id=signal_id,
            entity_type=EntityType.STRATEGIC_SIGNAL,
            tenant_id=tenant_id,
            classification=classification,
            name=f"{signal_class.value}: {scope}",
            properties={
                "signal_class": signal_class.value,
                "confidence": signal.confidence,
                "epistemic_status": signal.epistemic_status.value,
                "pattern": signal.observed_pattern,
            },
            provenance_hashes=[signal.provenance_hash],
        )
        self.graph.add_entity(entity)

        # Link supporting evidence entities if present
        for ev_id in supporting:
            if self.graph.get_entity(ev_id):
                self.graph.add_relationship(
                    GraphRelationship(
                        relationship_id=f"REL-{signal_id}-{ev_id}",
                        source_id=ev_id,
                        target_id=signal_id,
                        relation_type=RelationType.SUPPORTS,
                        tenant_id=tenant_id,
                        classification=classification,
                        scope=scope,
                        evidence_refs=[ev_id],
                    )
                )

        return signal

    def get_signal(self, signal_id: str, tenant_id: Optional[str] = None) -> Optional[StrategicSignal]:
        signal = self._signals.get(signal_id)
        if not signal:
            return None
        if tenant_id and signal.classification == IntelligenceClassification.CLIENT_PRIVATE:
            if signal.tenant_id != tenant_id:
                return None
        return signal

    def list_signals(self, tenant_id: str, signal_class: Optional[SignalClass] = None) -> List[StrategicSignal]:
        return [
            s for s in self._signals.values()
            if (s.tenant_id == tenant_id or s.classification != IntelligenceClassification.CLIENT_PRIVATE)
            and (signal_class is None or s.signal_class == signal_class)
            and s.is_active
        ]
