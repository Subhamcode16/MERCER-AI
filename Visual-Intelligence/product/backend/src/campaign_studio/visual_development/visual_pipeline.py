"""
Phase 27 Visual Development & Asset Pipeline.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone


class VisualAspectRatio(str, Enum):
    SQUARE = "1:1"
    PORTRAIT = "4:5"
    VERTICAL = "9:16"
    LANDSCAPE = "16:9"


@dataclass
class VisualDNAToken:
    token_id: str
    category: str  # "lighting", "lens", "texture", "color", "composition"
    token_name: str
    weight: float = 1.0
    locked: bool = True


@dataclass
class VisualAssetDraft:
    asset_id: str
    campaign_id: str
    direction_id: str
    title: str
    prompt_blueprint: str
    aspect_ratio: VisualAspectRatio
    channel: str  # "Instagram", "E-commerce Hero", "Digital OOH", "Lookbook"
    render_url: str
    visual_dna_tokens: List[str]
    model_provider: str = "Imagen-3-Photoreal"
    is_hero: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class VisualDevelopmentPipeline:
    """Compiles visual DNA, manages style locks, and orchestrates visual asset drafts."""

    def __init__(self):
        self._assets: Dict[str, List[VisualAssetDraft]] = {}  # campaign_id -> assets
        self._visual_dna: Dict[str, List[VisualDNAToken]] = {}  # campaign_id -> tokens

    def compile_visual_dna(self, campaign_id: str, direction_id: str, tokens: Optional[List[str]] = None) -> List[VisualDNAToken]:
        token_list = [
            VisualDNAToken(token_id=f"tok_{uuid.uuid4().hex[:6]}", category="lighting", token_name="raking_monolithic_late_sun", weight=1.0),
            VisualDNAToken(token_id=f"tok_{uuid.uuid4().hex[:6]}", category="lens", token_name="hasselblad_80mm_f2_8_creamy_falloff", weight=1.0),
            VisualDNAToken(token_id=f"tok_{uuid.uuid4().hex[:6]}", category="texture", token_name="dense_creased_wool_gabardine", weight=1.2),
            VisualDNAToken(token_id=f"tok_{uuid.uuid4().hex[:6]}", category="composition", token_name="negative_space_architectural_rule_of_thirds", weight=1.0),
        ]
        if tokens:
            for t in tokens:
                token_list.append(VisualDNAToken(token_id=f"tok_{uuid.uuid4().hex[:6]}", category="custom", token_name=t, weight=1.0))

        self._visual_dna[campaign_id] = token_list
        return token_list

    def generate_asset_drafts(self, campaign_id: str, direction_id: str, count: int = 4) -> List[VisualAssetDraft]:
        drafts = [
            VisualAssetDraft(
                asset_id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                direction_id=direction_id,
                title="Monolith Hero Centerpiece",
                prompt_blueprint="Editorial fashion photography of tailored coat on minimalist limestone plinth, raking sun",
                aspect_ratio=VisualAspectRatio.LANDSCAPE,
                channel="E-commerce Hero",
                render_url="https://assets.ilyren.internal/renders/hero_monolith_01.webp",
                visual_dna_tokens=["raking_monolithic_late_sun", "hasselblad_80mm", "dense_creased_wool"],
                is_hero=True,
            ),
            VisualAssetDraft(
                asset_id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                direction_id=direction_id,
                title="Garment Texture Close-Up",
                prompt_blueprint="Macro shot of hand-stitched lapel seam and matte metallic button in sharp studio lighting",
                aspect_ratio=VisualAspectRatio.SQUARE,
                channel="Instagram",
                render_url="https://assets.ilyren.internal/renders/macro_lapel_02.webp",
                visual_dna_tokens=["dense_creased_wool_gabardine", "sharp_macro_focus"],
                is_hero=False,
            ),
            VisualAssetDraft(
                asset_id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                direction_id=direction_id,
                title="Story Lookbook Sequence",
                prompt_blueprint="Full body movement shot walking across stark concrete pavilion, high-speed shutter",
                aspect_ratio=VisualAspectRatio.VERTICAL,
                channel="Digital OOH / Stories",
                render_url="https://assets.ilyren.internal/renders/story_walk_03.webp",
                visual_dna_tokens=["kinetic_stillness", "raking_monolithic_late_sun"],
                is_hero=False,
            ),
            VisualAssetDraft(
                asset_id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=campaign_id,
                direction_id=direction_id,
                title="Editorial Portrait Mood",
                prompt_blueprint="High fashion portrait gazing off-camera, dramatic architectural shadow diagonal",
                aspect_ratio=VisualAspectRatio.PORTRAIT,
                channel="Lookbook",
                render_url="https://assets.ilyren.internal/renders/lookbook_portrait_04.webp",
                visual_dna_tokens=["negative_space_architectural_rule_of_thirds", "raking_late_sun"],
                is_hero=False,
            ),
        ]
        self._assets[campaign_id] = drafts[:count]
        return self._assets[campaign_id]

    def list_assets(self, campaign_id: str) -> List[VisualAssetDraft]:
        return self._assets.get(campaign_id, [])

    def get_asset(self, campaign_id: str, asset_id: str) -> Optional[VisualAssetDraft]:
        assets = self._assets.get(campaign_id, [])
        return next((a for a in assets if a.asset_id == asset_id), None)
