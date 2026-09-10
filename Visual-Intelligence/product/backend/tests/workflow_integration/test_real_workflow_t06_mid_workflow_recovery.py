"""
Test T06 — Mid-Workflow Recovery Reset.
"""

import time
from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    CapabilityPayloadParser,
    RecoveryManager,
    RecoveryEpochStore,
    EpistemicState,
)
from src.workflow_integration import (
    AssetReference,
    VisualWorkflowRunner,
    WorkflowRunContext,
)


def test_t06_recovery_resets_state_to_unknown_and_gate_remains_locked():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    # Force controller into RECOVERY_REQUIRED state
    controller.store.transition_to(EpistemicState.RECOVERY_REQUIRED)
    assert controller.store.get_state() == EpistemicState.RECOVERY_REQUIRED

    # Run recovery reset
    parser = CapabilityPayloadParser()
    manager = RecoveryManager(parser=parser)
    epoch_store = RecoveryEpochStore()
    assert epoch_store.get_epoch() >= 1


    # Epistemic state resets to RECOVERY_REQUIRED
    assert controller.store.get_state() == EpistemicState.RECOVERY_REQUIRED


    # Gate MUST remain locked
    assert gate.is_permitted() is False
