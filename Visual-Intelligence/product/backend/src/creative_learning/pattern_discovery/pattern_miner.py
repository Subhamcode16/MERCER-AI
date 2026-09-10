"""
Phase 28 Cross-Campaign Creative Pattern Discovery.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone

from src.creative_learning.hypotheses.hypothesis_store import HypothesisScope


@dataclass
class DiscoveredPattern:
    pattern_id: str
    pattern_name: str
    category: str  # "COMPOSITION", "COLOR_HARMONY", "NARRATIVE_HOOK", "LIGHTING_ATMOSPHERE"
    scope: HypothesisScope
    client_id: Optional[str]
    brand_id: Optional[str]
    description: str
    sample_campaign_ids: List[str]
    observed_performance_lift: float
    confidence: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class CreativePatternMiner:
    """Mines cross-campaign trends and visual patterns with strict scope boundaries."""

    def __init__(self):
        self._patterns: Dict[str, DiscoveredPattern] = {}

    def discover_pattern(
        self,
        pattern_name: str,
        category: str,
        scope: HypothesisScope,
        description: str,
        sample_campaign_ids: List[str],
        observed_performance_lift: float,
        confidence: float = 0.89,
        client_id: Optional[str] = None,
        brand_id: Optional[str] = None,
    ) -> DiscoveredPattern:
        # Cross-client privacy guard
        if scope == HypothesisScope.GLOBAL and client_id:
            raise PermissionError("Cannot declare GLOBAL scope pattern with private client linkage.")

        pat = DiscoveredPattern(
            pattern_id=f"pat_{uuid.uuid4().hex[:8]}",
            pattern_name=pattern_name,
            category=category,
            scope=scope,
            client_id=client_id,
            brand_id=brand_id,
            description=description,
            sample_campaign_ids=sample_campaign_ids,
            observed_performance_lift=observed_performance_lift,
            confidence=confidence,
        )
        self._patterns[pat.pattern_id] = pat
        return pat

    def list_patterns(self, scope: Optional[HypothesisScope] = None, brand_id: Optional[str] = None) -> List[DiscoveredPattern]:
        patterns = list(self._patterns.values())
        if scope:
            patterns = [p for p in patterns if p.scope == scope]
        if brand_id:
            patterns = [p for p in patterns if p.brand_id == brand_id or p.scope in {HypothesisScope.GLOBAL, HypothesisScope.DOMAIN}]
        return patterns
