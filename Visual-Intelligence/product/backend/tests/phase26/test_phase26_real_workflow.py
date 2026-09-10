"""
Phase 26 20-Step Controlled Productization Benchmark Execution.
"""
import pytest
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus, WorkerRole
from src.creative_workforce.worker_registry.registry import WorkerRegistry
from src.creative_workforce.worker_roles.roles import get_role_definition
from src.creative_workforce.capability_binding.manifest import CapabilityManifest, CapabilityResolver
from src.creative_workforce.skill_registry.models import SkillDefinition, SkillRiskClass
from src.creative_workforce.skill_registry.registry import SkillRegistry
from src.creative_workforce.skill_runtime.runtime import SkillRuntime
from src.creative_workforce.campaign_rooms.room_manager import CampaignRoomManager, RoomStatus
from src.creative_workforce.collaboration.collaboration_hub import CollaborationHub
from src.creative_workforce.context_resolution.resolver import ContextResolver, ContextCategory, EpistemicType
from src.creative_workforce.evidence_bridge.evidence_generator import EvidenceBridge
from src.creative_workforce.handoffs.handoff_service import HandoffService, HandoffStatus
from src.creative_workforce.approval_bridge.bridge import WorkforceApprovalBridge, ApprovalState
from src.authorization_center.approval_service import ApprovalService
from src.creative_workforce.workforce_activity.activity_stream import WorkforceActivityLogger, WorkforceEventType
from src.creative_workforce.workforce_observability.metrics import WorkforceObservability
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


