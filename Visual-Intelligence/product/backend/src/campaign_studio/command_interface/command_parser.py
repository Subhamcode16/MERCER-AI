"""
Phase 27 Studio Command Interface & Directive Parser.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import re
import uuid

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


class ParsedCommandType(str, Enum):
    SYNTHESIZE = "SYNTHESIZE"
    DISCOVER = "DISCOVER"
    SELECT_DIRECTION = "SELECT_DIRECTION"
    REFINE_DIRECTION = "REFINE_DIRECTION"
    GENERATE_ASSETS = "GENERATE_ASSETS"
    REVIEW_ASSET = "REVIEW_ASSET"
    REQUEST_APPROVAL = "REQUEST_APPROVAL"
    DECIDE_APPROVAL = "DECIDE_APPROVAL"
    STAGE_LAUNCH = "STAGE_LAUNCH"
    EXECUTE_LAUNCH = "EXECUTE_LAUNCH"
    UNKNOWN = "UNKNOWN"


@dataclass
class StudioCommandResult:
    command_id: str
    command_type: ParsedCommandType
    raw_input: str
    is_authorized: bool
    status: str  # "SUCCESS", "DENIED", "ERROR", "SYNTAX_ERROR"
    message: str
    payload: Dict[str, Any] = field(default_factory=dict)


class StudioCommandParser:
    """Parses studio slash commands and natural language directives with strict RBAC enforcement."""

    def parse_and_validate(
        self,
        raw_text: str,
        operator: OperatorContext,
        campaign_id: Optional[str] = None,
    ) -> StudioCommandResult:
        cmd = raw_text.strip()
        command_id = f"cmd_{uuid.uuid4().hex[:8]}"

        if cmd.startswith("/synthesize") or "synthesize intelligence" in cmd.lower():
            return StudioCommandResult(
                command_id=command_id,
                command_type=ParsedCommandType.SYNTHESIZE,
                raw_input=raw_text,
                is_authorized=True,
                status="SUCCESS",
                message="Synthesizing creative intelligence and market signals.",
                payload={"campaign_id": campaign_id},
            )

        if cmd.startswith("/direction select") or "select direction" in cmd.lower():
            # Extract direction id
            match = re.search(r"select\s+([a-zA-Z0-9_\-]+)", cmd, re.IGNORECASE)
            direction_id = match.group(1) if match else "dir_default"
            return StudioCommandResult(
                command_id=command_id,
                command_type=ParsedCommandType.SELECT_DIRECTION,
                raw_input=raw_text,
                is_authorized=True,
                status="SUCCESS",
                message=f"Selected creative direction {direction_id}.",
                payload={"campaign_id": campaign_id, "direction_id": direction_id},
            )

        if cmd.startswith("/render") or "generate assets" in cmd.lower():
            return StudioCommandResult(
                command_id=command_id,
                command_type=ParsedCommandType.GENERATE_ASSETS,
                raw_input=raw_text,
                is_authorized=True,
                status="SUCCESS",
                message="Triggering visual asset draft generation.",
                payload={"campaign_id": campaign_id},
            )

        if cmd.startswith("/approve") or "approve asset" in cmd.lower():
            # Approvals require elevated roles
            authorized_roles = {OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.SUPER_ADMIN}
            if operator.role not in authorized_roles:
                return StudioCommandResult(
                    command_id=command_id,
                    command_type=ParsedCommandType.DECIDE_APPROVAL,
                    raw_input=raw_text,
                    is_authorized=False,
                    status="DENIED",
                    message=f"Operator '{operator.operator_id}' with role '{operator.role}' is not authorized to approve assets. Invariant: Natural Language Command ≠ Permission.",
                    payload={"campaign_id": campaign_id},
                )

            return StudioCommandResult(
                command_id=command_id,
                command_type=ParsedCommandType.DECIDE_APPROVAL,
                raw_input=raw_text,
                is_authorized=True,
                status="SUCCESS",
                message="Submitting formal asset sign-off approval.",
                payload={"campaign_id": campaign_id, "decision": "APPROVED"},
            )

        if cmd.startswith("/launch") or "execute launch" in cmd.lower():
            authorized_roles = {OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.SUPER_ADMIN}
            if operator.role not in authorized_roles:
                return StudioCommandResult(
                    command_id=command_id,
                    command_type=ParsedCommandType.EXECUTE_LAUNCH,
                    raw_input=raw_text,
                    is_authorized=False,
                    status="DENIED",
                    message=f"Operator '{operator.operator_id}' with role '{operator.role}' lacks permission to launch campaign.",
                    payload={"campaign_id": campaign_id},
                )

            return StudioCommandResult(
                command_id=command_id,
                command_type=ParsedCommandType.EXECUTE_LAUNCH,
                raw_input=raw_text,
                is_authorized=True,
                status="SUCCESS",
                message="Campaign launch execution authorized and queued.",
                payload={"campaign_id": campaign_id},
            )

        return StudioCommandResult(
            command_id=command_id,
            command_type=ParsedCommandType.UNKNOWN,
            raw_input=raw_text,
            is_authorized=True,
            status="SYNTAX_ERROR",
            message=f"Unknown command: '{raw_text}'",
            payload={},
        )
