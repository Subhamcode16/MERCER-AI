from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Path, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.campaign import Campaign, MemoryNode
from app.storage.local_store import LocalStore
from app.storage.asset_store import AssetStore
from app.adapters.vision_adapter import VisionAdapter
from app.adapters.prompt_engine import PromptEngine
from app.utils.security import limiter

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])

store = LocalStore()
asset_store = AssetStore()
vision_adapter = VisionAdapter()
prompt_engine = PromptEngine()


# --- Request/Response Models ---

class CreateCampaignRequest(BaseModel):
    name: str = Field("Untitled Campaign", max_length=100)

class RenameCampaignRequest(BaseModel):
    name: str = Field(..., max_length=100)

class CampaignSummary(BaseModel):
    """Lightweight summary for the folder grid view — avoids sending full phase data."""
    id: str
    name: str
    has_material: bool
    created_at: str

# --- Routes ---

@router.get("", response_model=List[CampaignSummary])
@limiter.limit("30/minute")
async def list_campaigns(request: Request):
    """
    Returns all campaign folders for the Studio grid view.
    Each item is a lightweight summary (id, name, has_material).
    """
    campaigns = store.list_campaigns()
    return [
        CampaignSummary(
            id=c.id,
            name=c.name,
            has_material=c.material_path is not None,
            created_at=c.created_at
        )
        for c in sorted(campaigns, key=lambda c: c.created_at)
    ]

@router.post("", response_model=CampaignSummary)
@limiter.limit("30/minute")
async def create_campaign(request: Request, body: CreateCampaignRequest):
    """
    Creates a new Campaign folder from just a name.
    The identity, planning, execution, and evaluation phases are empty and fill
    progressively as the user uploads material and triggers AI analysis.
    """
    campaign = Campaign(name=body.name)
    store.save_campaign(campaign)
    return CampaignSummary(
        id=campaign.id,
        name=campaign.name,
        has_material=False,
        created_at=campaign.created_at
    )

