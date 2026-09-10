"""
External Intelligence Trust Model & Prompt Injection Defense.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import re
from pydantic import BaseModel, Field
from ..graph.models import IntelligenceClassification


class SourceReliability(str, Enum):
    HIGH_ACADEMIC_INDUSTRY = "HIGH_ACADEMIC_INDUSTRY"  # Peer reviewed, vetted market research (Gartner, McKinsey, etc.)
    MEDIUM_PLATFORM_DOCS = "MEDIUM_PLATFORM_DOCS"      # Meta/Google/TikTok official reports
    LOW_UNVERIFIED_WEB = "LOW_UNVERIFIED_WEB"          # Blog posts, web scrapes, raw forum threads
    UNTRUSTED_ADVERSARIAL = "UNTRUSTED_ADVERSARIAL"    # Synthetic, suspicious or injection-carrying text


class ExternalObservation(BaseModel):
    observation_id: str
    source_url: str
    source_name: str
    source_reliability: SourceReliability
    raw_content: str
    sanitized_content: str
    classification: IntelligenceClassification = IntelligenceClassification.PUBLIC_EXTERNAL
    corroboration_state: str = "UNCORROBORATED"
    freshness: float = 1.0
    detected_injection_patterns: List[str] = Field(default_factory=list)
    acquired_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_safe_for_synthesis: bool = True
