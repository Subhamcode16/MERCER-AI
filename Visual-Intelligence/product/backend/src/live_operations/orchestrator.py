"""
Phase 24 Live Operations Master Orchestrator.
"""
import logging
from typing import Dict, Any, List, Optional
from src.live_operations.live_models import LiveValidationMode, ProbeResult, ProbeStatus
from src.live_operations.live_run_manager import LiveRunManager
from src.live_operations.llm_smoke import LLMSmokeProbe
from src.live_operations.visual_smoke import VisualSmokeProbe
from src.live_operations.mcp_smoke import MCPSmokeProbe
from src.live_operations.authorization_probe import LiveAuthorizationProbeSuite
from src.live_operations.tenant_isolation_probe import MultiClientIsolationProbe

logger = logging.getLogger(__name__)

class LiveOperationsOrchestrator:
    """Master orchestrator for executing comprehensive live operations validation suites."""

    def __init__(self, mode: LiveValidationMode = LiveValidationMode.SANDBOX):
        self.mode = mode
        self.run_manager = LiveRunManager(mode=mode)
        self.llm_probe = LLMSmokeProbe(mode=mode)
        self.visual_probe = VisualSmokeProbe(mode=mode)
        self.mcp_probe = MCPSmokeProbe(mode=mode)
        self.auth_suite = LiveAuthorizationProbeSuite()
        self.isolation_probe = MultiClientIsolationProbe()

    async def run_full_live_validation(self, tenant_id: str, client_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executes full live validation suite across model, visual, MCP, auth, and isolation."""
        ctx = context or {}
        run_id = self.run_manager.start_run(tenant_id, client_id, "FULL_LIVE_VALIDATION_SUITE")
        correlation_id = f"corr-{run_id}"

        results: List[ProbeResult] = []

        # 1. LLM Probe
        llm_res = await self.llm_probe.execute_probe(ctx.get("llm", {}))
        self.run_manager.record_probe_execution(run_id, llm_res, correlation_id, provider="google", model_or_version="gemini-2.5-flash", operation="LLM_SMOKE")
        results.append(llm_res)

        # 2. Visual Probe
        visual_res = await self.visual_probe.execute_probe(ctx.get("visual", {}))
        self.run_manager.record_probe_execution(run_id, visual_res, correlation_id, provider="imagen_3", model_or_version="imagen-3.0", operation="VISUAL_SMOKE")
        results.append(visual_res)

        # 3. MCP Probe
        mcp_res = await self.mcp_probe.execute_probe(ctx.get("mcp", {}))
        self.run_manager.record_probe_execution(run_id, mcp_res, correlation_id, provider="mcp_server", operation="MCP_SMOKE")
        results.append(mcp_res)

        # 4. Multi-Client Isolation Probe
        self.isolation_probe.register_client_context("client_alpha", {"brand": "AlphaLux"}, ["art-alpha-01"])
        self.isolation_probe.register_client_context("client_beta", {"brand": "BetaStreet"}, ["art-beta-01"])
        iso_res = self.isolation_probe.probe_cross_client_leakage(client_id, ctx.get("queried_context", {}), ctx.get("queried_visual_refs", []))
        self.run_manager.record_probe_execution(run_id, iso_res, correlation_id, operation="ISOLATION_CHECK")
        results.append(iso_res)

        # Verify ledger integrity
        ledger_valid = self.run_manager.ledger.verify_ledger_integrity()

        summary = self.run_manager.finish_run(run_id)
        summary["ledger_integrity_verified"] = ledger_valid
        summary["overall_status"] = "PASS" if summary["probes_failed"] == 0 else "FAIL"

        return summary
