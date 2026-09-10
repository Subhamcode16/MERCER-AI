"""
Phase 25 Human Review Evidence Packager.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List
import hashlib
import time

@dataclass
class ApprovalEvidencePackage:
    evidence_bundle_id: str
    campaign_id: str
    tenant_id: str
    client_id: str
    artifact_ids: List[str]
    artifact_hashes: List[str]
    total_cost_usd: float
    critique_summary: Dict[str, Any]
    bundle_hash: str
    timestamp: float = field(default_factory=time.time)

class ApprovalEvidencePackager:
    @staticmethod
    def package_evidence(
        bundle_id: str,
        campaign_id: str,
        tenant_id: str,
        client_id: str,
        artifacts: List[Dict[str, Any]],
        critique: Dict[str, Any],
        cost_usd: float
    ) -> ApprovalEvidencePackage:
        art_ids = [a.get("artifact_id", "") for a in artifacts]
        art_hashes = [a.get("artifact_hash", "") for a in artifacts]
        raw = f"{bundle_id}:{campaign_id}:{tenant_id}:{client_id}:{art_hashes}:{critique}:{cost_usd}"
        bundle_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return ApprovalEvidencePackage(
            evidence_bundle_id=bundle_id,
            campaign_id=campaign_id,
            tenant_id=tenant_id,
            client_id=client_id,
            artifact_ids=art_ids,
            artifact_hashes=art_hashes,
            total_cost_usd=cost_usd,
            critique_summary=critique,
            bundle_hash=bundle_hash
        )
