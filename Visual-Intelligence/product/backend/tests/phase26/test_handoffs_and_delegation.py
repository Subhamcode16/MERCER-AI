"""
Phase 26 Unit Tests: Governed Handoffs & Bounded Delegation.
"""
import pytest
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus
from src.creative_workforce.capability_binding.manifest import (
    CapabilityManifest,
    CapabilityResolver,
)
from src.creative_workforce.handoffs.handoff_service import (
    HandoffService,
    HandoffStatus,
    HandoffError,
)
from src.creative_workforce.delegation.delegation_engine import (
    DelegationEngine,
    DelegationLimitReached,
    DelegationError,
)


def test_handoff_lifecycle_and_artifact_hash_verification():
    resolver = CapabilityResolver()
    resolver.register_manifest(
        CapabilityManifest(
            worker_id="visual_01",
            allowed_capabilities={"render.request", "visual_dna.read"},
        )
    )

    recipient = WorkerIdentity(
        worker_id="visual_01",
        tenant_id="tenant_alpha",
        organization_id="org_1",
        name="Visual Worker",
        role_id="ART_DIRECTION",
        description="Art Director",
        status=WorkerStatus.ACTIVE,
    )

    service = HandoffService(capability_resolver=resolver)
    handoff = service.create_handoff(
        room_id="room_123",
        tenant_id="tenant_alpha",
        client_id="client_haute",
        sender_worker_id="cd_01",
        recipient_worker_id="visual_01",
        purpose="Generate visual prompts based on creative direction",
        input_artifacts=[{"artifact_id": "moodboard_01", "tokens": ["minimalism", "silk"]}],
        requested_action="render.request",
    )
    assert handoff.status == HandoffStatus.PENDING
    assert "moodboard_01" in handoff.artifact_hashes

    # Accept handoff
    accepted = service.accept_handoff(handoff.handoff_id, recipient=recipient)
    assert accepted.status == HandoffStatus.ACCEPTED


def test_delegation_engine_depth_limit_and_loop_prevention():
    engine = DelegationEngine(default_max_depth=3)

    w1 = WorkerIdentity(worker_id="w1", tenant_id="tenant_alpha", organization_id="org_1", name="W1", role_id="STRATEGY_DIRECTOR", description="1", status=WorkerStatus.ACTIVE)
    w2 = WorkerIdentity(worker_id="w2", tenant_id="tenant_alpha", organization_id="org_1", name="W2", role_id="CREATIVE_DIRECTOR", description="2", status=WorkerStatus.ACTIVE)
    w3 = WorkerIdentity(worker_id="w3", tenant_id="tenant_alpha", organization_id="org_1", name="W3", role_id="ART_DIRECTION", description="3", status=WorkerStatus.ACTIVE)
    w4 = WorkerIdentity(worker_id="w4", tenant_id="tenant_alpha", organization_id="org_1", name="W4", role_id="QUALITY_REVIEWER", description="4", status=WorkerStatus.ACTIVE)

    # Initial delegation: Human -> W1 (Depth 2: [human, w1])
    task = engine.initiate_delegation(
        tenant_id="tenant_alpha",
        client_id="client_haute",
        initiator_id="human_director",
        target_worker=w1,
        task_payload={"goal": "Develop Campaign"},
        max_depth=3,
    )
    assert len(task.delegation_chain) == 2

    # Delegate further: W1 -> W2 (Depth 3: [human, w1, w2])
    engine.delegate_further(task.delegation_id, sender_worker=w1, target_worker=w2)
    assert len(task.delegation_chain) == 3

    # Delegate loop: W2 -> W1 -> REJECTED
    with pytest.raises(DelegationError):
        engine.delegate_further(task.delegation_id, sender_worker=w2, target_worker=w1)

    # Delegate further: W2 -> W3 -> REJECTED due to depth limit
    with pytest.raises(DelegationLimitReached):
        engine.delegate_further(task.delegation_id, sender_worker=w2, target_worker=w3)
