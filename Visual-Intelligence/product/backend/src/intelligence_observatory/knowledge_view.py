"""
Phase 25 Brand DNA and Aesthetic Knowledge Domain View.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class BrandKnowledgeItem:
    knowledge_id: str
    client_id: str
    domain: str # LUXURY_HAUTE_COUTURE, STREETWEAR, ACCESSORIES, D2C
    brand_tokens: List[str]
    restricted_terms: List[str]
    palette_hex: List[str]
    typography_rules: Dict[str, Any]
    last_updated: float