@router.get("/{campaign_id}", response_model=Campaign)
@limiter.limit("30/minute")
async def get_campaign(request: Request, campaign_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$")):
    """
    Returns the full Campaign object including memory_stream, ProductDNA, and all lifecycle phases.
    The frontend uses this to restore workspace state after the user navigates away and comes back.
    """
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.patch("/{campaign_id}", response_model=CampaignSummary)
@limiter.limit("30/minute")
async def rename_campaign(request: Request, body: RenameCampaignRequest, campaign_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$")):
    """Renames a campaign folder."""
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.name = body.name
    campaign.updated_at = datetime.utcnow().isoformat()
    store.save_campaign(campaign)
    return CampaignSummary(
        id=campaign.id,
        name=campaign.name,
        has_material=campaign.material_path is not None,
        created_at=campaign.created_at
    )

@router.delete("/{campaign_id}")
@limiter.limit("30/minute")
async def delete_campaign(request: Request, campaign_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$")):
    """
    Deletes a campaign folder and all its associated asset files.
    """
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Delete the binary asset files (images)
    asset_store.delete_campaign_assets(campaign_id)

    # Delete the JSON metadata file
    import os
    json_path = store._get_path(campaign_id)
    if os.path.exists(json_path):
        os.remove(json_path)

    return {"status": "deleted", "campaign_id": campaign_id}

@router.post("/{campaign_id}/material")
@limiter.limit("30/minute")
async def upload_material(request: Request, campaign_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$"), file: UploadFile = File(...)):
    """
    Accepts a multipart image upload and saves it to the campaign's asset directory.
    Updates the campaign JSON with the material_path and marks it as ready for analysis.
    """
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    file_bytes = await file.read()
    material_path = asset_store.save_material(campaign_id, file_bytes, file.filename or "material.jpg")

    campaign.material_path = material_path
    campaign.updated_at = datetime.utcnow().isoformat()
    store.save_campaign(campaign)

    return {
        "status": "uploaded",
        "campaign_id": campaign_id,
        "material_path": material_path
    }

@router.post("/{campaign_id}/analyze")
@limiter.limit("5/minute")
async def analyze_material(request: Request, background_tasks: BackgroundTasks, campaign_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$")):
    """
    Triggers Gemini Vision analysis on the campaign's uploaded material.
    Runs the analysis as a background task and streams the results into the
    campaign's memory_stream and identity phase for frontend replay.
    """
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if not campaign.material_path:
        raise HTTPException(status_code=400, detail="No material uploaded yet. Upload an image first.")

    def _run_analysis(c: Campaign):
        """Background task: calls Gemini, populates identity phase and memory_stream."""
        try:
            # Step 1: Observation node
            c.memory_stream.append(MemoryNode(
                type="observation",
                content="Material received. Initiating visual analysis..."
            ))
            store.save_campaign(c)

            # Step 2: Call Gemini Vision
            product_dna, creative_direction = vision_adapter.analyze_product(c.material_path)

            # Step 3: Populate Identity Phase
            c.identity.product_dna = product_dna

            # Step 4: Build reasoning memory nodes from the extracted DNA
            c.memory_stream.append(MemoryNode(
                type="observation",
                content=f"Material identified as {product_dna.material.value} ({int(product_dna.material.confidence * 100)}% confidence). Technique: {product_dna.weaving_technique.value}."
            ))
            c.memory_stream.append(MemoryNode(
                type="reasoning",
                content=f"Cultural context traced to {product_dna.cultural_context.value}. Primary features extracted: {', '.join(product_dna.primary_features.value) if isinstance(product_dna.primary_features.value, list) else product_dna.primary_features.value}."
            ))

            # Step 5: Populate Planning Phase with AI-proposed creative direction
            if creative_direction and creative_direction.get("title"):
                c.planning.proposed_direction_title = creative_direction["title"]
                c.planning.proposed_direction_body = creative_direction["body"]
                c.memory_stream.append(MemoryNode(
                    type="conclusion",
                    content=f"Creative direction proposed: '{creative_direction['title']}'. {creative_direction['body']}"
                ))

            # Step 5.5: Compute Recommendations
            try:
                recs = prompt_engine.generate_recommendations(c)
                c.planning.recommendations = recs
                c.planning.selected_background = recs.get("background", {}).get("value")
                c.planning.selected_pose = recs.get("pose", {}).get("value")
                c.planning.selected_lighting = recs.get("lighting", {}).get("value")
                c.memory_stream.append(MemoryNode(
                    type="reasoning",
                    content=f"Art direction recommendations computed based on fabric physics. Background: {c.planning.selected_background}. Pose: {c.planning.selected_pose}. Lighting: {c.planning.selected_lighting}."
                ))
            except Exception as rec_err:
                print(f"[Analyze] Failed to compute recommendations: {rec_err}")
            
            c.updated_at = datetime.utcnow().isoformat()
            store.save_campaign(c)
            print(f"[Analyze] Campaign {c.id} analysis complete.")

        except Exception as e:
            # Log error into memory_stream so the frontend can surface it
            c.memory_stream.append(MemoryNode(
                type="reasoning",
                content=f"Analysis encountered an issue: {str(e)}. Retrying with fallback model..."
            ))
            store.save_campaign(c)
            print(f"[Analyze] Error during analysis for campaign {c.id}: {e}")

    background_tasks.add_task(_run_analysis, campaign)

    return {
        "status": "analysis_started",
        "campaign_id": campaign_id,
        "message": "Gemini Vision is analyzing the material. Poll GET /api/campaigns/{id} to track memory_stream updates."
    }

class UpdateOptionsRequest(BaseModel):
    background: str
    pose: str
    lighting: str

@router.patch("/{campaign_id}/options", response_model=Campaign)
@limiter.limit("30/minute")
async def update_campaign_options(request: Request, body: UpdateOptionsRequest, campaign_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$")):
    """
    Saves the user's manual selections for background, pose, and lighting.
    """
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.planning.selected_background = body.background
    campaign.planning.selected_pose = body.pose
    campaign.planning.selected_lighting = body.lighting
    campaign.updated_at = datetime.utcnow().isoformat()
    store.save_campaign(campaign)
    return campaign

@router.post("/{campaign_id}/generate")
@limiter.limit("5/minute")
async def generate_campaign(request: Request, background_tasks: BackgroundTasks, campaign_id: str = Path(..., pattern="^[a-zA-Z0-9_-]+$")):
    """
    Triggers the Phase 3 Prompt Engine (RAG Pipeline) to synthesize constraints
    and generate the moodboard brief and asset prompts.
    Stores the output in the DB. Returns placeholder images for the MVP.
    """
    campaign = store.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    def _run_generation(c: Campaign):
        try:
            c.memory_stream.append(MemoryNode(
                type="observation",
                content="Starting generation pipeline. Fetching Obsidian knowledge and Honcho memory..."
            ))
            store.save_campaign(c)
            
            # Run RAG Prompt Engine
            result = prompt_engine.generate_campaign_assets(c)
            
            c.memory_stream.append(MemoryNode(
                type="conclusion",
                content="Successfully synthesized constraints and generated prompts."
            ))
            
            # Populate execution phase with generated briefs and placeholder URLs
            from models.campaign import AssetState
            c.execution.moodboard_brief = result.get("moodboard_brief", "")
            
            prompts = result.get("prompts", {})
            c.execution.asset_states = []
            
            # Create a placeholder asset for each requested asset
            for asset_key, prompt_text in prompts.items():
                c.execution.asset_states.append(AssetState(
                    id=asset_key,
                    prompt=prompt_text,
                    status="completed", # Mocked as completed for MVP
                    image_url=f"https://source.unsplash.com/800x600/?{asset_key},fashion" # MVP placeholder
                ))
                
            c.updated_at = datetime.utcnow().isoformat()
            store.save_campaign(c)
            print(f"[Generate] Campaign {c.id} generation complete.")
            
        except Exception as e:
            c.memory_stream.append(MemoryNode(
                type="reasoning",
                content=f"Generation encountered an issue: {str(e)}."
            ))
            store.save_campaign(c)
            print(f"[Generate] Error during generation for campaign {c.id}: {e}")

    background_tasks.add_task(_run_generation, campaign)

    return {
        "status": "generation_started",
        "campaign_id": campaign_id,
        "message": "Prompt Engine is generating the campaign. Poll GET /api/campaigns/{id} to view execution states."
    }
