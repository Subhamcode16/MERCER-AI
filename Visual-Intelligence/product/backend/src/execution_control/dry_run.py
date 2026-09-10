"""
Phase 10 — Dry-Run Engine & Execution Plan Generator

Generates deterministic ExecutionPlan objects and formatted Markdown briefs,
exposing intended actions, capabilities, scopes, and side-effects WITHOUT invoking side-effect adapters.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

from src.execution_control.action_models import ExecutionAction
from src.execution_control.approval import ApprovalState
from src.execution_control.exceptions import DryRunSideEffectError


@dataclass(frozen=True)
class ExecutionPlan:
    """Deterministic Dry-Run simulation output."""

    plan_id: str
    workflow_id: str
    actions: List[ExecutionAction]
    required_capabilities: List[str]
    resource_scopes: List[str]
    target_systems: List[str]
    planned_effects: List[Dict[str, Any]]
    rollback_availability: Dict[str, bool]
    approval_status: ApprovalState
    markdown_brief: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "workflow_id": self.workflow_id,
            "actions": [a.to_dict() for a in self.actions],
            "required_capabilities": self.required_capabilities,
            "resource_scopes": self.resource_scopes,
            "target_systems": self.target_systems,
            "planned_effects": self.planned_effects,
            "rollback_availability": self.rollback_availability,
            "approval_status": self.approval_status.value,
            "markdown_brief": self.markdown_brief,
            "created_at": self.created_at,
        }


class DryRunEngine:
    """Side-Effect-Free Dry-Run simulation engine."""

    def __init__(self):
        pass

    def generate_plan(
        self,
        workflow_id: str,
        actions: List[ExecutionAction],
        active_approval_state: ApprovalState = ApprovalState.APPROVED_FOR_DRY_RUN,
    ) -> ExecutionPlan:
        """Generates an ExecutionPlan without triggering any real side-effects."""

        plan_id = f"plan_dryrun_{workflow_id}"
        req_caps = sorted(list(set(a.capability.value for a in actions)))
        res_scopes = sorted(list(set(a.resource_scope.scope_string for a in actions)))
        target_systems = sorted(list(set(a.planned_effect.target_system for a in actions)))

        planned_effects = [a.planned_effect.to_dict() for a in actions]
        rollback_avail = {a.action_id: a.planned_effect.reversible for a in actions}

        # Build formatted Markdown brief
        brief_lines = [
            f"# Execution Plan Dry-Run Simulation Brief",
            f"**Plan ID:** `{plan_id}` | **Workflow ID:** `{workflow_id}`",
            f"**Approval Status:** `{active_approval_state.value}`",
            f"",
            f"## Required Capabilities ({len(req_caps)})",
        ]
        for cap in req_caps:
            brief_lines.append(f"- `{cap}`")

        brief_lines.extend([
            f"",
            f"## Target Systems & Resources",
        ])
        for scope in res_scopes:
            brief_lines.append(f"- Resource Scope: `{scope}`")

        brief_lines.extend([
            f"",
            f"## Planned Actions & Side-Effects ({len(actions)})",
        ])
        for idx, act in enumerate(actions, 1):
            brief_lines.append(
                f"{idx}. **[{act.capability.value}]** on `{act.resource_scope.scope_string}` -> "
                f"Effect: *{act.planned_effect.description}* (Target: `{act.planned_effect.target_system}`, Reversible: `{act.planned_effect.reversible}`)"
            )

        markdown_brief = "\n".join(brief_lines)

        return ExecutionPlan(
            plan_id=plan_id,
            workflow_id=workflow_id,
            actions=actions,
            required_capabilities=req_caps,
            resource_scopes=res_scopes,
            target_systems=target_systems,
            planned_effects=planned_effects,
            rollback_availability=rollback_avail,
            approval_status=active_approval_state,
            markdown_brief=markdown_brief,
        )
