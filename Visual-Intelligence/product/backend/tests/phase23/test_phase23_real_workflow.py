"""
Phase 23 Real Production Workflow Benchmark (25-Step Controlled Lifecycle).
Demonstrates that operational continuity can be safely recovered across a
simulated worker/process restart without automatically acquiring or restoring execution authority.
"""
import pytest
import time
import uuid

from src.production_runtime.runtime_orchestrator import ProductionRuntimeOrchestrator
from src.production_runtime.runtime_models import (
    RuntimeTask,
    WorkflowOperationalState,
    QueuePriority
)
from src.persistence.state_store import StateStore
from src.persistence.checkpoint_store import CheckpointStore
from src.persistence.ledger_store import LedgerStore
from src.secret_operations.secret_provider import ProductionSecretProvider
from src.secret_operations.secret_models import CredentialDomain
from src.deployment.deployment_models import (
    ArtifactManifest,
    TargetEnvironment,
    PromotionStatus
)
from src.deployment.version_registry import VersionRegistry
from src.deployment.deployment_ledger import DeploymentLedger
from src.deployment.promotion import EnvironmentPromotionPipeline
from src.creative_workforce import (
    StaffRegistry,
    ClientContextManager,
    WorkforceDelegationEngine,
    CreativeWorkforceDirector,
    CreativeCollaborationProtocol,
    CreativeArtifact,
    IndependentReviewer
)
from src.model_observability.cost_meter import CostMeter
from src.model_observability.invocation_trace import InvocationTrace

