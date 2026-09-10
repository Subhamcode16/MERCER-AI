"""
Phase 23 Credential Domain Scope Enforcer.
"""
import logging
from typing import Dict, Set
from src.secret_operations.secret_models import CredentialDomain
from src.secret_operations.exceptions import UnauthorizedScopeError

logger = logging.getLogger(__name__)

# Allowed domains for specific service callers
SERVICE_ALLOWED_DOMAINS: Dict[str, Set[CredentialDomain]] = {
    "llm_gateway": {CredentialDomain.LLM},
    "vision_gateway": {CredentialDomain.VISION},
    "mcp_gateway": {CredentialDomain.MCP},
    "persistence_engine": {CredentialDomain.DATABASE, CredentialDomain.STORAGE},
    "observability_service": {CredentialDomain.OBSERVABILITY},
    "deployment_controller": {CredentialDomain.DEPLOYMENT}
}

class CredentialScopeValidator:
    """Enforces least-privilege domain scoping on credential requests."""

    @staticmethod
    def validate_access(service_name: str, domain: CredentialDomain) -> bool:
        allowed = SERVICE_ALLOWED_DOMAINS.get(service_name, set())
        if domain not in allowed:
            logger.error(f"Unauthorized credential access attempt: Service '{service_name}' requested domain '{domain.value}'")
            raise UnauthorizedScopeError(f"Service '{service_name}' is not authorized to access domain '{domain.value}'")
        return True
