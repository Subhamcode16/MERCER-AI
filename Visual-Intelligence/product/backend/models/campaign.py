from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid

# --- IDENTITY PHASE ---

class ConfidenceField(BaseModel):
    value: Any
    confidence: float

class ProductDNA(BaseModel):
    material: ConfidenceField
    weaving_technique: ConfidenceField
    primary_features: ConfidenceField
    raw_claims: Optional[List[Dict]] = []

class ReferenceDNA(BaseModel):
    lighting_preference: Optional[ConfidenceField] = None
    color_grading: Optional[ConfidenceField] = None
    composition_style: Optional[ConfidenceField] = None

class IdentityPhase(BaseModel):
    product_dna: Optional[ProductDNA] = None
    reference_dna: Optional[ReferenceDNA] = None

# --- PLANNING PHASE ---

class CampaignPlan(BaseModel):
    assets_requested: List[str] = ["hero_image", "product_closeup", "lifestyle"]
    dependency_graph: Dict[str, List[str]] = {
        "hero_image": [],
        "product_closeup": [],
        "lifestyle": [],
        "reel_storyboard": ["hero_image"]
    }

class PlanningPhase(BaseModel):
    creative_objective: str = "luxury_editorial"
    campaign_plan: CampaignPlan = Field(default_factory=CampaignPlan)

# --- EXECUTION PHASE ---

class AssetDNA(BaseModel):
    composition: Optional[str] = None
    lighting_emphasis: Optional[str] = None
    framing: Optional[str] = None

class AssetState(BaseModel):
    type: str
    status: str = "pending" # pending | generating | complete | rejected
    asset_dna: AssetDNA = Field(default_factory=AssetDNA)
    prompt: Optional[str] = None
    image_path: Optional[str] = None

class ExecutionPhase(BaseModel):
    campaign_state: Dict = {} # Global solver output
    asset_states: List[AssetState] = []

# --- EVALUATION PHASE ---

class Feedback(BaseModel):
    campaign_id: str
    asset_type: str
    action: str = "rejected"
    category: str
    severity: int
    reason: str
    desired_outcome: str
    suggested_solver_adjustment: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class EvaluationPhase(BaseModel):
    feedback_log: List[Feedback] = []
    consistency_scores: Dict[str, float] = {}
    approval_rate: Optional[float] = None
    edit_distance_minutes: Optional[int] = None

# --- CAMPAIGN ROOT ---

class Campaign(BaseModel):
    id: str = Field(default_factory=lambda: f"campaign_{uuid.uuid4().hex[:8]}")
    project_id: str
    product_id: str
    
    identity: IdentityPhase = Field(default_factory=IdentityPhase)
    planning: PlanningPhase = Field(default_factory=PlanningPhase)
    execution: ExecutionPhase = Field(default_factory=ExecutionPhase)
    evaluation: EvaluationPhase = Field(default_factory=EvaluationPhase)
    
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
