"""
Phase 14 Creative Direction Synthesizer
----------------------------------------
Synthesizes Brand DNA, Visual DNA, Trend Intelligence, Audience Intelligence,
and Campaign Objectives into inspectable, versioned Creative Direction Briefs.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import uuid

from src.creative_workforce.visual_dna import VisualDNAProfile
from src.creative_workforce.trend_observation import TrendObservation

@dataclass(frozen=True)
class CreativeDirectionBrief:
    """Versioned, inspectable creative direction brief."""
    brief_id: str
    campaign_title: str
    visual_dna_summary: Dict[str, Any]
    trend_insights: List[str]
    creative_pillars: List[str]
    art_direction_guidelines: Dict[str, str]
    version: str = "1.0.0"
    created_at: float = field(default_factory=time.time)

class CreativeDirectionSynthesizer:
    """Synthesizer combining multi-source creative inputs into unified direction briefs."""

    def synthesize_direction(
        self,
        campaign_title: str,
        visual_dna: VisualDNAProfile,
        trend_observations: Optional[List[TrendObservation]] = None,
        brand_tone: str = "Bold, Minimalist, High-Fashion",
    ) -> CreativeDirectionBrief:
        """Synthesizes inputs into a unified CreativeDirectionBrief."""
        brief_id = f"cdb-{uuid.uuid4().hex[:8]}"

        trend_insights = []
        if trend_observations:
            for obs in trend_observations:
                trend_insights.extend(obs.extracted_patterns)
        else:
            trend_insights = ["Monochrome editorial layouts", "Dynamic kinetic typography"]

        art_dir = {
            "tone": brand_tone,
            "palette": ", ".join(visual_dna.primary_colors),
            "typography": ", ".join(visual_dna.typography_styles),
            "composition": ", ".join(visual_dna.composition_rules),
        }

        pillars = [
            f"Visual DNA Alignment with {visual_dna.brand_or_concept}",
            "High-contrast editorial framing",
            "Targeted audience resonance",
        ]

        return CreativeDirectionBrief(
            brief_id=brief_id,
            campaign_title=campaign_title,
            visual_dna_summary={"colors": visual_dna.primary_colors, "keywords": visual_dna.aesthetic_keywords},
            trend_insights=trend_insights,
            creative_pillars=pillars,
            art_direction_guidelines=art_dir,
        )
