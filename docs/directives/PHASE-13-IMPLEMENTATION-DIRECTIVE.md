# Phase 13 Implementation Directive — External Tool & Platform Integration Boundary

**Document Status:** PROPOSED / AWAITING USER APPROVAL  
**Phase:** 13 — External Tool & Platform Integration Boundary  
**Prerequisites:** Phases 1–12 COMPLETE & RATIFIED — 373+ tests established before Phase 12, with Phase 12 reporting 373/373 PASSED  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`

---

## 1. Objective

Phase 13 extends the system from bounded internal orchestration into a **controlled external-world integration boundary**.

The purpose is NOT to make the system independently powerful. The purpose is to make already-authorized capabilities safely usable against real external services while preserving the separation:

$$
\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}
$$

$$
\mathbf{Coordination \neq Authorization}
$$

$$
\mathbf{Learning \neq Security\ Policy\ Mutation}
$$

$$
\mathbf{External\ Tool\ Access \neq Blanket\ Provider\ Access}
$$

Phase 13 must establish a machine-enforced boundary between:

1. AI planning and reasoning,
2. mission coordination,
3. human authorization,
4. capability-scoped external tool invocation,
5. provider-side side effects,
6. audit and reconciliation.

The phase must allow real-world workflow testing without allowing the agentic layer to manufacture authority, acquire credentials, widen scopes, or bypass the existing execution-control system.

---

## 2. Architectural Position

The intended control flow is:

```text
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
Phase 13 External Integration Boundary
        |
        +--> Provider Adapter
        |       |
        |       +--> Capability Validation
        |       +--> Resource Scope Validation
        |       +--> Credential Isolation
        |       +--> Rate / Budget Enforcement
        |       +--> Idempotency
        |       +--> Provider Call
        |
        v
