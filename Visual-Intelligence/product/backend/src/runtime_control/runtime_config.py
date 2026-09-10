"""
Phase 22 Runtime Control: Runtime Configuration
------------------------------------------------
Typed configuration with strict environment classification and fail-closed security.
Supported environments: TEST, SANDBOX, STAGING, PRODUCTION.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import os

class EnvironmentType(str, Enum):
    TEST = "TEST"
    SANDBOX = "SANDBOX"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

class RuntimeConfigError(Exception):
    """Raised when runtime configuration is invalid or unknown environment is provided."""
    pass

@dataclass(frozen=True)
class RuntimeConfig:
    environment: EnvironmentType
    app_version: str = "22.0.0"
    enable_live_providers: bool = False
    enable_mcp_gateway: bool = True
    max_request_timeout_seconds: float = 30.0
    max_retries_permitted: int = 2
    log_level: str = "INFO"
    strict_security_mode: bool = True
    allow_unverified_restarts: bool = False

    @classmethod
    def from_env(cls, env_name: Optional[str] = None) -> "RuntimeConfig":
        raw_env = (env_name or os.getenv("ILYREN_ENV", "TEST")).upper().strip()
        try:
            env_type = EnvironmentType(raw_env)
        except ValueError:
            # Fail closed on any unknown environment
            raise RuntimeConfigError(f"Security Invariant Violation: Unknown environment '{raw_env}' must fail closed.")
        
        is_prod = env_type == EnvironmentType.PRODUCTION
        is_staging = env_type == EnvironmentType.STAGING
        
        return cls(
            environment=env_type,
            enable_live_providers=is_prod or is_staging or os.getenv("ENABLE_LIVE_PROVIDERS", "false").lower() == "true",
            enable_mcp_gateway=True,
            max_request_timeout_seconds=float(os.getenv("MAX_TIMEOUT_SECONDS", "30.0")),
            max_retries_permitted=int(os.getenv("MAX_RETRIES", "2")),
            log_level="WARN" if is_prod else "INFO",
            strict_security_mode=True,
            allow_unverified_restarts=False,
        )

    def is_production(self) -> bool:
        return self.environment == EnvironmentType.PRODUCTION

    def is_test_or_sandbox(self) -> bool:
        return self.environment in (EnvironmentType.TEST, EnvironmentType.SANDBOX)
