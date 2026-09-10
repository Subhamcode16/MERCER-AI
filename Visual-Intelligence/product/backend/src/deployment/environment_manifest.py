"""
Phase 23 Environment Manifest and Fingerprinting.
"""
import hashlib
import json
from typing import Dict, Any
from src.deployment.deployment_models import TargetEnvironment

class EnvironmentManifest:
    """Fingerprints environment runtime configurations and verifies strict boundaries."""

    @staticmethod
    def generate_fingerprint(env: TargetEnvironment, settings: Dict[str, Any]) -> str:
        payload = json.dumps({
            "environment": env.value,
            "settings": settings
        }, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def validate_production_boundaries(env: TargetEnvironment, settings: Dict[str, Any]) -> bool:
        """Ensures TEST / SANDBOX do not contain production endpoints or credentials."""
        if env in (TargetEnvironment.TEST, TargetEnvironment.SANDBOX):
            serialized = json.dumps(settings).lower()
            if "prod" in serialized or "live" in serialized or "production" in serialized:
                return False
        return True
