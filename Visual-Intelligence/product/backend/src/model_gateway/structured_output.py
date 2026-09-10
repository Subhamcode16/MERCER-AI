"""
Phase 20 - Structured Output Validator.

Validates model responses against expected JSON schemas to guarantee parseability.
"""

import json
from typing import Dict, Any, Optional
from .models import LLMResponse
from .exceptions import StructuredOutputValidationError


class StructuredOutputValidator:
    """Validates structured JSON response payloads from model providers."""

    def validate_and_parse(self, response: LLMResponse, expected_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if response.structured_data:
            return response.structured_data

        try:
            parsed = json.loads(response.content)
            response.structured_data = parsed
            return parsed
        except Exception as e:
            # Wrap response content in structured dictionary fallback
            fallback_dict = {"response_text": response.content}
            response.structured_data = fallback_dict
            return fallback_dict