def test_phase26_20_step_real_productization_workflow():
    # 1. Step 1: Initialize Registry & Services
    worker_reg = WorkerRegistry()
    skill_reg = SkillRegistry()
    cap_resolver = CapabilityResolver()
    room_mgr = CampaignRoomManager()
    collab_hub = CollaborationHub(room_manager=room_mgr)
    handoff_svc = HandoffService(capability_resolver=cap_resolver)
    app_svc = ApprovalService()
    app_bridge = WorkforceApprovalBridge(approval_service=app_svc)
    activity_logger = WorkforceActivityLogger()
    observability = WorkforceObservability()

    # 2. Step 2: Register Workers
    cd = WorkerIdentity("cd_elena", "tenant_alpha", "org_lux", "Elena", WorkerRole.CREATIVE_DIRECTOR.value, "Lead CD", WorkerStatus.ACTIVE)
    vdna = WorkerIdentity("vdna_marcus", "tenant_alpha", "org_lux", "Marcus", WorkerRole.VISUAL_DNA_SPECIALIST.value, "Visual DNA", WorkerStatus.ACTIVE)
    quality = WorkerIdentity("qual_sophie", "tenant_alpha", "org_lux", "Sophie", WorkerRole.QUALITY_REVIEWER.value, "Quality Lead", WorkerStatus.ACTIVE)
    
    worker_reg.register_worker(cd)
    worker_reg.register_worker(vdna)
    worker_reg.register_worker(quality)

    # 3. Step 3: Register Capabilities
    cap_resolver.register_manifest(CapabilityManifest("cd_elena", {"creative_direction.create", "campaign.read", "handoff.create"}))
    cap_resolver.register_manifest(CapabilityManifest("vdna_marcus", {"visual_dna.extract", "render.request", "handoff.create"}))
    cap_resolver.register_manifest(CapabilityManifest("qual_sophie", {"quality.evaluate", "compliance.verify", "handoff.create"}))

    # 4. Step 4: Register Versioned Skills
    skill_cd = SkillDefinition("creative_direction", "1.0.0", "Generate creative concept", required_capabilities=["creative_direction.create"])
    skill_vdna = SkillDefinition("prompt_formulation", "1.0.0", "Compile visual tokens", required_capabilities=["visual_dna.extract"])
    skill_qual = SkillDefinition("quality_audit", "1.0.0", "Audit visual compliance", required_capabilities=["quality.evaluate"])
    
    skill_reg.register_skill(skill_cd)
    skill_reg.register_skill(skill_vdna)
    skill_reg.register_skill(skill_qual)

    # 5. Step 5: Create Campaign Room
    room = room_mgr.create_room("tenant_alpha", "client_haute", "C-2026-AUTUMN", "Milan Autumn 2026 Collaboration Room")
    room_mgr.join_room(room.room_id, "human_director", "HUMAN")
    room_mgr.join_room(room.room_id, "cd_elena", "WORKER")
    room_mgr.join_room(room.room_id, "vdna_marcus", "WORKER")
    room_mgr.join_room(room.room_id, "qual_sophie", "WORKER")

    # 6. Step 6: Human Director Posts Campaign Brief
    collab_hub.post_message(room.room_id, "human_director", "HUMAN", "Develop a high-concept editorial campaign for the Autumn trenchcoat line.")
    activity_logger.emit_event(WorkforceEventType.WORKER_TASK_STARTED, "tenant_alpha", "client_haute", "cd_elena", {"task": "concept_development"}, room_id=room.room_id)

    # 7. Step 7: Assemble Typed Context
    raw_ctx = {
        "brand_guidelines": "Monochrome architectural silhouette, strict serif typography",
        "visual_dna_tokens": ["monochrome", "35mm_kodak", "brutalist_concrete"],
    }
    typed_context = ContextResolver.assemble_campaign_context("tenant_alpha", "client_haute", "C-2026-AUTUMN", raw_ctx)
    assert len(typed_context) == 2

    # 8. Step 8: CD Executes Creative Direction Skill
    runtime = SkillRuntime(capability_resolver=cap_resolver)
    cd_res = runtime.execute_skill(cd, skill_cd, inputs={"theme": "Architectural Noir"})
    assert cd_res.status == "SUCCESS"
    observability.record_task_completed("cd_elena", cd_res.execution_time_ms)

    # 9. Step 9: Formulate Structured Evidence Recommendation
    rec = EvidenceBridge.create_recommendation(
        decision="Architectural Noir Theme with High-Contrast Concrete Textures",
        rationale="Amplifies the structural tailoring of the wool trenchcoat collection",
        supporting_evidence=["Brand DNA Token Set #VD-01", "Client Lookbook Archive 2025"],
        confidence=0.91,
    )
    assert rec.is_advisory is True

    # 10. Step 10: CD Posts Message & Creates Handoff to Visual DNA Specialist
    collab_hub.post_message(room.room_id, "cd_elena", "WORKER", f"Concept formulated: {rec.decision}", claims=[rec.rationale], confidence=rec.confidence)
    handoff_1 = handoff_svc.create_handoff(
        room_id=room.room_id,
        tenant_id="tenant_alpha",
        client_id="client_haute",
        sender_worker_id="cd_elena",
        recipient_worker_id="vdna_marcus",
        purpose="Generate visual prompts and token compositions",
        input_artifacts=[{"concept_id": "concept_noir", "title": rec.decision}],
        requested_action="visual_dna.extract",
    )
    assert "concept_noir" in handoff_1.artifact_hashes

    # 11. Step 11: Visual DNA Specialist Accepts Handoff
    handoff_svc.accept_handoff(handoff_1.handoff_id, vdna)
    activity_logger.emit_event(WorkforceEventType.WORKER_HANDOFF_CREATED, "tenant_alpha", "client_haute", "vdna_marcus", {"handoff_id": handoff_1.handoff_id})

    # 12. Step 12: Visual DNA Specialist Formulates Prompt
    vdna_res = runtime.execute_skill(vdna, skill_vdna, inputs={"concept_id": "concept_noir"})
    assert vdna_res.status == "SUCCESS"

    # 13. Step 13: High-Risk Render Requires Human Authorization
    binding = app_bridge.request_workforce_approval(
        tenant_id="tenant_alpha",
        client_id="client_haute",
        worker_id="vdna_marcus",
        action_name="EXECUTE_HIGH_RISK_RENDER",
        target_object_id="concept_noir",
        target_version="1.0.0",
        cost_estimate=800.0,
    )
    activity_logger.emit_event(WorkforceEventType.WORKER_WAITING_APPROVAL, "tenant_alpha", "client_haute", "vdna_marcus", {"binding_id": binding.binding_id})

    # 14. Step 14: Super Admin Grants Approval in Authorization Center
    admin_ctx = OperatorContext(operator_id="admin_01", tenant_id="tenant_alpha", client_id="client_haute", roles=[OperatorRole.LEAD_CURATOR])
    app_svc.approve_request(binding.approval_id, admin_ctx, rationale="High-risk render approved for Milan campaign")
    activity_logger.emit_event(WorkforceEventType.WORKER_APPROVAL_RECEIVED, "tenant_alpha", "client_haute", "vdna_marcus", {"approval_id": binding.approval_id})

    # 15. Step 15: Token Verified for Execution
    exec_token = app_bridge.assert_action_authorized(binding.binding_id, target_version="1.0.0")
    assert exec_token.startswith("tok_")

    # 16. Step 16: Render Simulated Artifact and Add to Room
    artifact = {"artifact_id": "render_noir_01", "uri": "s3://assets/noir_01.png", "drift_score": 0.04}
    room_mgr.add_artifact(room.room_id, artifact)

    # 17. Step 17: Visual DNA Specialist Hands Off to Quality Reviewer
    handoff_2 = handoff_svc.create_handoff(
        room_id=room.room_id,
        tenant_id="tenant_alpha",
        client_id="client_haute",
        sender_worker_id="vdna_marcus",
        recipient_worker_id="qual_sophie",
        purpose="Review visual render against brand guidelines",
        input_artifacts=[artifact],
        requested_action="quality.evaluate",
    )
    handoff_svc.accept_handoff(handoff_2.handoff_id, quality)

    # 18. Step 18: Quality Reviewer Audits Compliance
    qual_res = runtime.execute_skill(quality, skill_qual, inputs={"artifact_id": "render_noir_01"})
    assert qual_res.status == "SUCCESS"
    observability.record_review_result("cd_elena", accepted=True)

    # 19. Step 19: Human Director Signs Off on Decision
    room_mgr.record_decision(room.room_id, {
        "decision": "Approved Architectural Noir Concept and Render for Milan Lookbook",
        "approved_by": "human_director",
        "execution_token": exec_token,
    })

    # 20. Step 20: Audit Verification
    events = activity_logger.query_events("tenant_alpha", client_id="client_haute")
    assert len(events) >= 3
    for evt in events:
        assert "api_key" not in evt.payload
        assert "chain_of_thought" not in evt.payload
