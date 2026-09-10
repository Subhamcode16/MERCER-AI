"""
Phase 14 Visual DNA Intelligence Manager
-----------------------------------------
Extracts, structures, and compares Visual DNA dimensions (Typography, Color, Composition,
Grid, Photography, Texture, Editorial Rhythm, Art Direction).
Produces visual alignment recommendations without security side effects.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import uuid

@dataclass(frozen=True)
class VisualDNAProfile:
    """Structured representation of visual design DNA."""
    profile_id: str
    brand_or_concept: str
    primary_colors: List[str]
    typography_styles: List[str]
    composition_rules: List[str]
    aesthetic_keywords: List[str]
    texture_elements: List[str]

class VisualDNAManager:
    """Manager extracting and comparing visual DNA profiles."""

    def __init__(self):
        self._profiles: Dict[str, VisualDNAProfile] = {}

    def extract_visual_dna(
        self,
        brand_or_concept: str,
        primary_colors: List[str],
        typography_styles: List[str],
        composition_rules: Optional[List[str]] = None,
        aesthetic_keywords: Optional[List[str]] = None,
    ) -> VisualDNAProfile:
        """Extracts and stores a Visual DNA profile."""
        profile_id = f"vdna-{uuid.uuid4().hex[:8]}"

        profile = VisualDNAProfile(
            profile_id=profile_id,
            brand_or_concept=brand_or_concept,
            primary_colors=primary_colors,
            typography_styles=typography_styles,
            composition_rules=composition_rules or ["asymmetric_grid", "bold_white_space"],
            aesthetic_keywords=aesthetic_keywords or ["minimalist", "high_contrast", "editorial"],
            texture_elements=["film_grain", "matte_paper"],
        )
        self._profiles[profile_id] = profile
        return profile

    def compare_dna(self, profile_a: VisualDNAProfile, profile_b: VisualDNAProfile) -> Dict[str, Any]:
        """Compares two Visual DNA profiles and returns affinity metrics."""
        common_colors = set(profile_a.primary_colors).intersection(set(profile_b.primary_colors))
        common_type = set(profile_a.typography_styles).intersection(set(profile_b.typography_styles))
        common_keywords = set(profile_a.aesthetic_keywords).intersection(set(profile_b.aesthetic_keywords))

        affinity_score = (len(common_colors) + len(common_type) + len(common_keywords)) / 10.0
        affinity_score = min(1.0, max(0.2, affinity_score))

        return {
            "profile_a": profile_a.profile_id,
            "profile_b": profile_b.profile_id,
            "affinity_score": affinity_score,
            "shared_elements": list(common_colors.union(common_type).union(common_keywords)),
        }
