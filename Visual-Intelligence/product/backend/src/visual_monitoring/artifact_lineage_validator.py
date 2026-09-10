"""
Phase 24 Artifact Lineage and Cryptographic Commitment Validator.
"""
import hashlib
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ArtifactLineageValidator:
    """Validates SHA-256 commitment hashes and parent lineage DAGs for live visual deliverables."""

    @staticmethod
    def compute_commitment_hash(artifact_id: str, parent_id: Optional[str], client_id: str, payload: Dict[str, Any]) -> str:
        raw = f"{artifact_id}:{parent_id}:{client_id}:{json.dumps(payload, sort_keys=True)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def validate_lineage(artifact_dict: Dict[str, Any]) -> bool:
        art_id = artifact_dict.get("artifact_id")
        parent_id = artifact_dict.get("parent_artifact_id")
        client_id = artifact_dict.get("client_id")
        payload = artifact_dict.get("payload", {})
        expected_hash = artifact_dict.get("commitment_hash")

        if not expected_hash:
            return False

        computed = ArtifactLineageValidator.compute_commitment_hash(art_id, parent_id, client_id, payload)
        return computed == expected_hash
