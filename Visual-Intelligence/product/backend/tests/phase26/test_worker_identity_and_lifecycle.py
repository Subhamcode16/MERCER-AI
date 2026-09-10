"""
Phase 26 Unit Tests: Worker Identity & Lifecycle State Machine.
"""
import pytest
from src.creative_workforce.worker_identity.models import (
    WorkerIdentity,
    WorkerStatus,
    WorkerRole,
    RoleIdentity,
    CapabilityIdentity,
    ExecutionIdentity,
    ProvenanceIdentity,
)
from src.creative_workforce.worker_roles.roles import CANONICAL_ROLES, get_role_definition
from src.creative_workforce.worker_lifecycle.lifecycle_engine import (
    WorkerLifecycleManager,
    WorkerLifecycleError,
)
from src.creative_workforce.worker_registry.registry import (
    WorkerRegistry,
    WorkerRegistryError,
)


def test_worker_identity_and_roles():
    role_def = get_role_definition(WorkerRole.CREATIVE_DIRECTOR.value)
    assert role_def.role_id == "CREATIVE_DIRECTOR"
    assert "creative_direction.create" in role_def.default_capabilities

    worker = WorkerIdentity(
        worker_id="cd_01",
        tenant_id="tenant_alpha",
        organization_id="org_luxury",
        name="Elena Rostova",
        role_id=WorkerRole.CREATIVE_DIRECTOR.value,
        description="Lead Creative Director",
        status=WorkerStatus.ACTIVE,
    )
    assert worker.status == WorkerStatus.ACTIVE
    assert worker.worker_id == "cd_01"


def test_worker_lifecycle_transitions():
    worker = WorkerIdentity(
        worker_id="planner_01",
        tenant_id="tenant_alpha",
        organization_id="org_luxury",
        name="Marcus Vance",
        role_id=WorkerRole.CAMPAIGN_PLANNER.value,
        description="Lead Campaign Planner",
        status=WorkerStatus.DRAFT,
    )

    # DRAFT -> ACTIVE
    WorkerLifecycleManager.transition(worker, WorkerStatus.ACTIVE, reason="Onboarding approved")
    assert worker.status == WorkerStatus.ACTIVE
    WorkerLifecycleManager.assert_executable(worker)

    # ACTIVE -> PAUSED
    WorkerLifecycleManager.transition(worker, WorkerStatus.PAUSED, reason="Scheduled maintenance")
    assert worker.status == WorkerStatus.PAUSED
    with pytest.raises(WorkerLifecycleError):
        WorkerLifecycleManager.assert_executable(worker)

    # PAUSED -> ACTIVE
    WorkerLifecycleManager.transition(worker, WorkerStatus.ACTIVE, reason="Maintenance complete")
    assert worker.status == WorkerStatus.ACTIVE

    # ACTIVE -> SUSPENDED
    WorkerLifecycleManager.transition(worker, WorkerStatus.SUSPENDED, reason="Audit investigation")
    assert worker.status == WorkerStatus.SUSPENDED

    # SUSPENDED cannot jump directly to ACTIVE
    with pytest.raises(WorkerLifecycleError):
        WorkerLifecycleManager.transition(worker, WorkerStatus.ACTIVE, reason="Bypass review")

    # SUSPENDED -> RESTRICTED -> ACTIVE
    WorkerLifecycleManager.transition(worker, WorkerStatus.RESTRICTED, reason="Supervised trial")
    WorkerLifecycleManager.transition(worker, WorkerStatus.ACTIVE, reason="Cleared")
    assert worker.status == WorkerStatus.ACTIVE

    # ACTIVE -> RETIRED (Terminal state)
    WorkerLifecycleManager.transition(worker, WorkerStatus.RETIRED, reason="End of lifecycle")
    assert worker.status == WorkerStatus.RETIRED

    with pytest.raises(WorkerLifecycleError):
        WorkerLifecycleManager.transition(worker, WorkerStatus.ACTIVE, reason="Unretire")


def test_worker_registry_tenant_isolation():
    registry = WorkerRegistry()

    w1 = WorkerIdentity(
        worker_id="w_alpha",
        tenant_id="tenant_alpha",
        organization_id="org_1",
        name="Worker Alpha",
        role_id="STRATEGY_DIRECTOR",
        description="Alpha strategist",
    )
    w2 = WorkerIdentity(
        worker_id="w_beta",
        tenant_id="tenant_beta",
        organization_id="org_2",
        name="Worker Beta",
        role_id="STRATEGY_DIRECTOR",
        description="Beta strategist",
    )

    registry.register_worker(w1)
    registry.register_worker(w2)

    # Tenant alpha should only see w1
    alpha_workers = registry.list_workers(tenant_id="tenant_alpha")
    assert len(alpha_workers) == 1
    assert alpha_workers[0].worker_id == "w_alpha"

    # Cross-tenant get_worker returns None
    assert registry.get_worker("w_beta", tenant_id="tenant_alpha") is None
    assert registry.get_worker("w_beta", tenant_id="tenant_beta") is not None
