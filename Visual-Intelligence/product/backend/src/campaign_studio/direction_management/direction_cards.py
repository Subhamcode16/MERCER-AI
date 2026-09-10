"""
Phase 27 Creative Direction Management & Comparative Cards.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class CreativeDirectionCard:
    direction_id: str
    campaign_id: str
    title: str
    core_idea: str
    narrative_angle: str
    target_tension: str
    visual_tokens: List[str]
    palette_motifs: List[str]
    confidence_score: float
    feasibility_score: float
    trade_offs: List[str]
    risks: List[str]
    is_selected: bool = False
    refinement_history: List[str] = field(default_factory=list)


class DirectionManager:
    """Manages creative direction generation, comparative analysis, branching, and human selection."""

    def __init__(self):
        self._directions: Dict[str, List[CreativeDirectionCard]] = {}  # campaign_id -> list of cards

    def generate_candidate_directions(self, campaign_id: str, hypothesis_list: Optional[List[Dict[str, Any]]] = None) -> List[CreativeDirectionCard]:
        d1 = CreativeDirectionCard(
            direction_id=f"dir_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            title="Monolithic Elegance",
            core_idea="Monumental architecture intersecting minimalist high-tailoring silhouette.",
            narrative_angle="Sculptural stillness in an overstimulated digital universe.",
            target_tension="High-performance utility vs. Haute Couture posture",
            visual_tokens=["raw_limestone", "razor_creased_wool", "raking_late_sun", "sharp_silhouette"],
            palette_motifs=["#1A1A1A", "#E5E0D8", "#8A7D70", "#D4AF37"],
            confidence_score=0.94,
            feasibility_score=0.91,
            trade_offs=["Requires austere location scout", "Strict lighting control"],
            risks=["May read overly severe if models lack dynamic micro-gesture"],
            is_selected=False,
        )

        d2 = CreativeDirectionCard(
            direction_id=f"dir_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            title="Ethereal Kinetics",
            core_idea="Fluid silk garments suspended in airborne motion with high-speed strobe clarity.",
            narrative_angle="Weightless velocity capturing the ephemeral transition between seasons.",
            target_tension="Delicate sensory intimacy vs. commanding presence",
            visual_tokens=["billowing_organza", "strobe_crystallization", "deep_chroma_shadows", "kinetic_blur"],
            palette_motifs=["#0C1017", "#4A6FA5", "#E8EFF5", "#FF6B6B"],
            confidence_score=0.89,
            feasibility_score=0.86,
            trade_offs=["Complex fabric physics and motion capture prompt constraints"],
            risks=["Potential rendering artifacts on semi-transparent sheer textures"],
            is_selected=False,
        )

        d3 = CreativeDirectionCard(
            direction_id=f"dir_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            title="Neo-Archive Vanguard",
            core_idea="Deconstructed 90s vintage atelier meets cybernetic metallic micro-accents.",
            narrative_angle="Honoring historical tailoring while rewriting the contemporary silhouette.",
            target_tension="Archival nostalgia vs. hyper-futuristic relevance",
            visual_tokens=["heavy_gabardine", "anodized_titanium_hardware", "low_angle_editorial", "35mm_grain"],
            palette_motifs=["#22252A", "#707A8A", "#B8860B", "#F5F5F7"],
            confidence_score=0.91,
            feasibility_score=0.95,
            trade_offs=["Niche aesthetic appeal for mainstream luxury audiences"],
            risks=["Could veer into retro pastiche without disciplined curation"],
            is_selected=False,
        )

        cards = [d1, d2, d3]
        self._directions[campaign_id] = cards
        return cards

    def list_directions(self, campaign_id: str) -> List[CreativeDirectionCard]:
        return self._directions.get(campaign_id, [])

    def get_direction(self, campaign_id: str, direction_id: str) -> Optional[CreativeDirectionCard]:
        cards = self._directions.get(campaign_id, [])
        return next((c for c in cards if c.direction_id == direction_id), None)

    def select_direction(self, campaign_id: str, direction_id: str) -> CreativeDirectionCard:
        cards = self._directions.get(campaign_id, [])
        target = next((c for c in cards if c.direction_id == direction_id), None)
        if not target:
            raise KeyError(f"Direction '{direction_id}' not found for campaign '{campaign_id}'")

        for c in cards:
            c.is_selected = (c.direction_id == direction_id)
        return target

    def refine_direction(self, campaign_id: str, direction_id: str, instruction: str) -> CreativeDirectionCard:
        target = self.get_direction(campaign_id, direction_id)
        if not target:
            raise KeyError(f"Direction '{direction_id}' not found for campaign '{campaign_id}'")

        target.refinement_history.append(instruction)
        target.core_idea = f"{target.core_idea} [Refined: {instruction}]"
        return target
