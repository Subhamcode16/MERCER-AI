"""
Phase 27 Adaptive Epistemic Discovery Engine.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


class DiscoveryEpistemicState(str, Enum):
    KNOWN = "KNOWN"
    INFERRED = "INFERRED"
    MISSING = "MISSING"
    CONFLICTING = "CONFLICTING"
    UNKNOWN = "UNKNOWN"


@dataclass
class DiscoveryItem:
    item_id: str
    dimension: str  # e.g., "audience", "budget", "brand_values", "primary_channel"
    state: DiscoveryEpistemicState
    value: Any = None
    provenance: str = "CLIENT_INPUT"
    confidence: float = 1.0


@dataclass
class ConsequentialQuestion:
    question_id: str
    dimension: str
    prompt: str
    options: List[str] = field(default_factory=list)
    impact_description: str = ""


class AdaptiveDiscoveryEngine:
    """Dynamically analyzes campaign discovery state, tracks knowledge gaps, and asks consequential questions."""

    def __init__(self):
        self._discovery_items: Dict[str, Dict[str, DiscoveryItem]] = {}  # campaign_id -> {dimension: item}
        self._pending_questions: Dict[str, List[ConsequentialQuestion]] = {}

    def analyze_intake(self, campaign_id: str, raw_inputs: Dict[str, Any]) -> List[DiscoveryItem]:
        items: Dict[str, DiscoveryItem] = {}
        questions: List[ConsequentialQuestion] = []

        # 1. Target Audience
        if "target_audience" in raw_inputs:
            items["target_audience"] = DiscoveryItem(
                item_id=f"disc_{uuid.uuid4().hex[:8]}",
                dimension="target_audience",
                state=DiscoveryEpistemicState.KNOWN,
                value=raw_inputs["target_audience"],
            )
        else:
            items["target_audience"] = DiscoveryItem(
                item_id=f"disc_{uuid.uuid4().hex[:8]}",
                dimension="target_audience",
                state=DiscoveryEpistemicState.MISSING,
            )
            questions.append(
                ConsequentialQuestion(
                    question_id=f"q_{uuid.uuid4().hex[:8]}",
                    dimension="target_audience",
                    prompt="Who is the primary demographic target for this collection launch?",
                    options=["Gen-Z Streetwear Avant-Garde", "Affluent Luxury Minimalists", "Corporate Creative Professionals"],
                    impact_description="Determines narrative tone and visual styling direction.",
                )
            )

        # 2. Seasonality / Occasion
        if "season" in raw_inputs:
            items["season"] = DiscoveryItem(
                item_id=f"disc_{uuid.uuid4().hex[:8]}",
                dimension="season",
                state=DiscoveryEpistemicState.KNOWN,
                value=raw_inputs["season"],
            )
        else:
            items["season"] = DiscoveryItem(
                item_id=f"disc_{uuid.uuid4().hex[:8]}",
                dimension="season",
                state=DiscoveryEpistemicState.INFERRED,
                value="Autumn/Winter 2026",
                provenance="INFERRED_FROM_CALENDAR",
                confidence=0.85,
            )

        # 3. Visual Tone Constraints
        if "visual_tone" in raw_inputs:
            items["visual_tone"] = DiscoveryItem(
                item_id=f"disc_{uuid.uuid4().hex[:8]}",
                dimension="visual_tone",
                state=DiscoveryEpistemicState.KNOWN,
                value=raw_inputs["visual_tone"],
            )
        else:
            items["visual_tone"] = DiscoveryItem(
                item_id=f"disc_{uuid.uuid4().hex[:8]}",
                dimension="visual_tone",
                state=DiscoveryEpistemicState.MISSING,
            )
            questions.append(
                ConsequentialQuestion(
                    question_id=f"q_{uuid.uuid4().hex[:8]}",
                    dimension="visual_tone",
                    prompt="What is the intended lighting and visual atmosphere?",
                    options=["Architectural High-Contrast Editorial", "Warm Sun-Drenched Naturalism", "Futuristic Studio Cyan Noir"],
                    impact_description="Guides prompt compilation and visual DNA token weights.",
                )
            )

        self._discovery_items[campaign_id] = items
        self._pending_questions[campaign_id] = questions
        return list(items.values())

    def get_discovery_items(self, campaign_id: str) -> List[DiscoveryItem]:
        return list(self._discovery_items.get(campaign_id, {}).values())

    def get_pending_questions(self, campaign_id: str) -> List[ConsequentialQuestion]:
        return self._pending_questions.get(campaign_id, [])

    def answer_question(self, campaign_id: str, question_id: str, answer: str) -> DiscoveryItem:
        questions = self._pending_questions.get(campaign_id, [])
        target_q = next((q for q in questions if q.question_id == question_id), None)
        if not target_q:
            raise KeyError(f"Question '{question_id}' not found for campaign '{campaign_id}'")

        item = DiscoveryItem(
            item_id=f"disc_{uuid.uuid4().hex[:8]}",
            dimension=target_q.dimension,
            state=DiscoveryEpistemicState.KNOWN,
            value=answer,
            provenance="HUMAN_DISCOVERY_RESPONSE",
            confidence=1.0,
        )
        if campaign_id not in self._discovery_items:
            self._discovery_items[campaign_id] = {}
        self._discovery_items[campaign_id][target_q.dimension] = item

        # Remove answered question
        self._pending_questions[campaign_id] = [q for q in questions if q.question_id != question_id]
        return item
