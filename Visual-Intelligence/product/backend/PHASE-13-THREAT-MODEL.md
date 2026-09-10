# Phase 13 — External Tool & Platform Integration Threat Model & Risk Matrix

## Overview & Scope

Phase 13 establishes a controlled external tool and platform integration boundary. This threat model details potential attack vectors, scope confusion attempts, credential leakage risks, replay mutations, environment mismatches, and provider failure amplifications, along with their enforced defensive controls.

---

## Threat Matrix

| Threat Vector ID | Threat Description | Attack Vector / Scenario | Architectural Defense | Mitigated Invariant | Risk Level |
|---|---|---|---|---|---|
| **TM-13-001** | **Unauthorized Provider Invocation** | Attacker attempts to call a provider adapter without a valid Phase 10 authorization record. | `AuthorizationBridge.validate_authorization_for_external_call()` rejects calls missing valid `AuthorizationRecord` tokens. | `INV-13-001` | **CRITICAL** |
| **TM-13-002** | **Authorization Forgery / Synthetic Token** | Attacker presents a synthesized or tampered authorization record. | `AuthorizationRecord.validate_active()` checks signature, nonces, and human operator identity. Non-human authorizers raise `SelfAuthorizationAttemptError`. | `INV-13-001` | **CRITICAL** |
| **TM-13-003** | **Scope Confusion / Capability Mismatch** | Valid authorization for `CREATE_DRAFT` is reused to attempt `PUBLISH_CONTENT`. | `CapabilityMappingRegistry` enforces 1-to-1 exactness. Mismatches raise `CapabilityMappingError` or `AuthorizationScopeMismatchError`. | `INV-13-002` | **HIGH** |
| **TM-13-004** | **Credential Leakage in Prompts/Logs** | Secret keys enter AI prompts, memory, logs, exception tracebacks, or generated artifacts. | `CredentialGateway` uses opaque handles (`CredentialReference`). Secrets are kept in isolated memory and never serialized or logged. | `INV-13-004` | **CRITICAL** |
| **TM-13-005** | **Sandbox-to-Live Environment Mismatch** | Test credentials or sandbox operations reach a live provider interface. | `EnvironmentGuard` validates matching environment tiers. Test credentials on `LIVE` raise `EnvironmentMismatchError`. | `INV-13-005` | **CRITICAL** |
| **TM-13-006** | **External Mutation Replay** | An attacker re-submits a previously executed external mutation payload. | `ExternalIdempotencyBarrier` tracks SHA-256 operation keys (`mission_id + auth_id + action_hash + user_key`). Duplicate calls raise `ExternalReplayError`. | `INV-13-008` | **HIGH** |
| **TM-13-007** | **Concurrent Replay Race** | Two threads attempt the exact same external mutation simultaneously. | Atomic `threading.Lock()` reservation in `ExternalIdempotencyBarrier`. Exactly one thread succeeds; the other raises `ExternalReplayError`. | `INV-13-008` | **HIGH** |
| **TM-13-008** | **Provider Failure Amplification** | Provider timeouts or API crashes trigger un-throttled retries, overwhelming downstream services. | `IntegrationCircuitBreaker` trips to `OPEN` after 3 consecutive failures, blocking calls with `IntegrationCircuitOpenError`. | `INV-13-009` | **HIGH** |
| **TM-13-009** | **Rate Limit Bypass / Token Flooding** | An agent attempts to bypass provider API rate limits to issue 500 requests/minute. | `ProviderRateLimiter` enforces sliding-window RPM and burst limits. Exceeding caps throws `ExternalRateLimitError`. | `INV-13-009` | **HIGH** |
| **TM-13-010** | **Provider Response Tampering** | Provider returns a malformed or mismatched transaction ID reported as success. | `ReconciliationEngine` validates request ID, transaction ID, and capability matching. Mismatches throw `ReconciliationTamperError`. | `INV-13-012` | **HIGH** |
| **TM-13-011** | **Learned Authorization Escalation** | Phase 9 learned strategy attempts to grant new external permissions or bypass authorization. | Phase 9 learning signals are strictly advisory and cannot mutate security policies, authorization rules, or provider mappings. | `INV-13-010` | **HIGH** |
| **TM-13-012** | **FROST Research Evidence Escalation** | Phase 4 FROST research artifacts presented as production execution evidence. | FROST research artifacts are flagged `TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION` and rejected by `AuthorizationBridge`. | `INV-13-011` | **CRITICAL** |
| **TM-13-013** | **AST / Runtime Gate Bypass** | Provider adapter attempts to bypass `ExecutionGate` or call `execute_action()` directly. | AST static analysis (`test_phase13_isolation.py`) asserts no `ExecutionGate` imports or direct security gate mutation exist in integration boundary code. | `INV-13-001` | **CRITICAL** |

---

## Security Invariant Mapping Summary

- `INV-13-001`: Verified by `test_phase13_security_boundary.py` (T13-1).
- `INV-13-002`: Verified by `test_capability_mapping.py` & `test_phase13_security_boundary.py` (T13-3).
- `INV-13-003` & `INV-13-004`: Verified by `test_credential_gateway.py` & `test_phase13_isolation.py`.
- `INV-13-005`: Verified by `test_environment_guard.py` & `test_phase13_security_boundary.py` (T13-5).
- `INV-13-006`: Verified by `test_authorization_bridge.py`.
- `INV-13-008`: Verified by `test_integration_idempotency.py` & `test_phase13_security_boundary.py` (T13-6).
- `INV-13-009`: Verified by `test_circuit_breaker.py` & `test_rate_limiter.py`.
- `INV-13-012`: Verified by `test_integration_controller.py` & `test_phase13_real_workflow.py`.
