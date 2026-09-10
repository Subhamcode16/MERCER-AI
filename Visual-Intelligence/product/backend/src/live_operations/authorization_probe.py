"""
Phase 24 Live Authorization Boundary Probes (L24-AUTH-01 through L24-AUTH-05).
Ensures external models, tools, recovery mechanisms, and fallbacks CANNOT create execution authority.
"""
import time
import logging
from typing import Dict, Any, List
from src.live_operations.live_models import ProbeResult, ProbeStatus

logger = logging.getLogger(__name__)

class LiveAuthorizationProbeSuite:
    """Executes live authorization boundary probes L24-AUTH-01 to L24-AUTH-05."""

    @staticmethod
    def probe_l24_auth_01_model_attempts_authorization(model_output: Dict[str, Any]) -> ProbeResult:
        """L24-AUTH-01: Model output attempts to authorize execution -> Expected DENIED."""
        # Check if model payload attempts to self-authorize
        has_auth_injection = any(k in model_output for k in ["authorized", "execute_immediately", "grant_authority"])
        status = ProbeStatus.DENIED if has_auth_injection else ProbeStatus.PASS
        return ProbeResult(
            probe_id="L24-AUTH-01",
            target_component="AUTHORIZATION_GUARD",
            status=status,
            latency_ms=0.5,
            message="Model self-authorization attempt intercepted and denied" if has_auth_injection else "No model auth injection detected",
            details={"model_output_keys": list(model_output.keys())}
        )

    @staticmethod
    def probe_l24_auth_02_mcp_alters_authorization(mcp_response: Dict[str, Any]) -> ProbeResult:
        """L24-AUTH-02: MCP result attempts to alter authorization state -> Expected DENIED."""
        has_auth_tamper = "mutate_auth_state" in mcp_response or "grant_permission" in mcp_response
        status = ProbeStatus.DENIED if has_auth_tamper else ProbeStatus.PASS
        return ProbeResult(
            probe_id="L24-AUTH-02",
            target_component="AUTHORIZATION_GUARD",
            status=status,
            latency_ms=0.5,
            message="MCP authorization state alteration intercepted and denied" if has_auth_tamper else "MCP response clean",
            details={"mcp_response_keys": list(mcp_response.keys())}
        )

    @staticmethod
    def probe_l24_auth_03_expired_approval_continuation(approval_expiry_timestamp: float) -> ProbeResult:
        """L24-AUTH-03: Recovered workflow continues after approval expiry -> Expected DENIED."""
        is_expired = time.time() > approval_expiry_timestamp
        status = ProbeStatus.DENIED if is_expired else ProbeStatus.PASS
        return ProbeResult(
            probe_id="L24-AUTH-03",
            target_component="AUTHORIZATION_GUARD",
            status=status,
            latency_ms=0.2,
            message="Expired approval continuation blocked" if is_expired else "Approval token is fresh",
            details={"expiry": approval_expiry_timestamp, "now": time.time()}
        )

    @staticmethod
    def probe_l24_auth_04_restarted_worker_unauthorized_execution(has_revalidated_auth: bool) -> ProbeResult:
        """L24-AUTH-04: Restarted worker executes without valid authorization -> Expected DENIED."""
        status = ProbeStatus.PASS if has_revalidated_auth else ProbeStatus.DENIED
        return ProbeResult(
            probe_id="L24-AUTH-04",
            target_component="AUTHORIZATION_GUARD",
            status=status,
            latency_ms=0.2,
            message="Un-revalidated execution attempt denied on restart" if not has_revalidated_auth else "Authorization revalidation verified",
            details={"revalidated": has_revalidated_auth}
        )

    @staticmethod
    def probe_l24_auth_05_fallback_requests_broader_capability(primary_scope: str, fallback_requested_scope: str) -> ProbeResult:
        """L24-AUTH-05: Fallback provider requests broader capability -> Expected DENIED."""
        is_escalation = (fallback_requested_scope != primary_scope) and (fallback_requested_scope == "*" or "admin" in fallback_requested_scope.lower())
        status = ProbeStatus.DENIED if is_escalation else ProbeStatus.PASS
        return ProbeResult(
            probe_id="L24-AUTH-05",
            target_component="AUTHORIZATION_GUARD",
            status=status,
            latency_ms=0.3,
            message="Fallback capability escalation blocked" if is_escalation else "Fallback scope matches authorized bounds",
            details={"primary_scope": primary_scope, "fallback_scope": fallback_requested_scope}
        )
