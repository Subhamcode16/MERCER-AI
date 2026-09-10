"""
Tests for Phase 23 Production Runtime Subsystem.
"""
import pytest
import asyncio
from src.production_runtime.runtime_models import (
    RuntimeTask,
    QueuePriority,
    WorkflowOperationalState,
    WorkerStatus
)
from src.production_runtime.runtime_orchestrator import ProductionRuntimeOrchestrator
from src.production_runtime.exceptions import (
    WorkerLimitExceededError,
    QueueCapacityError,
    InvalidStateTransitionError,
    DependencyUnhealthyError
)

@pytest.mark.asyncio
async def test_runtime_phased_startup_and_shutdown():
    orchestrator = ProductionRuntimeOrchestrator(max_global_workers=4, max_tenant_workers=2)
    
    # Register mock healthy dependency probe
    async def mock_db_probe():
        return True
    orchestrator.health_monitor.register_probe("database", mock_db_probe, is_critical=True)

    start_res = await orchestrator.start(verify_dependencies=True)
    assert start_res["success"] is True
    assert len(start_res["stages_completed"]) == 5
    assert start_res["status"] == "RUNNING"

    snapshot = orchestrator.get_snapshot()
    assert snapshot.idle_workers == 4
    assert snapshot.active_workers == 0

    stop_res = await orchestrator.stop()
    assert stop_res["success"] is True
    assert stop_res["final_status"] == "STOPPED"

@pytest.mark.asyncio
async def test_worker_tenant_concurrency_quota():
    orchestrator = ProductionRuntimeOrchestrator(max_global_workers=8, max_tenant_workers=2)
    
    t1 = RuntimeTask("t-1", "tenant-alpha", "client-1", "camp-1", "m-1", "action-1", {})
    t2 = RuntimeTask("t-2", "tenant-alpha", "client-1", "camp-1", "m-1", "action-2", {})
    t3 = RuntimeTask("t-3", "tenant-alpha", "client-1", "camp-1", "m-1", "action-3", {})

    w1 = orchestrator.worker_mgr.allocate_worker("tenant-alpha", t1)
    w2 = orchestrator.worker_mgr.allocate_worker("tenant-alpha", t2)
    assert w1 is not None
    assert w2 is not None

    # Third allocation for same tenant must breach quota
    with pytest.raises(WorkerLimitExceededError):
        orchestrator.worker_mgr.allocate_worker("tenant-alpha", t3)

    # Release one worker
    orchestrator.worker_mgr.release_worker(w1.worker_id)
    w3 = orchestrator.worker_mgr.allocate_worker("tenant-alpha", t3)
    assert w3 is not None

@pytest.mark.asyncio
async def test_priority_queue_and_dlq():
    orchestrator = ProductionRuntimeOrchestrator(max_queue_capacity=5)
    
    task_norm = RuntimeTask("task-norm", "t-1", "c-1", "camp-1", "m-1", "norm", {}, priority=QueuePriority.NORMAL)
    task_crit = RuntimeTask("task-crit", "t-1", "c-1", "camp-1", "m-1", "crit", {}, priority=QueuePriority.CRITICAL)

    await orchestrator.queue_runtime.enqueue(task_norm)
    await orchestrator.queue_runtime.enqueue(task_crit)

    # Critical task should be dequeued first
    dequeued_1 = await orchestrator.queue_runtime.dequeue()
    assert dequeued_1.task_id == "task-crit"

    # Route task to DLQ
    orchestrator.queue_runtime.route_to_dead_letter(task_norm, failure_reason="Max retries exhausted")
    assert orchestrator.queue_runtime.dead_letter_depth == 1

@pytest.mark.asyncio
async def test_state_machine_strict_transition_rules():
    orchestrator = ProductionRuntimeOrchestrator()
    wf = orchestrator.state_mgr.create_workflow("wf-101", "tenant-1", "client-1")
    assert wf.current_state == WorkflowOperationalState.CREATED

    # Valid: CREATED -> ADMITTED
    wf.transition_to(WorkflowOperationalState.ADMITTED, reason="Admitted to queue")
    assert wf.current_state == WorkflowOperationalState.ADMITTED

    # Valid: ADMITTED -> WAITING_FOR_APPROVAL
    wf.transition_to(WorkflowOperationalState.WAITING_FOR_APPROVAL, reason="Awaiting human sign-off")
    assert wf.current_state == WorkflowOperationalState.WAITING_FOR_APPROVAL

    # Invalid: WAITING_FOR_APPROVAL -> EXECUTING directly without approval/token
    with pytest.raises(InvalidStateTransitionError):
        wf.transition_to(WorkflowOperationalState.EXECUTING, reason="Unauthorized bypass")

    # Valid: WAITING_FOR_APPROVAL -> APPROVED -> EXECUTING (with token)
    wf.transition_to(WorkflowOperationalState.APPROVED, reason="Host approved", auth_token_id="tok-valid-99")
    wf.transition_to(WorkflowOperationalState.EXECUTING, reason="Starting execution", auth_token_id="tok-valid-99")
    assert wf.current_state == WorkflowOperationalState.EXECUTING
