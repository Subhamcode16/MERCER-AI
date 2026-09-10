"""
Phase 23 High-Performance Secret Masker and Leakage Detector.
"""
import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

SECRET_PATTERNS = [
    re.compile(r"(api[-_]?key|secret|password|bearer|token|private[-_]?key)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{8,})['\"]?", re.IGNORECASE),
    re.compile(r"sk-[a-zA-Z0-9_\-]{15,}", re.IGNORECASE),
    re.compile(r"ghp_[a-zA-Z0-9]{20,}", re.IGNORECASE),
    re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]{15,}", re.IGNORECASE),
]

REPLACEMENT_MASK = "***REDACTED***"

class SecretRedactionEngine:
    """Masks secrets and sensitive values from telemetry, logs, and outputs."""

    @staticmethod
    def redact_text(text: str) -> str:
        if not text:
            return text

        masked = text
        for pattern in SECRET_PATTERNS:
            masked = pattern.sub(lambda m: f"{m.group(1)}={REPLACEMENT_MASK}" if len(m.groups()) >= 2 else REPLACEMENT_MASK, masked)
        return masked

    @staticmethod
    def redact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively redacts dictionary values."""
        clean = {}
        for k, v in data.items():
            if any(s in k.lower() for s in ["key", "secret", "password", "token", "auth", "credential"]):
                clean[k] = REPLACEMENT_MASK
            elif isinstance(v, dict):
                clean[k] = SecretRedactionEngine.redact_dict(v)
            elif isinstance(v, list):
                clean[k] = [
                    SecretRedactionEngine.redact_dict(i) if isinstance(i, dict) else (
                        SecretRedactionEngine.redact_text(str(i)) if isinstance(i, str) else i
                    ) for i in v
                ]
            elif isinstance(v, str):
                clean[k] = SecretRedactionEngine.redact_text(v)
            else:
                clean[k] = v
        return clean
