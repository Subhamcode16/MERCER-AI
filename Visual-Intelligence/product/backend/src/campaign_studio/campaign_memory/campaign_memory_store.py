"""
Phase 27 Campaign Memory & Brand Evolution Store.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class BrandMemoryEntry:
    entry_id: str
    client_id: str
    brand_id: str
    category: str  # "visual_preference", "audience_resonance", "postmortem_learning", "tone_guardrail"
    title: str
    content: str
    confidence: float = 0.95


class CampaignMemoryStore:
    """Stores brand-specific historical intelligence, winning visual tokens, and past campaign learnings."""

    def __init__(self):
        self._memory: Dict[str, List[BrandMemoryEntry]] = {}  # brand_id -> entries

    def add_memory(self, client_id: str, brand_id: str, category: str, title: str, content: str) -> BrandMemoryEntry:
        entry = BrandMemoryEntry(
            entry_id=f"mem_{uuid.uuid4().hex[:8]}",
            client_id=client_id,
            brand_id=brand_id,
            category=category,
            title=title,
            content=content,
        )
        if brand_id not in self._memory:
            self._memory[brand_id] = []
        self._memory[brand_id].append(entry)
        return entry

    def get_brand_memories(self, brand_id: str, category: Optional[str] = None) -> List[BrandMemoryEntry]:
        entries = self._memory.get(brand_id, [])
        if category:
            return [e for e in entries if e.category == category]
        return entries
