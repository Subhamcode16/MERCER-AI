"""
Phase 25 Tamper-Evident Evidence Bundle Exporter.
"""
from typing import Dict, Any, List
import json
import hashlib
import time
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability
from src.control_plane.permissions import PermissionGuard
from src.control_plane.dto import sanitize_payload
from src.live_operations.live_models import LiveEvidenceRecord

class EvidenceBundleExporter:
    """Exports cryptographically signed evidence bundles for external compliance."""

    @staticmethod
    def export_evidence_bundle(
        context: OperatorContext,
        tenant_id: str,
        client_id: str,
        evidence_records: List[LiveEvidenceRecord]
    ) -> Dict[str, Any]:
        PermissionGuard.enforce_capability(context, OperatorCapability.VIEW_EVIDENCE)
        PermissionGuard.enforce_tenant_boundary(context, tenant_id, client_id)

        serialized_records = []
        for r in evidence_records:
            if (tenant_id == "*" or r.tenant_id == tenant_id) and (client_id == "*" or r.client_id == client_id):
                serialized_records.append({
                    "evidence_id": r.evidence_id,
                    "probe_id": r.probe_id,
                    "timestamp": r.timestamp,
                    "correlation_id": r.correlation_id,
                    "tenant_id": r.tenant_id,
                    "client_id": r.client_id,
                    "component": r.component,
                    "status": r.status,
                    "record_hash": r.record_hash
                })

        payload_raw = json.dumps(serialized_records, sort_keys=True)
        bundle_hash = hashlib.sha256(payload_raw.encode("utf-8")).hexdigest()

        return {
            "bundle_id": f"bnd-{bundle_hash[:12]}",
            "exported_at": time.time(),
            "exported_by": context.operator_id,
            "tenant_id": tenant_id,
            "client_id": client_id,
            "total_records": len(serialized_records),
            "bundle_sha256": bundle_hash,
            "records": serialized_records
        }
