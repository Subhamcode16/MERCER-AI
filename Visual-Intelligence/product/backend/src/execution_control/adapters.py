"""
Phase 10 — In-Memory Sandbox Adapters

Provides isolated, mock integration adapters operating with zero external network or credential dependencies.
Records deterministic execution transaction IDs and structured return payloads.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional

from src.execution_control.action_models import ExecutionAction
from src.execution_control.capability_models import ExecutionCapability


@dataclass(frozen=True)
class AdapterExecutionResult:
    """Result object returned by a sandbox integration adapter."""

    transaction_id: str
    action_id: str
    capability: ExecutionCapability
    success: bool
    output_data: Dict[str, Any]
    error_message: Optional[str] = None
    executed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class BaseSandboxAdapter(ABC):
    """Abstract base class for all in-memory sandbox integration adapters."""

    @abstractmethod
    def supported_capabilities(self) -> List[ExecutionCapability]:
        """Returns list of capabilities supported by this adapter."""
        pass

    @abstractmethod
    def execute_action(self, action: ExecutionAction) -> AdapterExecutionResult:
        """Executes an action in sandbox mode."""
        pass


class SocialPlatformAdapter(BaseSandboxAdapter):
    """Mock sandbox adapter for social platform publishing and scheduling."""

    def __init__(self):
        self.published_posts: List[Dict[str, Any]] = []
        self.scheduled_posts: List[Dict[str, Any]] = []

    def supported_capabilities(self) -> List[ExecutionCapability]:
        return [ExecutionCapability.PUBLISH_CONTENT, ExecutionCapability.SCHEDULE_CONTENT]

    def execute_action(self, action: ExecutionAction) -> AdapterExecutionResult:
        tx_id = f"tx_social_{uuid.uuid4().hex[:8]}"

        if action.capability == ExecutionCapability.PUBLISH_CONTENT:
            post_record = {
                "tx_id": tx_id,
                "action_id": action.action_id,
                "scope": action.resource_scope.scope_string,
                "payload": action.input_payload,
                "status": "PUBLISHED_IN_SANDBOX",
            }
            self.published_posts.append(post_record)
            return AdapterExecutionResult(
                transaction_id=tx_id,
                action_id=action.action_id,
                capability=action.capability,
                success=True,
                output_data={"post_id": f"sandbox_post_{len(self.published_posts)}", "status": "PUBLISHED"},
            )

        elif action.capability == ExecutionCapability.SCHEDULE_CONTENT:
            sched_record = {
                "tx_id": tx_id,
                "action_id": action.action_id,
                "scope": action.resource_scope.scope_string,
                "payload": action.input_payload,
                "status": "SCHEDULED_IN_SANDBOX",
            }
            self.scheduled_posts.append(sched_record)
            return AdapterExecutionResult(
                transaction_id=tx_id,
                action_id=action.action_id,
                capability=action.capability,
                success=True,
                output_data={"schedule_id": f"sandbox_sched_{len(self.scheduled_posts)}", "status": "SCHEDULED"},
            )

        return AdapterExecutionResult(
            transaction_id=tx_id,
            action_id=action.action_id,
            capability=action.capability,
            success=False,
            output_data={},
            error_message=f"Unsupported capability {action.capability}",
        )


class AssetStorageAdapter(BaseSandboxAdapter):
    """Mock sandbox adapter for asset storage and generation."""

    def __init__(self):
        self.stored_assets: Dict[str, Dict[str, Any]] = {}

    def supported_capabilities(self) -> List[ExecutionCapability]:
        return [ExecutionCapability.GENERATE_ASSET, ExecutionCapability.MODIFY_BRAND_ASSETS]

    def execute_action(self, action: ExecutionAction) -> AdapterExecutionResult:
        tx_id = f"tx_asset_{uuid.uuid4().hex[:8]}"
        asset_id = f"sandbox_asset_{uuid.uuid4().hex[:6]}"

        self.stored_assets[asset_id] = {
            "tx_id": tx_id,
            "action_id": action.action_id,
            "scope": action.resource_scope.scope_string,
            "payload": action.input_payload,
        }

        return AdapterExecutionResult(
            transaction_id=tx_id,
            action_id=action.action_id,
            capability=action.capability,
            success=True,
            output_data={"asset_id": asset_id, "url": f"sandbox://assets/{asset_id}"},
        )


class ContentManagementAdapter(BaseSandboxAdapter):
    """Mock sandbox adapter for draft content management."""

    def __init__(self):
        self.drafts: Dict[str, Dict[str, Any]] = {}

    def supported_capabilities(self) -> List[ExecutionCapability]:
        return [
            ExecutionCapability.CREATE_DRAFT,
            ExecutionCapability.EDIT_DRAFT,
            ExecutionCapability.DELETE_CONTENT,
        ]

    def execute_action(self, action: ExecutionAction) -> AdapterExecutionResult:
        tx_id = f"tx_cms_{uuid.uuid4().hex[:8]}"

        if action.capability == ExecutionCapability.CREATE_DRAFT:
            draft_id = f"sandbox_draft_{len(self.drafts) + 1}"
            self.drafts[draft_id] = {
                "action_id": action.action_id,
                "scope": action.resource_scope.scope_string,
                "payload": action.input_payload,
            }
            return AdapterExecutionResult(
                transaction_id=tx_id,
                action_id=action.action_id,
                capability=action.capability,
                success=True,
                output_data={"draft_id": draft_id, "status": "DRAFT_CREATED"},
            )

        elif action.capability == ExecutionCapability.EDIT_DRAFT:
            draft_id = action.input_payload.get("draft_id", "draft_unknown")
            self.drafts[draft_id] = {
                "action_id": action.action_id,
                "scope": action.resource_scope.scope_string,
                "payload": action.input_payload,
            }
            return AdapterExecutionResult(
                transaction_id=tx_id,
                action_id=action.action_id,
                capability=action.capability,
                success=True,
                output_data={"draft_id": draft_id, "status": "DRAFT_UPDATED"},
            )

        elif action.capability == ExecutionCapability.DELETE_CONTENT:
            content_id = action.input_payload.get("content_id", "content_unknown")
            self.drafts.pop(content_id, None)
            return AdapterExecutionResult(
                transaction_id=tx_id,
                action_id=action.action_id,
                capability=action.capability,
                success=True,
                output_data={"content_id": content_id, "status": "CONTENT_DELETED"},
            )

        return AdapterExecutionResult(
            transaction_id=tx_id,
            action_id=action.action_id,
            capability=action.capability,
            success=False,
            output_data={},
            error_message="Unsupported capability",
        )


class AnalyticsAdapter(BaseSandboxAdapter):
    """Mock sandbox adapter for reading campaign analytics."""

    def supported_capabilities(self) -> List[ExecutionCapability]:
        return [ExecutionCapability.READ_ANALYTICS]

    def execute_action(self, action: ExecutionAction) -> AdapterExecutionResult:
        tx_id = f"tx_analytics_{uuid.uuid4().hex[:8]}"
        return AdapterExecutionResult(
            transaction_id=tx_id,
            action_id=action.action_id,
            capability=action.capability,
            success=True,
            output_data={
                "impressions": 15400,
                "engagement_rate": 0.048,
                "reach": 12100,
                "conversions": 340,
            },
        )
