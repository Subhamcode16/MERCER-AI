"""
Phase 25 Campaign Command Center Tests.
"""
import pytest
from src.control_plane.models import OperatorRole
from src.control_plane.context import OperatorContext
from src.control_plane.exceptions import StaleActionConflictError
from src.campaign_command.campaign_projection import DetailedCampaignState, CampaignDetailedProjection
from src.campaign_command.dependency_view import DependencyNode, DependencyGraphViewer
from src.campaign_command.campaign_actions import CampaignActionService

def test_campaign_state_machine_and_optimistic_locking():
    action_service = CampaignActionService()
    cmp = CampaignDetailedProjection(
        campaign_id="cmp-silk-001",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        name="Autumn Silk",
        objective={"kpi": "Affinity"},
        state=DetailedCampaignState.REVIEW_REQUIRED,
        version=1
    )
    action_service.register_campaign(cmp)

    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )

    # Transition with correct expected version
    updated = action_service.transition_campaign_state(
        context=ctx,
        campaign_id="cmp-silk-001",
        target_state=DetailedCampaignState.APPROVAL_REQUIRED,
        expected_version=1,
        reason="Critique passed"
    )
    assert updated.state == DetailedCampaignState.APPROVAL_REQUIRED
    assert updated.version == 2

    # Attempt transition with stale expected version (e.g. 1 instead of 2) -> 409 Conflict
    with pytest.raises(StaleActionConflictError):
        action_service.transition_campaign_state(
            context=ctx,
            campaign_id="cmp-silk-001",
            target_state=DetailedCampaignState.AUTHORIZED,
            expected_version=1,
            reason="Stale action"
        )

def test_dependency_graph_readiness_evaluation():
    node_a = DependencyNode(node_id="task_strategy", label="Strategy", node_type="TASK")
    node_b = DependencyNode(node_id="task_visual", label="Visual Gen", node_type="TASK", prerequisites={"task_strategy"})
    node_c = DependencyNode(node_id="approval_gate", label="Human Auth", node_type="APPROVAL", prerequisites={"task_strategy", "task_visual"})

    completed = {"task_strategy"}
    assert DependencyGraphViewer.evaluate_readiness(node_b, completed) is True
    assert DependencyGraphViewer.evaluate_readiness(node_c, completed) is False

    completed.add("task_visual")
    assert DependencyGraphViewer.evaluate_readiness(node_c, completed) is True