Phase 7/10/11/12 Audit + Reconciliation
```

### Critical rule

Phase 13 is a **transport/integration boundary**, not a new source of authority.

It may consume an already-valid `AuthorizationRecord` from Phase 10 and an already-approved execution action from the existing control plane.

It may NOT create, broaden, inherit, transfer, or reinterpret authorization.

---

# 3. Non-Negotiable Invariants

### `INV-13-001` — Authorization Origin

Only the existing `HumanAuthorizationBoundary` may originate execution authorization.

Provider adapters, external tools, AI staff, coordinators, learning engines, and integration code cannot issue authorization.

---

### `INV-13-002` — Capability Exactness

Every external operation must resolve to one explicit Phase 10 capability.

Examples:

- `CREATE_DRAFT`
- `EDIT_DRAFT`
- `GENERATE_ASSET`
- `READ_ANALYTICS`
- `SCHEDULE_CONTENT`
- `PUBLISH_CONTENT`
- `DELETE_CONTENT`
- `MODIFY_BRAND_ASSETS`

A provider adapter may expose multiple operations, but each operation must map to a single approved capability.

Generic permissions such as:

```text
admin
all
*
root
bypass
manage_everything
```

must be rejected.

---

### `INV-13-003` — Credential Non-Authority

Credentials are secrets, not authorization.

The integration layer must never interpret possession of a credential as permission to perform an operation.

Authorization must be independently validated before credential use.

---

### `INV-13-004` — Credential Isolation

Raw provider credentials must never enter:

- AI staff context,
- prompts,
- workflow memory,
- learning signals,
- trend knowledge,
- task results,
- audit records,
- exception messages,
- generated artifacts.

Credentials must be accessed through a narrow provider credential interface.

For this phase, production credential persistence and secret-management infrastructure remain out of scope unless explicitly authorized by a future governance directive.

---

### `INV-13-005` — Sandbox / Live Separation

Provider integrations must distinguish:

```text
SANDBOX
TEST
DRY_RUN
LIVE
```

No implicit promotion from sandbox/test to live is permitted.

A test credential must not be accepted by a live adapter.

A live operation must require an explicit live environment declaration plus valid Phase 10 authorization.

---

### `INV-13-006` — Authorization Scope Propagation

The exact:

- mission ID,
- authorization ID,
- capability,
- resource scope,
- action hash,
- expiration,
- authorization nonce

must remain bound throughout the external execution path.

Any mismatch causes fail-closed rejection.

---

### `INV-13-007` — No Credential Escalation

An adapter must never:

- request broader scopes,
- exchange a credential for elevated privileges,
- discover alternate credentials,
- call an administrative endpoint to obtain access,
- modify authorization records.

---

### `INV-13-008` — Idempotent External Effects

Every externally mutating operation must carry a deterministic idempotency key derived from the authorized action context.

Retries must not unintentionally duplicate provider-side effects.

If the provider does not support idempotency natively, the adapter must use a bounded local idempotency barrier and mark the limitation explicitly.

---

### `INV-13-009` — Provider Failure Containment

Provider failures must remain integration failures.

A timeout, malformed provider response, rate-limit error, authentication failure, network error, or provider-side rejection must NOT mutate security policy or silently alter authorization.

---

### `INV-13-010` — Learning Cannot Auto-Execute

Phase 9 learning and Phase 8 self-improvement may improve strategy and workflow behavior, but learned changes cannot automatically authorize a new external side effect.

---

### `INV-13-011` — Research Isolation

Phase 4 FROST research artifacts remain `TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION`.

They cannot be supplied to provider adapters as authorization evidence.

---

### `INV-13-012` — Audit Completeness

Every external invocation attempt must produce a secret-free integration event containing enough information to reconstruct:

- who/what requested the action,
- which mission initiated it,
- which capability was invoked,
- which provider/environment was targeted,
- authorization reference,
- action hash,
- idempotency key hash,
- start/end status,
- provider outcome class,
- failure class.

Never log raw credentials, access tokens, request bodies containing secrets, or private cryptographic material.

---

# 4. Proposed Package Structure

Create:

```text
Visual-Intelligence/product/backend/src/integration_boundary/
```

## Core modules

### `exceptions.py`

Define fail-closed integration exceptions:

- `IntegrationBoundaryError`
- `ProviderNotRegisteredError`
- `CapabilityMappingError`
- `AuthorizationScopeMismatchError`
- `CredentialAccessViolationError`
- `EnvironmentMismatchError`
- `ProviderResponseValidationError`
- `ExternalReplayError`
- `ExternalRateLimitError`
- `ExternalOperationRejectedError`
- `ExternalTimeoutError`
- `IntegrationCircuitOpenError`

---

### `models.py`

Immutable contracts:

- `ProviderId`
- `ProviderEnvironment`
- `ExternalOperation`
- `ProviderCapability`
- `CredentialReference`
- `ExternalRequest`
- `ExternalResponse`
- `ExternalExecutionContext`
- `IntegrationOutcome`

No raw secret field may exist in these models.

---

### `capability_mapping.py`

Maps provider-specific operations to existing Phase 10 capabilities.

Example:

```text
InstagramProvider.create_draft
        -> CREATE_DRAFT

InstagramProvider.publish
        -> PUBLISH_CONTENT

AnalyticsProvider.read_metrics
        -> READ_ANALYTICS
