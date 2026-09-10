"""
Phase 26 Capability Binding & Manifest Resolution.
"""
from dataclasses import dataclass, field
from typing import Set, Dict, Optional


class CapabilityError(Exception):
    pass


@dataclass
class CapabilityManifest:
    worker_id: str
    allowed_capabilities: Set[str] = field(default_factory=set)
    forbidden_capabilities: Set[str] = field(default_factory=set)


class CapabilityResolver:
    """Evaluates and enforces worker capability manifests."""

    def __init__(self):
        self._manifests: Dict[str, CapabilityManifest] = {}

    def register_manifest(self, manifest: CapabilityManifest) -> None:
        # Check for prohibited wildcard capabilities
        if "*" in manifest.allowed_capabilities or "all" in manifest.allowed_capabilities:
            raise CapabilityError(f"Wildcard capability grants are strictly forbidden for worker {manifest.worker_id}")
        self._manifests[manifest.worker_id] = manifest

    def get_manifest(self, worker_id: str) -> Optional[CapabilityManifest]:
        return self._manifests.get(worker_id)

    def has_capability(self, worker_id: str, capability: str) -> bool:
        manifest = self._manifests.get(worker_id)
        if not manifest:
            return False
        
        # Explicit forbidden overrides everything
        if capability in manifest.forbidden_capabilities:
            return False

        return capability in manifest.allowed_capabilities

    def assert_capability(self, worker_id: str, capability: str) -> None:
        if not self.has_capability(worker_id, capability):
            manifest = self._manifests.get(worker_id)
            forbidden_msg = " (Explicitly Forbidden)" if (manifest and capability in manifest.forbidden_capabilities) else ""
            raise CapabilityError(
                f"Worker '{worker_id}' lacks required capability '{capability}'{forbidden_msg}"
            )
