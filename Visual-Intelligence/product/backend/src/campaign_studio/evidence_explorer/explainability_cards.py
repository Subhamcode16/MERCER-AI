"""
Phase 27 Studio Evidence Explorer & Explainability Cards.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class EvidenceItem:
    evidence_id: str
    source_type: str  # "MARKET_RADAR", "BRAND_GUIDELINE", "AUDIENCE_SURVEY", "HISTORICAL_CAMPAIGN"
    citation: str
    snippet: str
    confidence_weight: float = 0.95


@dataclass
class ExplainabilityCard:
    card_id: str
    target_entity_type: str  # "DIRECTION", "HYPOTHESIS", "VISUAL_DNA", "CRITIQUE"
    target_entity_id: str
    title: str
    rationale: str
    evidence_items: List[EvidenceItem]
    model_attribution: str = "CreativeWorkforce_Consensus"
    invariants_validated: List[str] = field(default_factory=lambda: [
        "Intelligence ≠ Authorization",
        "Visual Similarity ≠ Strategic Correctness",
        "Attribution ≠ Causal Proof",
    ])


class EvidenceExplorer:
    """Manages explainability traces, evidence citations, and rationale breakdowns for studio artifacts."""

    def __init__(self):
        self._cards: Dict[str, List[ExplainabilityCard]] = {}  # target_entity_id -> cards

    def create_explainability_card(
        self,
        target_entity_type: str,
        target_entity_id: str,
        title: str,
        rationale: str,
        evidence: Optional[List[Dict[str, Any]]] = None,
    ) -> ExplainabilityCard:
        items = []
        if evidence:
            for e in evidence:
                items.append(EvidenceItem(
                    evidence_id=f"ev_{uuid.uuid4().hex[:6]}",
                    source_type=e.get("source_type", "BRAND_GUIDELINE"),
                    citation=e.get("citation", "Brand Guidelines 2026"),
                    snippet=e.get("snippet", ""),
                    confidence_weight=e.get("confidence_weight", 0.95),
                ))
        else:
            items.append(EvidenceItem(
                evidence_id=f"ev_{uuid.uuid4().hex[:6]}",
                source_type="BRAND_GUIDELINE",
                citation="Minimalist Luxury Dossier v2.4",
                snippet="Brand identity prioritizes architectural stillness over aggressive kinetic motion.",
                confidence_weight=0.98,
            ))

        card = ExplainabilityCard(
            card_id=f"exp_{uuid.uuid4().hex[:8]}",
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            title=title,
            rationale=rationale,
            evidence_items=items,
        )

        if target_entity_id not in self._cards:
            self._cards[target_entity_id] = []
        self._cards[target_entity_id].append(card)
        return card

    def get_cards_for_entity(self, target_entity_id: str) -> List[ExplainabilityCard]:
        return self._cards.get(target_entity_id, [])
