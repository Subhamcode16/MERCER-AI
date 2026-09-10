"""
Phase 27 Creative Campaign Studio FastAPI Router.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.campaign_studio.workspace import WorkspaceStore
from src.campaign_studio.campaign_workspace import CampaignWorkspaceManager, StudioCampaignStatus
from src.campaign_studio.discovery import AdaptiveDiscoveryEngine
from src.campaign_studio.creative_intelligence import CreativeIntelligenceEngine
from src.campaign_studio.direction_management import DirectionManager
from src.campaign_studio.visual_development import VisualDevelopmentPipeline
from src.campaign_studio.asset_lineage import AssetLineageGraph
from src.campaign_studio.review import StudioReviewEngine
from src.campaign_studio.approval import StudioApprovalBridge, StudioApprovalStatus
from src.campaign_studio.launch import LaunchManager
from src.campaign_studio.outcomes import OutcomesManager
from src.campaign_studio.campaign_memory import CampaignMemoryStore
from src.campaign_studio.command_interface import StudioCommandParser
from src.campaign_studio.evidence_explorer import EvidenceExplorer
from src.campaign_studio.conflict_resolution import ConflictResolutionEngine
from src.campaign_studio.state_projection import StateProjectionEngine
from src.campaign_studio.studio_governance import StudioGovernanceEngine


studio_router = APIRouter(prefix="/api/studio", tags=["CampaignStudio"])

# Singleton Services for Studio Session
workspace_store = WorkspaceStore()
campaign_mgr = CampaignWorkspaceManager()
discovery_engine = AdaptiveDiscoveryEngine()
intelligence_engine = CreativeIntelligenceEngine()
direction_mgr = DirectionManager()
visual_pipeline = VisualDevelopmentPipeline()
lineage_graph = AssetLineageGraph()
review_engine = StudioReviewEngine()
approval_bridge = StudioApprovalBridge()
launch_mgr = LaunchManager()
outcomes_mgr = OutcomesManager()
memory_store = CampaignMemoryStore()
command_parser = StudioCommandParser()
evidence_explorer = EvidenceExplorer()
conflict_engine = ConflictResolutionEngine()
projection_engine = StateProjectionEngine()
governance_engine = StudioGovernanceEngine()


def get_operator_context(
    x_operator_id: str = Header(default="op_creative_director_01"),
    x_operator_role: str = Header(default="CREATIVE_DIRECTOR"),
) -> OperatorContext:
    try:
        role = OperatorRole(x_operator_role)
    except ValueError:
        role = OperatorRole.STAFF_OPERATOR
    return OperatorContext(
        operator_id=x_operator_id,
        role=role,
        department="Creative Direction",
    )


# --- Request Models ---
class CreateClientRequest(BaseModel):
    client_id: str
    name: str
    industry: str = "Haute Couture & Luxury Fashion"


class CreateBrandRequest(BaseModel):
    brand_id: str
    client_id: str
    name: str
    brand_ethos: str = ""


class CreateCampaignRequest(BaseModel):
    campaign_id: str
    client_id: str
    brand_id: str
    title: str
    description: str = ""


class DiscoveryIntakeRequest(BaseModel):
    campaign_id: str
    raw_inputs: Dict[str, Any]


class AnswerQuestionRequest(BaseModel):
    campaign_id: str
    question_id: str
    answer: str


class CommandRequest(BaseModel):
    raw_text: str
    campaign_id: Optional[str] = None


class ApprovalDecisionRequest(BaseModel):
    approval_id: str
    decision: StudioApprovalStatus
    comments: str = ""


# --- Endpoints ---

@studio_router.post("/clients")
def create_client(req: CreateClientRequest):
    client = workspace_store.create_client(req.client_id, req.name, req.industry)
    return {"status": "success", "client": client}


@studio_router.get("/clients")
def list_clients():
    return {"clients": workspace_store.list_clients()}


@studio_router.post("/campaigns")
def create_campaign(req: CreateCampaignRequest, operator: OperatorContext = Depends(get_operator_context)):
    camp = campaign_mgr.create_campaign(
        campaign_id=req.campaign_id,
        client_id=req.client_id,
        brand_id=req.brand_id,
        title=req.title,
        created_by=operator.operator_id,
        description=req.description,
    )
    return {"status": "success", "campaign": camp}


@studio_router.get("/campaigns/{campaign_id}")
def get_campaign(campaign_id: str):
    camp = campaign_mgr.get_campaign(campaign_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"campaign": camp}


@studio_router.post("/discovery/intake")
def intake_discovery(req: DiscoveryIntakeRequest):
    items = discovery_engine.analyze_intake(req.campaign_id, req.raw_inputs)
    questions = discovery_engine.get_pending_questions(req.campaign_id)
    return {"status": "success", "discovery_items": items, "pending_questions": questions}


@studio_router.post("/discovery/answer")
def answer_question(req: AnswerQuestionRequest):
    try:
        item = discovery_engine.answer_question(req.campaign_id, req.question_id, req.answer)
        return {"status": "success", "resolved_item": item}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@studio_router.post("/intelligence/synthesize")
def synthesize_intelligence(campaign_id: str, brand_name: str = "Aethelgard Paris"):
    intel = intelligence_engine.synthesize_intelligence(campaign_id, brand_name, {})
    return {"status": "success", "intelligence": intel}


@studio_router.post("/directions/generate")
def generate_directions(campaign_id: str):
    cards = direction_mgr.generate_candidate_directions(campaign_id)
    return {"status": "success", "directions": cards}


@studio_router.post("/directions/{direction_id}/select")
def select_direction(campaign_id: str, direction_id: str):
    try:
        card = direction_mgr.select_direction(campaign_id, direction_id)
        return {"status": "success", "selected_direction": card}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@studio_router.post("/visuals/generate")
def generate_visual_drafts(campaign_id: str, direction_id: str):
    visual_pipeline.compile_visual_dna(campaign_id, direction_id)
    drafts = visual_pipeline.generate_asset_drafts(campaign_id, direction_id)
    return {"status": "success", "drafts": drafts}


@studio_router.post("/reviews/{asset_id}")
def review_asset(campaign_id: str, asset_id: str):
    critique = review_engine.evaluate_asset(campaign_id, asset_id)
    return {"status": "success", "critique": critique}


@studio_router.post("/approvals/request")
def request_approval(campaign_id: str, asset_id: str, operator: OperatorContext = Depends(get_operator_context)):
    req = approval_bridge.create_approval_request(campaign_id, asset_id, operator.operator_id)
    return {"status": "success", "approval_request": req}


@studio_router.post("/approvals/decide")
def decide_approval(req: ApprovalDecisionRequest, operator: OperatorContext = Depends(get_operator_context)):
    try:
        decided = approval_bridge.submit_decision(req.approval_id, operator, req.decision, req.comments)
        return {"status": "success", "approval": decided}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@studio_router.post("/commands/execute")
def execute_command(req: CommandRequest, operator: OperatorContext = Depends(get_operator_context)):
    result = command_parser.parse_and_validate(req.raw_text, operator, req.campaign_id)
    return {"result": result}


@studio_router.get("/projections/{campaign_id}")
def get_campaign_projection(campaign_id: str):
    camp = campaign_mgr.get_campaign(campaign_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    proj = projection_engine.project_campaign_overview(
        campaign_id=camp.campaign_id,
        client_name="Luxury Portfolio Inc.",
        brand_name="Aethelgard Paris",
        title=camp.title,
        status=camp.status.value,
        version=camp.version,
        asset_count=len(visual_pipeline.list_assets(campaign_id)),
        pending_approvals_count=len(approval_bridge.list_approvals_for_campaign(campaign_id)),
    )
    return {"projection": proj}