```

Unknown operations must fail closed.

---

### `credential_gateway.py`

Narrow interface for retrieving credentials.

Requirements:

- opaque credential references,
- no raw secret persistence in integration models,
- no secret serialization,
- no secret logging,
- no credential access before authorization validation,
- no credential discovery.

Use an in-memory test credential provider for Phase 13.

Do not introduce production vault/KMS/secret-manager integration.

---

### `environment_guard.py`

Enforce sandbox/live separation.

Required behavior:

```text
TEST credential + LIVE operation -> REJECT
SANDBOX operation + LIVE credential -> REJECT
LIVE operation without explicit LIVE context -> REJECT
```

---

### `authorization_bridge.py`

Consumes Phase 10 `AuthorizationRecord`.

Validates:

- expiration,
- mission binding,
- capability,
- resource scope,
- action hash,
- authorization nonce,
- approval state.

This module may validate authorization but may not create it.

---

### `idempotency.py`

External operation replay barrier.

Requirements:

- deterministic operation key,
- atomic registration,
- duplicate mutation rejection,
- bounded retention,
- thread-safe behavior.

---

### `rate_limiter.py`

Provider- and capability-scoped rate control.

Requirements:

- bounded request rate,
- burst limits,
- retry-after handling,
- no automatic escalation of limits,
- deterministic fail-closed behavior when limits are exceeded.

---

### `provider.py`

Abstract provider contract.

Every provider must implement:

```text
provider_id
environment
supported_operations
execute(request)
health()
```

No provider may bypass `AuthorizationBridge`.

---

### `mock_social_provider.py`

Deterministic test provider representing a social platform.

Supported operations:

- create draft,
- edit draft,
- read analytics,
- schedule content,
- publish content.

Provider state must remain local to the test sandbox.

---

### `integration_controller.py`

Primary Phase 13 entry point.

Pipeline:

```text
validate request
   -> validate capability
   -> validate authorization
   -> validate environment
   -> validate resource scope
   -> validate rate limit
   -> reserve idempotency key
   -> retrieve credential
   -> invoke provider
   -> validate provider response
   -> record integration event
   -> return normalized outcome
