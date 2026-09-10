# Phase 13 — External Tool & Platform Integration Architecture

## Executive Architectural Summary

Phase 13 introduces a **Controlled External Tool & Platform Integration Boundary** (`src/integration_boundary/`) above the Phase 1–12 baseline (`src/security_substrate/`, `src/agentic_work/`, `src/execution_control/`, `src/mission_control/`, `src/coordination/`).

Phase 13 establishes a machine-enforced transport boundary between AI reasoning, multi-mission coordination, human authorization, and external provider execution. It allows already-authorized capabilities to interact safely with real external tool interfaces without manufacturing authority or leaking credentials.

---

## Governing Architectural Invariants

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$
$$\mathbf{Coordination \neq Authorization}$$
$$\mathbf{Learning \neq Security\ Policy\ Mutation}$$
$$\mathbf{External\ Tool\ Access \neq Blanket\ Provider\ Access}$$

1. **`INV-13-001` — Authorization Origin:** Only `HumanAuthorizationBoundary` originates authorization. Integration boundary code CANNOT create or modify authorization records.
2. **`INV-13-002` — Capability Exactness:** Every external operation maps 1-to-1 to an explicit Phase 10 capability (`CREATE_DRAFT`, `PUBLISH_CONTENT`, `SCHEDULE_CONTENT`, etc.). Generic or wildcard permissions (`admin`, `*`) are prohibited and fail closed.
3. **`INV-13-003` & `INV-13-004` — Credential Non-Authority & Isolation:** Possession of credentials does NOT grant authorization. Credentials are managed as opaque handles (`CredentialReference`) in `CredentialGateway`; raw secrets NEVER enter AI context, memory, prompts, logs, or exceptions.
4. **`INV-13-005` — Sandbox / Live Separation:** `EnvironmentGuard` strictly rejects test credentials on `LIVE` operations and blocks `LIVE` calls without explicit environment flags and Phase 10 approval.
5. **`INV-13-006` — Scope Propagation:** Mission ID, Authorization ID, Capability, Resource Scope, Action Hash, Expiration, and Nonce remain cryptographically bound.
6. **`INV-13-007` — No Credential Escalation:** Provider adapters cannot request broader scopes or exchange credentials for elevated privileges.
7. **`INV-13-008` — Idempotent External Effects:** Idempotency barrier deduplicates external mutations via SHA-256 operation keys across threads.
8. **`INV-13-009` — Provider Failure Containment:** Circuit breaker trips after 3 consecutive failures, setting status to `OPEN` and blocking execution without altering security policy.
9. **`INV-13-010` to `INV-13-012` — Audit & Isolation:** Phase 9 learning signals and Phase 4 FROST research artifacts cannot mutate security policies or act as production evidence. Every invocation produces a secret-free, append-only integration ledger event.

---

## Integration Pipeline Control Flow

```
External User Intent
        |
        v
Phase 8 Agentic Work
        |
        v
Phase 9 Learning / Knowledge
        |
        v
Phase 11 Mission Control
        |
        v
Phase 12 Multi-Mission Coordination
        |
        v
Phase 10 Human Authorization
        |
        v
Phase 13 Integration Controller (10-Step Pipeline)
        |
        +---> 1. Provider Registration Check
        +---> 2. 1-to-1 Capability Mapping (CapabilityMappingRegistry)
        +---> 3. Authorization Bridge Validation (AuthorizationBridge)
        +---> 4. Sandbox/Live Boundary Validation (EnvironmentGuard)
        +---> 5. Rate Limit & Burst Check (ProviderRateLimiter)
        +---> 6. Circuit Breaker Check (IntegrationCircuitBreaker)
        +---> 7. Idempotency Key Reservation (ExternalIdempotencyBarrier)
        +---> 8. Opaque Credential Retrieval (CredentialGateway)
        +---> 9. Adapter Invocation (BaseProviderAdapter)
        +---> 10. Outcome Reconciliation (ReconciliationEngine)
        |
        v
Phase 13 Integration Audit Ledger (IntegrationLedger)
```

---

## Component Architecture Overview

1. **`CapabilityMappingRegistry` (`src/integration_boundary/capability_mapping.py`):** Enforces 1-to-1 mapping between provider operations and Phase 10 capabilities. Rejects wildcard (`*`) and `admin` operation names.
2. **`CredentialGateway` (`src/integration_boundary/credential_gateway.py`):** Manages opaque credential reference handles. Rejects credential access requests unless `authorization_verified` is explicitly `True`.
3. **`EnvironmentGuard` (`src/integration_boundary/environment_guard.py`):** Verifies environment boundary matching across `TEST`, `SANDBOX`, `DRY_RUN`, and `LIVE`.
4. **`AuthorizationBridge` (`src/integration_boundary/authorization_bridge.py`):** Consumes Phase 10 `AuthorizationRecord` tokens, checking expiration, mission binding, scope matching, and nonces.
5. **`ExternalIdempotencyBarrier` (`src/integration_boundary/idempotency.py`):** Atomic SHA-256 key deduplication barrier preventing duplicate external mutations.
6. **`ProviderRateLimiter` (`src/integration_boundary/rate_limiter.py`):** Sliding window token bucket limiter enforcing requests-per-minute and burst caps.
7. **`IntegrationCircuitBreaker` (`src/integration_boundary/circuit_breaker.py`):** Tracks provider failure thresholds and isolates faulty providers in `OPEN` state.
8. **`BaseProviderAdapter` & `MockSocialProvider` (`src/integration_boundary/provider.py`, `mock_social_provider.py`):** Abstract provider contract and deterministic sandbox mock adapter.
9. **`ReconciliationEngine` (`src/integration_boundary/reconciliation.py`):** Reconciles requested vs authorized vs returned provider execution results.
10. **`IntegrationLedger` (`src/integration_boundary/integration_ledger.py`):** Append-only SHA-256 hash-linked audit log stored in `data/phase13_ledger/`.
11. **`IntegrationController` (`src/integration_boundary/integration_controller.py`):** Orchestrates the full 10-step integration execution pipeline.
