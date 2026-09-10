"""
Phase 22 Runtime Control: Environment Guard
-------------------------------------------
Enforces strict environment boundary separation. Prevents sandbox/test data,
unauthorized live mutations, or unverified secrets from cross-contaminating production.
"""

from typing import Dict, Any, List
from src.runtime_control.runtime_config import EnvironmentType, RuntimeConfig, RuntimeConfigError

class EnvironmentGuardError(Exception):
    """Raised when an environment isolation or permission invariant is violated."""
    pass

class EnvironmentGuard:
    """Enforces execution boundaries according to active runtime environment."""

    def __init__(self, config: RuntimeConfig):
        self.config = config

    def validate_action_environment(self, requested_action: str, target_env: EnvironmentType) -> bool:
        """Ensures that actions targeting an environment match active runtime bounds."""
        if self.config.environment != target_env:
            raise EnvironmentGuardError(
                f"Cross-environment operation rejected: Runtime is in {self.config.environment.value}, "
                f"cannot execute action '{requested_action}' targeting {target_env.value}."
            )
        return True

    def sanitize_environment_variables(self, raw_env: Dict[str, str]) -> Dict[str, str]:
        """Redacts sensitive credentials and ensures non-leaking env maps."""
        sanitized = {}
        sensitive_keywords = ["KEY", "SECRET", "TOKEN", "AUTH", "PASSWORD", "CREDENTIAL"]
        for k, v in raw_env.items():
            if any(kw in k.upper() for kw in sensitive_keywords):
                sanitized[k] = "[REDACTED]"
            else:
                sanitized[k] = v
        return sanitized