```

The order is intentional: **credential retrieval must occur only after authorization and boundary checks succeed.**

---

### `integration_ledger.py`

Append-only, hash-linked integration audit ledger.

It must integrate conceptually with Phase 7/10/11/12 audit records without becoming a replacement for those ledgers.

---

### `reconciliation.py`

Validates external outcome consistency:

- requested operation,
- authorized operation,
- provider operation,
- reported result.

A mismatch must produce a reconciliation failure rather than silently marking success.

---

### `circuit_breaker.py`

Provider failure containment.

Trip on configurable repeated provider failures.

When open:

```text
external execution -> BLOCKED
```

No automatic policy mutation or authorization widening.

---

### `__init__.py`

Export only the intended Phase 13 public API.

---

# 5. Test Suite

Create:

```text
Visual-Intelligence/product/backend/tests/integration_boundary/
```

## Required test modules

### `test_models.py`

Validate:

- immutable models,
- no secret fields,
- empty value rejection,
- boolean type confusion,
- malformed operation rejection.

### `test_capability_mapping.py`

Test:

- valid provider-to-Phase-10 mapping,
- unsupported operation rejection,
- generic admin/bypass rejection,
- capability mismatch.

### `test_credential_gateway.py`

Test:

- opaque references,
- authorization-before-credential-access,
- secret non-leakage,
- unavailable credential failure,
- no credential discovery.

### `test_environment_guard.py`

Test all sandbox/live mismatch combinations.

### `test_authorization_bridge.py`

Test:

- expired authorization,
- wrong mission,
- wrong capability,
- wrong scope,
- wrong action hash,
- missing approval,
- valid authorization.

### `test_idempotency.py`

Test:

- duplicate mutation,
- concurrent registration race,
- deterministic key generation,
- bounded retention.

### `test_rate_limiter.py`

Test:

- provider limits,
- capability limits,
- burst limits,
- retry-after handling.

### `test_mock_social_provider.py`

Test deterministic provider behavior and failure simulation.

### `test_integration_controller.py`

Test the full controlled invocation pipeline.

### `test_reconciliation.py`

Test provider-result mismatch and tampering.

### `test_circuit_breaker.py`

Test repeated failures, open state, recovery, and fail-closed execution.

### `test_phase13_security_boundary.py`

Threat matrix tests covering all T13 controls.

### `test_phase13_isolation.py`

AST/runtime tests proving:

- no direct `ExecutionGate` manipulation,
- no authorization creation,
- no credential leakage,
- no Phase 4 research dependency,
- no security-policy mutation.

### `test_phase13_real_workflow.py`

Mandatory end-to-end benchmark.

---

# 6. Threat Model

## T13-1 — Unauthorized Provider Invocation

Attacker attempts to call a provider adapter without a valid Phase 10 authorization.

**Required result:** fail closed.

---

## T13-2 — Authorization Forgery

Malformed or fabricated `AuthorizationRecord`.

**Required result:** reject before credential retrieval.

---

## T13-3 — Scope Confusion

Valid authorization for one capability/resource is reused for another.

**Required result:** `AuthorizationScopeMismatchError`.

---

## T13-4 — Credential Leakage

Secret enters staff context, memory, audit log, exception, or artifact.

**Required result:** zero secret exposure.

---

## T13-5 — Sandbox-to-Live Confusion

Test credentials or sandbox operations reach a live provider.

**Required result:** reject.

---

## T13-6 — Replay

Previously executed external action is submitted again.

**Required result:** idempotency barrier rejects duplicate mutation.

---

## T13-7 — Concurrent Replay Race

Two threads attempt the same external mutation simultaneously.

**Required result:** exactly one reservation succeeds.

---

## T13-8 — Provider Failure Amplification

Provider timeout or repeated failure causes uncontrolled retries.

**Required result:** bounded retry behavior and circuit breaker.

---

## T13-9 — Rate Limit Bypass

Agent attempts to bypass provider or capability limits.

**Required result:** no bypass path exists.

---

## T13-10 — Provider Response Tampering

Malformed or inconsistent provider response is returned as success.

**Required result:** reconciliation failure.

---

## T13-11 — Learned Authorization Escalation

Phase 9 learned strategy attempts to increase external permissions.

**Required result:** reject.

---

## T13-12 — Research Escalation

Phase 4 FROST artifact presented as production authorization.

**Required result:** reject.

---

## T13-13 — Adapter Authorization Bypass

A provider adapter directly invokes execution functionality.

**Required result:** AST/runtime isolation test failure if attempted.

---

## T13-14 — Cross-Mission Credential/Authorization Confusion

Mission A authorization or credential reference is used for Mission B.

**Required result:** fail closed.

---

## T13-15 — Audit Suppression

External operation executes without producing an integration ledger event.

**Required result:** operation is considered unsuccessful / integration boundary violation.

---

## T13-16 — Circuit Breaker Circumvention

Agent routes around an open provider circuit.

**Required result:** all operations for the affected provider/environment remain blocked.

---

# 7. Mandatory Real Workflow Benchmark

The benchmark must use a deterministic mock social platform first.

### Scenario: NOCAP Monthly Campaign

The mission should:

1. Receive a user-defined campaign objective.
2. Phase 8 staff produce strategy, trend research, visual direction, and content.
3. Phase 9 contributes bounded learned preferences and historical workflow signals.
4. Phase 11 creates the mission and task graph.
5. Phase 12 coordinates resources.
6. Phase 10 performs dry-run and obtains human authorization for one explicit external capability.
7. Phase 13:
   - validates the authorization,
   - validates mission/resource scope,
   - checks environment,
   - checks rate limits,
   - acquires an opaque test credential,
   - executes `CREATE_DRAFT`,
   - receives a deterministic provider response,
   - reconciles the result,
   - records the integration event.
8. The benchmark then attempts:
   - unauthorized publish,
   - wrong-capability reuse,
   - cross-mission authorization reuse,
   - duplicate draft creation,
   - sandbox/live mismatch,
   - simulated provider timeout.
9. All prohibited operations must fail closed.
10. The final audit/integration ledgers must verify intact hash chains.

### Required benchmark assertions

```text
authorized CREATE_DRAFT      -> SUCCESS
unauthorized PUBLISH_CONTENT -> BLOCKED
cross-mission reuse          -> BLOCKED
duplicate mutation           -> BLOCKED
sandbox/live mismatch        -> BLOCKED
provider timeout             -> FAIL-CLOSED
audit integrity              -> PASS
ExecutionGate bypass        -> IMPOSSIBLE
```

---

# 8. Verification Plan

Run the full regression suite:

```bash
python -m pytest tests/security_substrate tests/frost_prototype tests/workflow_integration tests/agentic_work tests/execution_control tests/mission_control tests/coordination tests/integration_boundary -v
```

Acceptance requirements:

1. All pre-Phase-13 tests remain green.
2. All Phase-13 tests pass.
3. No test modifies existing security-boundary semantics.
4. No test requires production credentials.
5. No test contacts a real external social platform.
6. No raw secret appears in test output.
7. AST isolation checks pass.
8. Mandatory real workflow benchmark passes.
9. Integration ledger integrity passes.
10. `ExecutionGate.is_permitted()` remains `False` unless an existing, explicitly authorized Phase 10 execution path is being exercised.

---

# 9. Governance Requirements

Phase 13 is **not authorized** to introduce:

- autonomous credential acquisition,
- production secret-manager infrastructure,
- unrestricted OAuth scope negotiation,
- arbitrary HTTP execution by agents,
- browser automation as a bypass,
- direct database mutation,
- provider admin privileges,
- autonomous account creation,
- autonomous authorization approval,
- automatic publication without existing Phase 10 authorization,
- automatic security-policy mutation,
- FROST-based production authorization,
- replacement of the existing Human Authorization Boundary.

Any such capability requires a future explicit governance directive.

---

# 10. Acceptance Criteria

Phase 13 may be considered complete only when:

- [ ] Every external operation maps to a Phase 10 capability.
- [ ] No adapter can create or modify authorization.
- [ ] Credential access occurs only after authorization validation.
- [ ] Sandbox/live boundaries are mechanically enforced.
- [ ] Mission and resource scopes remain intact.
- [ ] External mutations are idempotency-protected.
- [ ] Provider rate limits are enforced.
- [ ] Provider failures are bounded.
- [ ] Provider responses are reconciled.
- [ ] Every invocation is auditable.
- [ ] No secrets appear in logs, records, prompts, or exceptions.
- [ ] Phase 9 learning cannot elevate permissions.
- [ ] Phase 4 research cannot become production authorization.
- [ ] Existing 373-test baseline remains green.
- [ ] Phase 13 tests pass.
- [ ] Mandatory NOCAP workflow benchmark passes.
- [ ] Governance review is independently documented.
- [ ] Final verdict is `PASS` or `PASS WITH LIMITATIONS`.

---

# 11. Required Documentation Deliverables

The engineer must create:

1. `PHASE-13-INTEGRATION-ARCHITECTURE.md`
2. `PHASE-13-INTEGRATION-SECURITY-REVIEW.md`
3. `PHASE-13-THREAT-MODEL.md`
4. `PHASE-13-TEST-REPORT.md`
5. `PHASE-13-REAL-WORKFLOW-REPORT.md`
6. `PHASE-13-GOVERNANCE-GATE.md`

The final governance document must explicitly state:

> Phase 13 provides controlled integration with external services but does not create independent authorization authority. Real-world side effects remain subordinate to the Phase 10 Human Authorization Boundary and all existing security, mission, coordination, and audit controls.

---

# 12. Engineer Instruction

**Do not implement Phase 13 until the user explicitly approves this directive.**

After approval:

1. Inspect the existing Phase 1–12 implementation before modifying anything.
2. Preserve existing public APIs and security invariants.
3. Implement the smallest coherent boundary necessary to satisfy this specification.
4. Prefer deterministic mock providers and local test infrastructure.
5. Do not introduce real production credentials.
6. Do not contact live external services.
7. Do not weaken or refactor existing security controls merely to make Phase 13 easier.
8. Run targeted Phase 13 tests first.
9. Run the complete regression suite afterward.
10. Perform AST/import and runtime isolation audits.
11. Execute the mandatory NOCAP real-workflow benchmark.
12. Produce all six documentation deliverables.
13. Report exact files changed, tests executed, failures encountered, fixes applied, security findings, limitations, and final governance verdict.

**Approval state:** `AWAITING USER GREEN SIGNAL`
