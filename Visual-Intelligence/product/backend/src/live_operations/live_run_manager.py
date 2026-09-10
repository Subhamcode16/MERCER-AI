"""
Phase 24 Live Run Manager for Multi-Tier Environment Testing.
"""
import uuid
import time
import logging
from typing import Dict, Any, List, Optional
from src.live_operations.live_models import LiveValidationMode, ProbeResult, ProbeStatus, LiveEvidenceRecord
from src.live_operations.evidence_collector import LiveEvidenceCollector
from src.live_operations.live_ledger import LiveOperationsLedger

logger = logging.getLogger(__name__)

class LiveRunManager:
    """Coordinates execution of live validation test runs across environments."""

    def __init__(self, mode: LiveValidationMode = LiveValidationMode.SANDBOX):
        self.mode = mode
        self.collector = LiveEvidenceCollector()
        self.ledger = LiveOperationsLedger()
        self._active_runs: Dict[str, Dict[str, Any]] = {}

    def start_run(self, tenant_id: str, client_id: str, run_name: str) -> str:
        run_id = f"run-{uuid.uuid4().hex[:8]}"
        self._active_runs[run_id] = {
            "run_id": run_id,
            "tenant_id": tenant_id,
            "client_id": client_id,
            "run_name": run_name,
            "environment": self.mode.value,
            "start_time": time.time(),
            "probes_executed": 0,
            "probes_passed": 0,
            "probes_failed": 0
        }
        logger.info(f"Started live validation run {run_id} ({run_name}) in mode {self.mode.value}")
        return run_id

    def record_probe_execution(
        self,
        run_id: str,
        probe_result: ProbeResult,
        correlation_id: str,
        provider: str = "",
        model_or_version: str = "",
        operation: str = "",
        cost_usd: float = 0.0,
        authorization_token_id: Optional[str] = None
    ) -> LiveEvidenceRecord:
        run = self._active_runs.get(run_id, {})
        tenant_id = run.get("tenant_id", "default_tenant")
        client_id = run.get("client_id", "default_client")

        rec = self.collector.create_evidence_record(
            probe_result=probe_result,
            correlation_id=correlation_id,
            tenant_id=tenant_id,
            client_id=client_id,
            provider=provider,
            model_or_version=model_or_version,
            operation=operation,
            cost_usd=cost_usd,
            authorization_token_id=authorization_token_id,
            environment=self.mode
        )
        self.ledger.append_evidence(rec)

        if run:
            run["probes_executed"] += 1
            if probe_result.status == ProbeStatus.PASS:
                run["probes_passed"] += 1
            else:
                run["probes_failed"] += 1

        return rec

    def finish_run(self, run_id: str) -> Dict[str, Any]:
        run = self._active_runs.get(run_id)
        if not run:
            return {"error": "Run not found"}

        run["end_time"] = time.time()
        run["duration_seconds"] = round(run["end_time"] - run["start_time"], 2)
        run["success_rate"] = round(run["probes_passed"] / run["probes_executed"], 4) if run["probes_executed"] > 0 else 0.0
        return run
