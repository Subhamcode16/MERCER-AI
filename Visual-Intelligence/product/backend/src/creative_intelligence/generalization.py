"""
Phase 19 - De-identification & Confidentiality Filter Pipeline.

Enforces CrossClientPattern != CrossClientData.
Scubs and anonymizes client metadata, PII, asset paths, and proprietary terms
before promoting patterns to the studio-global namespace.
"""

import re
from typing import Dict, Any, List, Tuple
from .exceptions import ClientDataLeakageError, UnsafeGeneralizationError


class ConfidentialityFilter:
    """Rigorous de-identification engine for cross-client pattern generalization."""

    # Prohibited client patterns & key names
    PROHIBITION_KEYS = {
        "client_id", "client_name", "brand_name", "user_id", "email",
        "contact_email", "api_key", "secret", "private_key", "ip_address", "phone", "raw_client_data"
    }

    # Regex patterns for scrubbing sensitive data
    SENSITIVE_REGEXES = [
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # Email
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',                    # Phone
        r'\b(?:nocap|beta_tech|zenith|apex_luxury|client_[a-zA-Z0-9]+)\b', # Client brand names
    ]

    def filter_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Scrub dictionary of attributes, stripping prohibited keys and scrubbing sensitive strings."""
        cleaned = {}
        for key, val in attributes.items():
            key_lower = key.lower()
            if key_lower in self.PROHIBITION_KEYS or any(k in key_lower for k in ["email", "client_id", "raw_client"]):
                continue  # Strip prohibited key

            if isinstance(val, str):
                cleaned_val = self.scrub_string(val)
                cleaned[key] = cleaned_val
            elif isinstance(val, dict):
                cleaned[key] = self.filter_attributes(val)
            elif isinstance(val, list):
                cleaned_list = []
                for item in val:
                    if isinstance(item, str):
                        cleaned_list.append(self.scrub_string(item))
                    elif isinstance(item, dict):
                        cleaned_list.append(self.filter_attributes(item))
                    else:
                        cleaned_list.append(item)
                cleaned[key] = cleaned_list
            else:
                cleaned[key] = val

        return cleaned

    def scrub_string(self, text: str) -> str:
        """Replace sensitive patterns in strings with anonymized placeholders."""
        res = text
        for pattern in self.SENSITIVE_REGEXES:
            res = re.sub(pattern, "[ANONYMIZED_IDENTIFIER]", res, flags=re.IGNORECASE)
        return res

    def validate_anonymization(self, cleaned_data: Dict[str, Any]) -> bool:
        """Verify that zero client-specific raw data or keys remain in the object."""
        def check_node(val: Any) -> None:
            if isinstance(val, str):
                for pattern in self.SENSITIVE_REGEXES:
                    if re.search(pattern, val, flags=re.IGNORECASE):
                        raise ClientDataLeakageError(f"Un-scrubbed sensitive string detected: {val}")
            elif isinstance(val, dict):
                for k, v in val.items():
                    k_lower = k.lower()
                    if k_lower in self.PROHIBITION_KEYS or any(p in k_lower for p in ["email", "client_id", "raw_client"]):
                        raise ClientDataLeakageError(f"Confidential key detected in global pattern: {k}")
                    check_node(v)
            elif isinstance(val, list):
                for item in val:
                    check_node(item)

        check_node(cleaned_data)
        return True
