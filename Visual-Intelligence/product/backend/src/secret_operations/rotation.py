"""
Phase 23 Non-Disruptive In-Flight Credential Rotation.
"""
import time
import hashlib
import logging
from typing import Dict, Any, Optional
from src.secret_operations.secret_models import SecretMetadata, CredentialDomain
from src.secret_operations.exceptions import SecretRotationError

logger = logging.getLogger(__name__)

class SecretRotationEngine:
    """Handles in-flight credential rotation without requiring server restarts."""

    def __init__(self):
        self._secrets: Dict[str, Dict[str, Any]] = {}
        self._metadata: Dict[str, SecretMetadata] = {}

    def set_secret(self, secret_name: str, domain: CredentialDomain, secret_value: str) -> SecretMetadata:
        now = time.time()
        fp = hashlib.sha256(secret_value.encode("utf-8")).hexdigest()[:16]
        meta = SecretMetadata(
            secret_name=secret_name,
            domain=domain,
            version=1,
            created_at=now,
            last_rotated_at=now,
            fingerprint=fp,
            is_active=True
        )
        self._secrets[secret_name] = {"value": secret_value, "version": 1}
        self._metadata[secret_name] = meta
        return meta

    def rotate_secret(self, secret_name: str, new_secret_value: str) -> SecretMetadata:
        if secret_name not in self._secrets:
            raise SecretRotationError(f"Cannot rotate non-existent secret: {secret_name}")

        now = time.time()
        curr_ver = self._secrets[secret_name]["version"]
        new_ver = curr_ver + 1
        fp = hashlib.sha256(new_secret_value.encode("utf-8")).hexdigest()[:16]

        self._secrets[secret_name] = {"value": new_secret_value, "version": new_ver}
        meta = self._metadata[secret_name]
        meta.version = new_ver
        meta.last_rotated_at = now
        meta.fingerprint = fp

        logger.info(f"Secret {secret_name} rotated to version {new_ver} (Fingerprint: {fp})")
        return meta

    def get_secret_value(self, secret_name: str) -> Optional[str]:
        sec = self._secrets.get(secret_name)
        return sec["value"] if sec else None

    def get_metadata(self, secret_name: str) -> Optional[SecretMetadata]:
        return self._metadata.get(secret_name)
