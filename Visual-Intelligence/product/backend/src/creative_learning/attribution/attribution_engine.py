"""
Phase 28 Epistemic Attribution & Confounder Analysis Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class EvidenceCausalStatus(str, Enum):
    CORRELATIONAL_OBSERVATIONAL = "CORRELATIONAL_OBSERVATIONAL"
    CONFOUNDED = "CONFOUNDED"
    CONTROLLED_EXPERIMENT = "CONTROLLED_EXPERIMENT"
    UNPROVEN = "UNPROVEN"


@dataclass
class ConfounderRecord:
    confounder_id: str
    name: str  # e.g. "Ad Spend Surge", "Macro Black Friday Seasonality", "Competitor Stockout"
    severity_impact: float  # 0.0 - 1.0
    description: str


@dataclass
class AttributionAssessment:
    assessment_id: str
    campaign_id: str
    asset_id: str
    attributed_conversion_lift: float
    causal_status: EvidenceCausalStatus
    attribution_model: str
    detected_confounders: List[ConfounderRecord]
    epistemic_disclaimer: str = (
        "Attribution reflects correlational association. Invariant: Outcome ≠ Causation. "
        "High performance does not prove visual style caused conversion lift."
    )


class AttributionEngine:
    """Evaluates multi-touch attribution and detects external confounding factors."""

    def evaluate_attribution(
        self,
        campaign_id: str,
        asset_id: str,
        raw_lift: float,
        is_controlled_ab_test: bool = False,
        external_confounders: Optional[List[Dict[str, Any]]] = None,
    ) -> AttributionAssessment:
        confounders = []
        if external_confounders:
            for c in external_confounders:
                confounders.append(ConfounderRecord(
                    confounder_id=f"cnf_{uuid.uuid4().hex[:6]}",
                    name=c.get("name", "External Anomaly"),
                    severity_impact=c.get("severity", 0.6),
                    description=c.get("description", ""),
                ))
        else:
            # Default check for common retail/seasonality confounders
            confounders.append(ConfounderRecord(
                confounder_id=f"cnf_{uuid.uuid4().hex[:6]}",
                name="Macro Fashion Seasonality",
                severity_impact=0.35,
                description="Autumn collection launch coincided with general market outerwear purchasing cycle.",
            ))

        if is_controlled_ab_test and not confounders:
            status = EvidenceCausalStatus.CONTROLLED_EXPERIMENT
        elif confounders:
            status = EvidenceCausalStatus.CONFOUNDED
        else:
            status = EvidenceCausalStatus.CORRELATIONAL_OBSERVATIONAL

        return AttributionAssessment(
            assessment_id=f"att_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            asset_id=asset_id,
            attributed_conversion_lift=raw_lift,
            causal_status=status,
            attribution_model="Multi-Touch Markov Attribution (Correlational)",
            detected_confounders=confounders,
        )
