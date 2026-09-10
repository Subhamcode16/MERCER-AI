"""
Phase 26 Typed Context Resolution.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


class ContextCategory(str, Enum):
    BUSINESS = "BUSINESS"
    BRAND = "BRAND"
    AUDIENCE = "AUDIENCE"
    CAMPAIGN = "CAMPAIGN"
    PRODUCT = "PRODUCT"
    DOMAIN = "DOMAIN"
    VISUAL_DNA = "VISUAL_DNA"
    KNOWLEDGE = "KNOWLEDGE"
    TASK = "TASK"
    EVIDENCE = "EVIDENCE"
    DECISIONS = "DECISIONS"
    CONSTRAINTS = "CONSTRAINTS"


class EpistemicType(str, Enum):
    FACT = "FACT"
    INFERENCE = "INFERENCE"
    RECOMMENDATION = "RECOMMENDATION"
    HYPOTHESIS = "HYPOTHESIS"
    UNKNOWN = "UNKNOWN"


@dataclass
class ContextItem:
    item_id: str
    category: ContextCategory
    epistemic_type: EpistemicType
    content: Any
    provenance: str
    confidence: float = 1.0


class ContextResolver:
    """Assembles typed context packets for workers while maintaining epistemic classification."""

    @staticmethod
    def assemble_campaign_context(
        tenant_id: str,
        client_id: str,
        campaign_id: str,
        raw_inputs: Dict[str, Any],
    ) -> List[ContextItem]:
        items = []

        if "brand_guidelines" in raw_inputs:
            items.append(
                ContextItem(
                    item_id="ctx_brand",
                    category=ContextCategory.BRAND,
                    epistemic_type=EpistemicType.FACT,
                    content=raw_inputs["brand_guidelines"],
                    provenance="CLIENT_ONBOARDING_DOCS",
                )
            )

        if "visual_dna_tokens" in raw_inputs:
            items.append(
                ContextItem(
                    item_id="ctx_vdna",
                    category=ContextCategory.VISUAL_DNA,
                    epistemic_type=EpistemicType.FACT,
                    content=raw_inputs["visual_dna_tokens"],
                    provenance="VISUAL_DNA_REGISTRY",
                )
            )

        if "trend_hypothesis" in raw_inputs:
            items.append(
                ContextItem(
                    item_id="ctx_trend",
                    category=ContextCategory.DOMAIN,
                    epistemic_type=EpistemicType.HYPOTHESIS,
                    content=raw_inputs["trend_hypothesis"],
                    provenance="TREND_RESEARCHER_WORKER",
                    confidence=0.75,
                )
            )

        return items
