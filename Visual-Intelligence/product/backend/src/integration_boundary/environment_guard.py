"""
Phase 13 Environment Guard.

Enforces INV-13-005: Strict Sandbox / Live Separation.
Prevents cross-environment credential usage and blocks unauthorized LIVE operations.
"""

from src.integration_boundary.models import ProviderEnvironment, CredentialReference
from src.integration_boundary.exceptions import EnvironmentMismatchError


class EnvironmentGuard:
    """Enforces strict sandbox and live environment separation."""

    @staticmethod
    def validate_environment_boundary(
        target_environment: ProviderEnvironment,
        credential_reference: CredentialReference,
        explicit_live_allowed: bool = False
    ) -> None:
        """
        Validates that credential environment matches operation target environment.
        Fails closed on any mismatch or unauthorized LIVE execution.
        """
        cred_env = credential_reference.environment

        # 1. Credential vs Operation environment match check
        if cred_env != target_environment:
            raise EnvironmentMismatchError(
                f"Sandbox/Live Environment Boundary Violation (INV-13-005): "
                f"Credential environment '{cred_env.value}' cannot be used for target environment '{target_environment.value}'."
            )

        # 2. LIVE environment restriction check
        if target_environment == ProviderEnvironment.LIVE:
            if not explicit_live_allowed:
                raise EnvironmentMismatchError(
                    "Environment Separation Violation (INV-13-005): Execution in LIVE environment is forbidden without explicit live context enablement."
                )

        # 3. Test credential prohibition on LIVE operations
        if cred_env in (ProviderEnvironment.TEST, ProviderEnvironment.SANDBOX) and target_environment == ProviderEnvironment.LIVE:
            raise EnvironmentMismatchError(
                f"Environment Separation Violation (INV-13-005): {cred_env.value} credential cannot execute in LIVE environment."
            )
