"""
Phase 20 - Credential Redaction & Security Isolator.

Ensures credentials, API keys, and sensitive tokens never enter model prompts,
model context, response payloads, or audit logs.
"""

import re
from typing import Dict, Any
from .exceptions import CredentialLeakageError


class CredentialRedactor:
    """Scubs sensitive credentials and tokens from strings and dictionaries."""

    PATTERNS = [
        r'AIzaSy[a-zA-Z0-9_-]{20,}',   # Google Gemini API key pattern
        r'sk-[a-zA-Z0-9_-]{20,}',       # OpenAI key pattern
        r'sk-ant-[a-zA-Z0-9_-]{20,}',   # Anthropic key pattern
        r'bearer\s+[a-zA-Z0-9._-]{20,}',# Bearer tokens
        r'(?i)(api_key|secret|private_key|token)\s*[:=]\s*["\']?[a-zA-Z0-9_-]{10,}["\']?' # Generic secrets
    ]

    def sanitize_text(self, text: str) -> str:
        """Replace detected credential patterns with anonymized placeholder."""
        result = text
        for pat in self.PATTERNS:
            result = re.sub(pat, "[REDACTED_CREDENTIAL]", result)
        return result

    def sanitize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively redact dictionary values and keys."""
        cleaned = {}
        for key, val in data.items():
            if key.lower() in ["api_key", "secret", "private_key", "token", "password"]:
                cleaned[key] = "[REDACTED_CREDENTIAL]"
                continue

            if isinstance(val, str):
                cleaned[key] = self.sanitize_text(val)
            elif isinstance(val, dict):
                cleaned[key] = self.sanitize_dict(val)
            elif isinstance(val, list):
                cleaned[key] = [self.sanitize_text(x) if isinstance(x, str) else x for x in val]
            else:
                cleaned[key] = val
        return cleaned

    def audit_for_leakage(self, text_or_dict: Any) -> None:
        """Raise CredentialLeakageError if un-redacted credential pattern is found."""
        target_str = str(text_or_dict)
        for pat in self.PATTERNS:
            if re.search(pat, target_str):
                raise CredentialLeakageError("Un-redacted API key or credential detected in payload!")
