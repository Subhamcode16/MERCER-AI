from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid

# --- Phase 1: Database Foundation & Knowledge Models ---

class WorkspaceSettings(BaseModel):
    default_domain: str = "Human Expression"
    use_24_hour_time: bool = True

class Workspace(BaseModel):
    id: str = Field(default_factory=lambda: f"workspace_{uuid.uuid4().hex[:8]}")
    name: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    owner_id: str
    settings: WorkspaceSettings = Field(default_factory=WorkspaceSettings)

class TypographyRules(BaseModel):
    pairings: List[Dict[str, str]] = []
    casing_rule: str = "Sentence case"

class ColorPaletteRestrictions(BaseModel):
    primary: List[str] = []
    secondary: List[str] = []
    accents: List[str] = []

class VisualStyleGuidelines(BaseModel):
    typography: TypographyRules = Field(default_factory=TypographyRules)
    color_palette: ColorPaletteRestrictions = Field(default_factory=ColorPaletteRestrictions)
    exclusions: List[str] = []
    composition_preferences: List[str] = []

class Brand(BaseModel):
    id: str = Field(default_factory=lambda: f"brand_{uuid.uuid4().hex[:8]}")
    workspace_id: str
    name: str
    aesthetic_dna: List[str] = []
    guidelines: VisualStyleGuidelines = Field(default_factory=VisualStyleGuidelines)
    brand_memory_core: List[str] = []
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ProductVisualAttributes(BaseModel):
    silhouette_extracted: bool = False
    detected_materials: List[Dict[str, Any]] = []
    color_palette: List[str] = []
    texture_density: Optional[str] = None
    reflectance_matrix: Optional[Dict[str, float]] = None
    draping_weight_index: Optional[str] = None

class Provenance(BaseModel):
    extracted_by: str = "System"
    confidence: float = 0.0
    is_verified: bool = False
    verified_by: Optional[str] = None
    verified_at: Optional[str] = None

class Product(BaseModel):
    id: str = Field(default_factory=lambda: f"product_{uuid.uuid4().hex[:8]}")
    brand_id: str
    name: str
    domain: str
    images: List[Dict[str, Any]] = []
    attributes: ProductVisualAttributes = Field(default_factory=ProductVisualAttributes)
    provenance: Provenance = Field(default_factory=Provenance)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class KnowledgeClaim(BaseModel):
    """
    Canonical Knowledge Claim defined by LAW-001.
    """
    id: str = Field(default_factory=lambda: f"kc_{uuid.uuid4().hex[:8]}")
    subject: str
    predicate: str
    object_value: Any
    evidence: str
    source: str
    confidence: float
    context: str
    status: str = "Valid"
    version: int = 1
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class GraphEdge(BaseModel):
    """
    Ontology Graph Relations (ARC-001)
    """
    source_id: str
    target_id: str
    edge_type: str # OWNED_BY, MEMBER_OF, PROMOTED_IN, AESTHETIC_ALIGNED
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
