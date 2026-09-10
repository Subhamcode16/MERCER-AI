"""
Multi-Tenant Boundaries & Cross-Client Isolation (Phase 30).
Enforces tenant partition isolation and scrubs private identifiers before cross-client synthesis.
"""
from typing import List, Dict, Optional, Any, Set
from pydantic import BaseModel, Field
import re
from ..types import ThreatID, GovernanceInvariantViolation


class MultiTenantIsolationBoundary:
    CLIENT_IDENTIFIER_PATTERNS = [
        r"\bclient_[a-zA-Z0-9_-]+\b",
        r"\btenant_[a-zA-Z0-9_-]+\b",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        r"\b(secret|api_key|token)_[a-zA-Z0-9]+\b"
    ]

    @classmethod
    def validate_tenant_access(cls, requesting_tenant: str, target_tenant: str):
        # T30-017: Cross-tenant contamination prevention
        if requesting_tenant != target_tenant:
            raise GovernanceInvariantViolation(
                ThreatID.T30_017,
                f"Cross-tenant access violation: Tenant '{requesting_tenant}' attempted to access '{target_tenant}' data.",
                {"requesting_tenant": requesting_tenant, "target_tenant": target_tenant}
            )
        return True

    @classmethod
    def scrub_and_abstract_for_institutional(cls, raw_insight: str, source_tenant: str) -> str:
        # T30-018: Semantic leakage detection and scrubbing
        scrubbed = raw_insight
        for pattern in cls.CLIENT_IDENTIFIER_PATTERNS:
            scrubbed = re.sub(pattern, "[ANONYMIZED]", scrubbed, flags=re.IGNORECASE)
        
        # Verify no direct tenant name remains
        if source_tenant in scrubbed:
            scrubbed = scrubbed.replace(source_tenant, "[ANONYMIZED_TENANT]")

        return f"[GOVERNED_ABSTRACTION] {scrubbed}"
