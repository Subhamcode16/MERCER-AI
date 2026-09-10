"""
Phase 23 Immutable Version Registry.
"""
import logging
from typing import Dict, List, Optional
from src.deployment.deployment_models import ArtifactManifest

logger = logging.getLogger(__name__)

class VersionRegistry:
    """Immutable catalog of validated release versions."""

    def __init__(self):
        self._versions: Dict[str, ArtifactManifest] = {}

    def register_version(self, manifest: ArtifactManifest) -> None:
        manifest.manifest_hash = manifest.compute_hash()
        self._versions[manifest.version_id] = manifest
        logger.info(f"Registered immutable release version: {manifest.version_id} (Hash: {manifest.manifest_hash[:12]}...)")

    def get_version(self, version_id: str) -> Optional[ArtifactManifest]:
        return self._versions.get(version_id)

    def list_versions(self) -> List[ArtifactManifest]:
        return list(self._versions.values())
