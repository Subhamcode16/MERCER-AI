"""
Phase 24 Standardized Evidence Collector and Receipt Generator.
"""
import uuid
import time
import logging
from typing import Dict, Any, List, Optional
from src.live_operations.live_models import LiveEvidenceRecord, ProbeResult, LiveValidationMode

logger = logging.getLogger(__name__)

class LiveEvidenceCollector:
    """Collects, standardizes, and hashes live validation evidence."""

    def __init__(self):
        self._records: List[LiveEvidenceRecord] = []

    def create_evidence_record(
        self,
        probe_result: ProbeResult,
        correlation_id: str,
        tenant_id: str,
        client_id: str,
        provider: str = "",
        model_or_version: str = "",
        operation: str = "",
        input_hash: str = "",
        output_hash: str = "",
        cost_usd: float = 0.0,
        authorization_token_id: Optional[str] = None,
        environment: LiveValidationMode = LiveValidationMode.SANDBOX,
        artifact_hash: Optional[str] = None,
        lineage_hash: Optional[str] = None
    ) -> LiveEvidenceRecord:
        """Creates and cryptographically hashes an evidence record."""
        rec = LiveEvidenceRecord(
            evidence_id=f"evi-{uuid.uuid4().hex[:10]}",
            probe_id=probe_result.probe_id,
            environment=environment,
            timestamp=time.time(),
            correlation_id=correlation_id,
            tenant_id=tenant_id,
            client_id=client_id,
            component=probe_result.target_component,
            provider=provider,
            model_or_version=model_or_version,
            operation=operation,
            input_hash=input_hash,
            output_hash=output_hash,
            status=probe_result.status,
            failure_class=probe_result.message if probe_result.status != "PASS" else None,
            latency_ms=probe_result.latency_ms,
            cost_usd=cost_usd,
            authorization_token_id=authorization_token_id,
            policy_decision="PERMITTED" if probe_result.status != "DENIED" else "DENIED",
            artifact_hash=artifact_hash,
            lineage_hash=lineage_hash
        )
        rec.record_hash = rec.compute_hash()
        self._records.append(rec)
        logger.info(f"Recorded live evidence {rec.evidence_id} for probe {rec.probe_id} [{rec.status.value}]")
        return rec

    def list_records(self) -> List[LiveEvidenceRecord]:
        return list(self._records)
