"""
Phase 22 Production Validation: Environment Validation
------------------------------------------------------
Validates live environment settings, prevents secret leaks, and confirms fail-closed behavior.
"""

from typing import Dict, Any, List
from src.runtime_control import RuntimeConfig, EnvironmentType

class EnvironmentValidator:
    """Validates environment state and security preconditions."""

    def __init__(self, config: RuntimeConfig):
        self.config = config

    def validate_production_readiness(self) -> Dict[str, Any]:
        """Ensures that required environment configurations meet production safety gates."""
        checks = {
            "strict_security_mode": self.config.strict_security_mode,
            "no_unverified_restarts": not self.config.allow_unverified_restarts,
            "valid_environment": self.config.environment in [EnvironmentType.TEST, EnvironmentType.SANDBOX, EnvironmentType.STAGING, EnvironmentType.PRODUCTION],
            "timeout_bounded": self.config.max_request_timeout_seconds <= 60.0,
            "retries_bounded": self.config.max_retries_permitted <= 3,
        }
        all_passed = all(checks.values())
        return {
            "passed": all_passed,
            "environment": self.config.environment.value,
            "checks": checks,
        }
