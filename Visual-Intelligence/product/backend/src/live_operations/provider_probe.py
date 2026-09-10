"""
Phase 24 Base Provider Probe with Cryptographic Hashing and Telemetry Tracking.
"""
import abc
import time
import hashlib
import json
import logging
from typing import Dict, Any, Optional
from src.live_operations.live_models import ProbeResult, ProbeStatus, LiveValidationMode

logger = logging.getLogger(__name__)

class BaseProviderProbe(abc.ABC):
    """Abstract base class for all live external and governed internal probes."""

    def __init__(self, probe_id: str, target_component: str, mode: LiveValidationMode = LiveValidationMode.SANDBOX):
        self.probe_id = probe_id
        self.target_component = target_component
        self.mode = mode

    @staticmethod
    def hash_payload(data: Any) -> str:
        """Computes SHA-256 hash of payload without exposing raw content or secrets."""
        if isinstance(data, (dict, list)):
            serialized = json.dumps(data, sort_keys=True)
        else:
            serialized = str(data)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @abc.abstractmethod
    async def execute_probe(self, context: Dict[str, Any]) -> ProbeResult:
        """Executes the probe against the target component."""
        pass