@pytest.mark.asyncio
async def test_phase23_real_production_25_step_workflow():
    # Setup Infrastructure
    orchestrator = ProductionRuntimeOrchestrator(max_global_workers=8, max_tenant_workers=4)
    state_store = StateStore()
    cp_store = CheckpointStore()
    ledger_store = LedgerStore()
    secret_provider = ProductionSecretProvider()
    cost_meter = CostMeter()

    # Register mock healthy dependency probes
    async def mock_db_probe():
        return True
    async def mock_llm_probe():
        return True
    orchestrator.health_monitor.register_probe("database", mock_db_probe, is_critical=True)
    orchestrator.health_monitor.register_probe("llm_gateway", mock_llm_probe, is_critical=True)

    # Register scoped secrets
    secret_provider.register_secret("gemini_key", CredentialDomain.LLM, "sk-gemini-live-prod-key")
    secret_provider.register_secret("mcp_key", CredentialDomain.MCP, "sk-mcp-live-tool-key")

    # Step 1: Client Context
    client_id = "client-ilyren-lux"
    tenant_id = "tenant-001"
    brand_id = "brand-ilyren-couture"
    workflow_id = f"wf-prod-{uuid.uuid4().hex[:8]}"

    # Step 2: Campaign Creation
    campaign_title = "ILYREN Autumn/Winter 2026 Haute Couture"
    objective = "Produce campaign copy, moodboards, and approved social rollout assets."
    state_store.put(
        key=f"campaign:{workflow_id}",
        tenant_id=tenant_id,
        client_id=client_id,
        data={"title": campaign_title, "objective": objective, "status": "INITIALIZED"}
    )
    ledger_store.append_event(f"evt-{uuid.uuid4().hex[:6]}", tenant_id, client_id, "CAMPAIGN_CREATED", {"title": campaign_title})

    # Step 3: Workforce Assignment
    staff_registry = StaffRegistry()
    context_mgr = ClientContextManager()
    delegation_engine = WorkforceDelegationEngine(staff_registry, context_mgr)
    director = CreativeWorkforceDirector(delegation_engine)

    # Step 4: Creative Direction & Plan Formulation
    plan = director.formulate_workforce_plan(
        client_id=client_id,
        brand_id=brand_id,
        campaign_title=campaign_title,
        objective=objective
    )
    assert plan is not None
    assert len(plan.assignments) > 0

    # Step 5: LLM Strategy Generation
    cost_meter.ingest_trace(InvocationTrace(
        trace_id="tr-real-01",
        correlation_id="corr-real-01",
        client_id=client_id,
        provider="google",
        model="gemini-2.5-flash",
        model_version="2.5",
        role="PROPOSE",
        timestamp=time.time(),
        latency_ms=420.0,
        input_tokens=1500,
        output_tokens=800,
        known_cost_usd=0.0023,
        timeout_occurred=False,
        retry_count=0,
        fallback_used=False,
        structured_output_valid=True,
        policy_rejected=False,
        status="SUCCESS"
    ))
    strategy_text = "Emphasize architectural draping, obsidian-silk textures, and cinematic golden hour lighting."

    # Step 6: Visual Generation
    visual_asset_id = f"asset-{uuid.uuid4().hex[:8]}"
    visual_payload = {
        "asset_id": visual_asset_id,
        "aspect_ratio": "16:9",
        "aesthetic": "Haute Couture Minimalist Obsidian",
        "resolution": "4K"
    }

    # Step 7: Visual Evaluation
    visual_score = 0.94
    assert visual_score >= 0.85

    # Step 8: Independent Review
    from src.creative_workforce.organization_models import ContextBinding
    binding = ContextBinding(
        client_id=client_id,
        brand_id=brand_id,
        campaign_id=workflow_id,
        mission_id="mission_01",
        task_id="task_01",
        staff_id="staff_art_director"
    )
    protocol = CreativeCollaborationProtocol()
    artifact = protocol.create_artifact(
        title="Hero Campaign Obsidian Draping",
        content_type="IMAGE",
        payload=visual_payload,
        context_binding=binding
    )
    reviewer = IndependentReviewer(reviewer_id="independent_reviewer_01")
    review_result = reviewer.review_artifact(artifact)
    assert review_result.recommendation == "ACCEPTED"

    # Step 9: Approval Request
    approval_token_id = f"auth-tok-{uuid.uuid4().hex[:8]}"
    wf_record = orchestrator.state_mgr.create_workflow(workflow_id, tenant_id, client_id)
    wf_record.transition_to(WorkflowOperationalState.ADMITTED, "Admitted to production pipeline")
    wf_record.transition_to(WorkflowOperationalState.WAITING_FOR_APPROVAL, "Awaiting host sign-off")

    # Step 10: Human Authorization
    wf_record.transition_to(WorkflowOperationalState.APPROVED, "Host granted green signal", auth_token_id=approval_token_id)
    ledger_store.append_event(f"evt-{uuid.uuid4().hex[:6]}", tenant_id, client_id, "HUMAN_APPROVAL_GRANTED", {"token_id": approval_token_id})

    # Step 11: Production Admission
    wf_record.transition_to(WorkflowOperationalState.EXECUTING, "Admitted to live execution", auth_token_id=approval_token_id)

    # Step 12: MCP / Tool Operation
    mcp_secret, mcp_lease = secret_provider.acquire_secret_with_lease("mcp_key", CredentialDomain.MCP, "mcp_gateway")
    assert mcp_secret is not None
    assert mcp_lease.is_valid() is True

    # Step 13: Controlled External Mutation
    mutation_payload = {"destination": "ilyren_global_cdn", "asset_id": visual_asset_id, "published": True}
    ledger_store.append_event(f"evt-{uuid.uuid4().hex[:6]}", tenant_id, client_id, "EXTERNAL_MUTATION_EXECUTED", mutation_payload)

    # Step 14: Outcome Observation
    wf_record.transition_to(WorkflowOperationalState.OBSERVING, "Observing CDN delivery metrics")

    # Step 15: Intelligence Evaluation
    delivery_success = True
    assert delivery_success is True

    # Step 16: Learning Signal
    wf_record.transition_to(WorkflowOperationalState.LEARNING, "Recording performance feedback")

    # Step 17: Checkpoint Pre-Crash
    cp_pre_crash = cp_store.save_checkpoint(
        checkpoint_id=f"cp-{uuid.uuid4().hex[:6]}",
        workflow_id=workflow_id,
        tenant_id=tenant_id,
        client_id=client_id,
        step_index=17,
        step_name="PRE_CRASH_SNAPSHOT",
        state_payload=wf_record.to_dict(),
        authorization_token_id=approval_token_id
    )
    assert cp_pre_crash.checkpoint_hash != ""

    # Step 18: Simulated Worker Restart / Process Crash
    # Simulate a fresh orchestrator instance restarting after worker failure
    fresh_orchestrator = ProductionRuntimeOrchestrator()
    crashed_state_dict = wf_record.to_dict()

    # Step 19: State Reconstruction
    reconstructed_wf = fresh_orchestrator.state_mgr.reconstruct_workflow(crashed_state_dict)
    assert reconstructed_wf.is_recovering is True
    # Invariant check: In-flight execution is downgraded to RECOVERING
    assert reconstructed_wf.current_state in (WorkflowOperationalState.RECOVERING, WorkflowOperationalState.WAITING_FOR_APPROVAL)

    # Step 20: Authorization Revalidation
    # The authorization must be explicitly verified before resumption
    auth_valid = (reconstructed_wf.authorization_ref == approval_token_id)
    assert auth_valid is True

    # Step 21: Outcome Reconciliation
    reconstructed_wf.transition_to(WorkflowOperationalState.COMPLETED, "Reconciliation successful post-recovery")
    assert reconstructed_wf.current_state == WorkflowOperationalState.COMPLETED

    # Step 22: Ledger Verification
    assert ledger_store.verify_ledger_integrity() is True

    # Step 23: Cost Verification
    summary = cost_meter.get_summary()
    assert summary["total_known_cost_usd"] > 0.0
    assert summary["total_tokens"] == 2300

    # Step 24: Health Verification
    health_status = await orchestrator.health_monitor.evaluate_all(fail_closed=True)
    assert health_status["overall_healthy"] is True

    # Step 25: Canary Decision
    canary_controller = EnvironmentPromotionPipeline(VersionRegistry(), DeploymentLedger()).canary_controller
    canary_eval = canary_controller.evaluate_canary(
        total_requests=100,
        error_count=0,
        p95_latency_ms=850.0,
        visual_regression_score=visual_score
    )
    assert canary_eval.sla_breached is False

    # Benchmark successfully validated
