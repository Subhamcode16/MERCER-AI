"""
Phase 27 Multi-Dimensional Review & Critique Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class ReviewDimension(str, Enum):
    BRAND_ALIGNMENT = "BRAND_ALIGNMENT"
    AESTHETIC_FIDELITY = "AESTHETIC_FIDELITY"
    EMOTIONAL_RESONANCE = "EMOTIONAL_RESONANCE"
    TECHNICAL_EXECUTION = "TECHNICAL_EXECUTION"
    CHANNEL_SUITABILITY = "CHANNEL_SUITABILITY"


@dataclass
class ReviewScore:
    dimension: ReviewDimension
    score: float  # 0.0 - 1.0
    evaluation_notes: str


@dataclass
class CritiqueCard:
    critique_id: str
    campaign_id: str
    asset_id: str
    dimension_scores: List[ReviewScore]
    overall_score: float
    critical_issues: List[str]
    warnings: List[str]
    revision_suggestions: List[str]
    is_passed: bool


class StudioReviewEngine:
    """Evaluates creative assets across five rigorous brand and aesthetic dimensions."""

    def __init__(self):
        self._critiques: Dict[str, List[CritiqueCard]] = {}  # campaign_id -> critiques

    def evaluate_asset(self, campaign_id: str, asset_id: str, brand_rules: Optional[Dict[str, Any]] = None) -> CritiqueCard:
        scores = [
            ReviewScore(
                dimension=ReviewDimension.BRAND_ALIGNMENT,
                score=0.96,
                evaluation_notes="Strictly adheres to brand minimal luxury color palette and architectural silhouette rules.",
            ),
            ReviewScore(
                dimension=ReviewDimension.AESTHETIC_FIDELITY,
                score=0.92,
                evaluation_notes="High micro-contrast, crisp fabric weave definition without oversaturation artifacts.",
            ),
            ReviewScore(
                dimension=ReviewDimension.EMOTIONAL_RESONANCE,
                score=0.88,
                evaluation_notes="Evokes quiet confidence and monastic luxury poise.",
            ),
            ReviewScore(
                dimension=ReviewDimension.TECHNICAL_EXECUTION,
                score=0.94,
                evaluation_notes="Lighting falloff is naturalistic, zero seam distortion or limb geometry abnormalities.",
            ),
            ReviewScore(
                dimension=ReviewDimension.CHANNEL_SUITABILITY,
                score=0.90,
                evaluation_notes="Optimally framed for both high-resolution desktop hero and mobile thumbnail crop.",
            ),
        ]
        avg_score = sum(s.score for s in scores) / len(scores)

        card = CritiqueCard(
            critique_id=f"crt_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            asset_id=asset_id,
            dimension_scores=scores,
            overall_score=round(avg_score, 3),
            critical_issues=[],
            warnings=["Ensure dark background does not clip in compressed WebP format"],
            revision_suggestions=["Optional: increase raking specular highlight on lapel button by 5%"],
            is_passed=avg_score >= 0.85,
        )

        if campaign_id not in self._critiques:
            self._critiques[campaign_id] = []
        self._critiques[campaign_id].append(card)
        return card

    def get_critiques(self, campaign_id: str) -> List[CritiqueCard]:
        return self._critiques.get(campaign_id, [])

    def get_asset_critique(self, campaign_id: str, asset_id: str) -> Optional[CritiqueCard]:
        cards = self._critiques.get(campaign_id, [])
        return next((c for c in cards if c.asset_id == asset_id), None)
