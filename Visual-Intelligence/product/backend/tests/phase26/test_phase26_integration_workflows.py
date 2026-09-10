"""
Phase 26 Integration Workflows A, B, C, D, E.
"""
import pytest
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus
from src.creative_workforce.worker_registry.registry import WorkerRegistry
from src.creative_workforce.capability_binding.manifest import (
    CapabilityManifest,
    CapabilityResolver,
)
from src.creative_workforce.skill_registry.models import SkillDefinition
from src.creative_workforce.skill_runtime.runtime import SkillRuntime
from src.creative_workforce.campaign_rooms.room_manager import CampaignRoomManager
from src.creative_workforce.collaboration.collaboration_hub import CollaborationHub
from src.creative_workforce.handoffs.handoff_service import HandoffService
from src.creative_workforce.delegation.delegation_engine import DelegationEngine
from src.creative_workforce.routines.routine_engine import WorkforceRoutine, RoutineEngine
from src.creative_workforce.approval_bridge.bridge import WorkforceApprovalBridge
from src.authorization_center.approval_service import ApprovalService
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


def test_workflow_a_campaign_creation():
    """Workflow A: Human -> Planner -> CD -> Visual DNA -> Quality -> Human Review."""
    resolver = CapabilityResolver()
    resolver.register_manifest(CapabilityManifest("planner_01", {"campaign.plan", "handoff.create"}))
    resolver.register_manifest(CapabilityManifest("cd_01", {"creative_direction.create", "handoff.create"}))
    resolver.register_manifest(CapabilityManifest("vdna_01", {"visual_dna.extract", "handoff.create"}))
    resolver.register_manifest(CapabilityManifest("quality_01", {"quality.evaluate", "handoff.create"}))

    planner = WorkerIdentity("planner_01", "t1", "o1", "Planner", "CAMPAIGN_PLANNER", "desc", WorkerStatus.ACTIVE)
    cd = WorkerIdentity("cd_01", "t1", "o1", "CD", "CREATIVE_DIRECTOR", "desc", WorkerStatus.ACTIVE)
    vdna = WorkerIdentity("vdna_01", "t1", "o1", "Visual DNA", "VISUAL_DNA_SPECIALIST", "desc", WorkerStatus.ACTIVE)
    quality = WorkerIdentity("quality_01", "t1", "o1", "Quality", "QUALITY_REVIEWER", "desc", WorkerStatus.ACTIVE)

    handoff_svc = HandoffService(capability_resolver=resolver)

    # 1. Planner handoff to CD
    h1 = handoff_svc.create_handoff("room_1", "t1", "c1", "planner_01", "cd_01", "Milestone schedule", requested_action="creative_direction.create")
    handoff_svc.accept_handoff(h1.handoff_id, cd)

    # 2. CD handoff to Visual DNA
    h2 = handoff_svc.create_handoff("room_1", "t1", "c1", "cd_01", "vdna_01", "Moodboard visual concept", requested_action="visual_dna.extract")
    handoff_svc.accept_handoff(h2.handoff_id, vdna)

    # 3. Visual DNA handoff to Quality
    h3 = handoff_svc.create_handoff("room_1", "t1", "c1", "vdna_01", "quality_01", "Completed Visual DNA tokens", requested_action="quality.evaluate")
    handoff_svc.accept_handoff(h3.handoff_id, quality)

    assert h3.status == "ACCEPTED"


def test_workflow_b_product_understanding():
    """Workflow B: Product Intake -> Intelligence -> Brand Context -> Opportunities."""
    resolver = CapabilityResolver()
    resolver.register_manifest(CapabilityManifest("intel_01", {"brand.audit", "handoff.create"}))
    intel = WorkerIdentity("intel_01", "t1", "c1", "Intel", "BRAND_INTELLIGENCE", "desc", WorkerStatus.ACTIVE)

    skill = SkillDefinition(
        skill_id="brand_audit",
        version="1.0.0",
        purpose="Analyze product catalog and brand positioning",
        required_capabilities=["brand.audit"],
    )
    runtime = SkillRuntime(capability_resolver=resolver)
    res = runtime.execute_skill(intel, skill, inputs={"catalog_id": "cat_2026_fall"})
    assert res.status == "SUCCESS"


def test_workflow_c_visual_direction():
    """Workflow C: CD -> Visual DNA -> Prompt Compilation -> Render Request -> Human Review."""
    resolver = CapabilityResolver()
    resolver.register_manifest(CapabilityManifest("cd_01", {"creative_direction.create", "render.request"}))
    cd = WorkerIdentity("cd_01", "t1", "c1", "CD", "CREATIVE_DIRECTOR", "desc", WorkerStatus.ACTIVE)

    skill = SkillDefinition(
        skill_id="render_prep",
        version="1.0.0",
        purpose="Prepare prompts and request render",
        required_capabilities=["render.request"],
    )
    runtime = SkillRuntime(capability_resolver=resolver)
    res = runtime.execute_skill(cd, skill, inputs={"concept": "Monochrome Silhouette"})
    assert res.status == "SUCCESS"


def test_workflow_d_multi_agent_campaign_room():
    """Workflow D: Multi-agent Campaign Room collaboration and decision tracking."""
    room_mgr = CampaignRoomManager()
    room = room_mgr.create_room("t1", "c1", "CAMP_100", "Summer Campaign Room")
    hub = CollaborationHub(room_manager=room_mgr)

    hub.post_message(room.room_id, "human_lead", "HUMAN", "We need 3 concept variations.")
    hub.post_message(room.room_id, "strat_01", "WORKER", "Proposing Neo-Classical, Y2K Minimal, Cyber Tailoring.")
    
    room_mgr.record_decision(room.room_id, {"decision": "Adopted Neo-Classical direction", "approved_by": "human_lead"})
    updated_room = room_mgr.get_room(room.room_id)
    assert len(updated_room.decisions) == 1


def test_workflow_e_routine_execution_and_human_approval():
    """Workflow E: Routine Trigger -> Work Item -> Worker Assignment -> Human Approval."""
    resolver = CapabilityResolver()
    routine_engine = RoutineEngine(capability_resolver=resolver)
    app_service = ApprovalService()
    bridge = WorkforceApprovalBridge(approval_service=app_service)

    routine = WorkforceRoutine(
        routine_id="weekly_audit",
        tenant_id="t1",
        client_id="c1",
        name="Weekly Visual Audit",
        worker_id="qual_01",
        skill_id="quality_audit",
        required_approvals=["APPROVE_AUDIT_PUBLISH"],
    )
    routine_engine.register_routine(routine)
    worker = WorkerIdentity("qual_01", "t1", "c1", "Quality", "QUALITY_REVIEWER", "desc", WorkerStatus.ACTIVE)

    outcome = routine_engine.trigger_routine("weekly_audit", worker, execution_nonce="audit_nonce_01")
    assert outcome.is_advisory is True

    # Request human approval
    binding = bridge.request_workforce_approval("t1", "c1", "qual_01", "APPROVE_AUDIT_PUBLISH", "audit_report", "1.0.0")
    
    # Approve in Authorization Center
    ctx = OperatorContext(operator_id="admin_01", tenant_id="t1", client_id="c1", roles=[OperatorRole.LEAD_CURATOR])
    app_service.approve_request(binding.approval_id, ctx, rationale="Audit confirmed")

    token = bridge.assert_action_authorized(binding.binding_id, target_version="1.0.0")
    assert token.startswith("tok_")
