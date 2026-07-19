from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from models.campaign import Campaign, IdentityPhase, PlanningPhase, AssetState, AssetDNA
from adapters.vision_adapter import VisionAdapter
from storage.local_store import LocalStore

app = FastAPI(title="Visual Intelligence Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = LocalStore()
vision_adapter = VisionAdapter()

# --- Request Models ---

class AnalyzeRequest(BaseModel):
    image_url: str
    provider: str = "gemini"
    
class AnalyzeReferenceRequest(BaseModel):
    image_urls: List[str]
    provider: str = "gemini"

class CreateCampaignRequest(BaseModel):
    project_id: str
    product_id: str
    creative_objective: str
    assets_requested: List[str]

class FeedbackRequest(BaseModel):
    category: str
    severity: int
    desired_outcome: str

# --- API Endpoints ---

@app.post("/api/analyze/product")
async def analyze_product(request: AnalyzeRequest):
    """Extracts Product DNA from a product image."""
    adapter = VisionAdapter(provider=request.provider)
    dna = adapter.analyze_product(request.image_url)
    return {"status": "success", "product_dna": dna.model_dump()}

@app.post("/api/analyze/reference")
async def analyze_reference(request: AnalyzeReferenceRequest):
    """Extracts Reference DNA from moodboards or past campaigns."""
    adapter = VisionAdapter(provider=request.provider)
    dna = adapter.analyze_reference(request.image_urls)
    return {"status": "success", "reference_dna": dna.model_dump()}

@app.post("/api/campaign/create", response_model=Campaign)
async def create_campaign(request: CreateCampaignRequest):
    """Initializes a new Campaign in the Planning phase."""
    campaign = Campaign(
        project_id=request.project_id,
        product_id=request.product_id
    )
    
    # Setup planning phase
    campaign.planning.creative_objective = request.creative_objective
    campaign.planning.campaign_plan.assets_requested = request.assets_requested
    
    # Initialize asset states based on plan
    for asset_type in request.assets_requested:
        asset_state = AssetState(
            type=asset_type,
            status="pending",
            asset_dna=AssetDNA()
        )
        campaign.execution.asset_states.append(asset_state)
        
    store.save_campaign(campaign)
    return campaign

@app.get("/api/campaign/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    """Retrieves a campaign's full lifecycle state."""
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.post("/api/campaign/{campaign_id}/generate")
async def generate_assets(campaign_id: str, background_tasks: BackgroundTasks):
    """Triggers generation for pending assets, respecting the dependency graph."""
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    # Mocking generation kickoff
    def _mock_generate(c: Campaign):
        # In reality, this talks to orchestrator.py
        for asset in c.execution.asset_states:
            if asset.status == "pending":
                asset.status = "generating"
        store.save_campaign(c)
        
    background_tasks.add_task(_mock_generate, campaign)
    return {"status": "generation_started", "campaign_id": campaign_id}

@app.post("/api/campaign/{campaign_id}/assets/{asset_type}/feedback")
async def submit_feedback(campaign_id: str, asset_type: str, request: FeedbackRequest):
    """Logs structured feedback for a rejected asset and flags it for regeneration."""
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    # Find the asset
    asset = next((a for a in campaign.execution.asset_states if a.type == asset_type), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    # In reality, this would store the feedback log to a DB table
    # We will log it to the local store for now
    import json
    import os
    feedback_file = os.path.join(store.data_dir, "feedback_log.json")
    
    log_entry = {
        "campaign_id": campaign_id,
        "asset_type": asset_type,
        "feedback": request.model_dump()
    }
    
    # Append to log
    logs = []
    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                pass
                
    logs.append(log_entry)
    with open(feedback_file, "w") as f:
        json.dump(logs, f, indent=2)
        
    # Update asset status
    asset.status = "rejected"
    store.save_campaign(campaign)
    
    return {"status": "feedback_logged", "asset_type": asset_type}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
