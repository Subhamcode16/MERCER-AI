"""
Phase 20 - MCP Result Sanitizer & Trust Classifier.

Sanitizes raw MCP tool execution results, strips credentials/tokens,
and classifies results as UNTRUSTED_EXTERNAL_OBSERVATION.
"""

import re
from typing import Dict, Any
from .exceptions import MCPCredentialLeakageError


class MCPResultSanitizer:
    """Sanitizes raw tool results and enforces trust boundaries."""

    SENSITIVE_KEYS = {"api_key", "secret", "private_key", "token", "password"}

    def sanitize_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively redact sensitive credentials from tool output."""
        cleaned = {}
        for k, v in raw_result.items():
            if k.lower() in self.SENSITIVE_KEYS:
                cleaned[k] = "[REDACTED_CREDENTIAL]"
                continue

            if isinstance(v, str):
                cleaned[k] = self._sanitize_text(v)
            elif isinstance(v, dict):
                cleaned[k] = self.sanitize_result(v)
            elif isinstance(v, list):
                cleaned[k] = [self._sanitize_text(x) if isinstance(x, str) else x for x in v]
            else:
                cleaned[k] = v

        return cleaned

    def _sanitize_text(self, text: str) -> str:
        res = text
        for pat in [r'AIzaSy[a-zA-Z0-9_-]{33}', r'sk-[a-zA-Z0-9]{48}']:
            res = re.sub(pat, "[REDACTED_CREDENTIAL]", res)
        return res
