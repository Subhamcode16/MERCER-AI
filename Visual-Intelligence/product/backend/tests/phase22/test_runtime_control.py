"""
Phase 22 Tests: Runtime Control
--------------------------------
"""

import pytest
from src.runtime_control import (
    RuntimeConfig,
    EnvironmentType,
    RuntimeConfigError,
    EnvironmentGuard,
    EnvironmentGuardError,
    CorrelationContext,
    HealthChecker,
    ReadinessChecker,
    DependencyHealthChecker,
    HealthStatus,
    ShutdownCoordinator,
)

def test_runtime_config_environments():
    cfg_test = RuntimeConfig.from_env("TEST")
    assert cfg_test.environment == EnvironmentType.TEST
    assert cfg_test.is_test_or_sandbox()

    cfg_prod = RuntimeConfig.from_env("PRODUCTION")
    assert cfg_prod.environment == EnvironmentType.PRODUCTION
    assert cfg_prod.is_production()

def test_unknown_environment_fails_closed():
    with pytest.raises(RuntimeConfigError):
        RuntimeConfig.from_env("UNKNOWN_ROGUE_ENV")

def test_environment_guard_isolation():
    cfg = RuntimeConfig.from_env("TEST")
    guard = EnvironmentGuard(cfg)
    assert guard.validate_action_environment("run_local_test", EnvironmentType.TEST)

    with pytest.raises(EnvironmentGuardError):
        guard.validate_action_environment("mutate_prod_database", EnvironmentType.PRODUCTION)

def test_secret_redaction():
    guard = EnvironmentGuard(RuntimeConfig.from_env("TEST"))
    raw = {"API_KEY": "secret123", "AUTH_TOKEN": "token456", "APP_NAME": "ILYREN"}
    sanitized = guard.sanitize_environment_variables(raw)
    assert sanitized["API_KEY"] == "[REDACTED]"
    assert sanitized["AUTH_TOKEN"] == "[REDACTED]"
    assert sanitized["APP_NAME"] == "ILYREN"

def test_correlation_context_propagation():
    ctx = CorrelationContext.create(client_id="client_01", campaign_id="camp_01")
    assert ctx.correlation_id.startswith("corr_")
    assert ctx.client_id == "client_01"

    child = ctx.spawn_child("model_call")
    assert child.parent_correlation_id == ctx.correlation_id
    assert child.tags.get("sub_stage") == "model_call"

    headers = ctx.to_header_dict()
    assert headers["X-Correlation-ID"] == ctx.correlation_id
    assert headers["X-Client-ID"] == "client_01"

def test_health_and_readiness_probes():
    health = HealthChecker().check_liveness()
    assert health["status"] == "HEALTHY"

    readiness = ReadinessChecker().check_readiness()
    assert readiness["ready"] is True

    dep_checker = DependencyHealthChecker()
    dep_checker.record_dependency("gemini_api", HealthStatus.HEALTHY, 120.5)
    dep_report = dep_checker.check_dependencies()
    assert dep_report["status"] == "HEALTHY"
    assert "gemini_api" in dep_report["dependencies"]

def test_graceful_shutdown():
    coordinator = ShutdownCoordinator()
    cleaned = []
    coordinator.register_hook(lambda: cleaned.append("hook1"))
    coordinator.record_checkpoint("cp_1", {"state": "saved"})

    result = coordinator.execute_shutdown()
    assert result["status"] == "COMPLETED"
    assert result["executed_hooks"] == 1
    assert result["audit_flushed"] is True
    assert "hook1" in cleaned
