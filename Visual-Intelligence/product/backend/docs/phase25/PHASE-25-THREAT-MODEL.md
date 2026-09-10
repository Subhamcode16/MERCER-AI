# Phase 25: Threat Model & Attack Surface Analysis

## 1. Threat Actors & Vectors
- **Compromised Frontend Client**: Attacker modifies DOM state, alters HTTP request headers, or attempts to claim admin execution authority.
- **Malicious Tenant**: Tenant A attempts to read or mutate Tenant B assets via forged IDs or direct API requests.
- **Deceptive AI Model Response**: LLM produces output attempting to mimic system authorization or trigger unauthorized actions.
- **Untrusted MCP Server**: MCP server attempts to request wildcard system access or return forged telemetry.

## 2. Mitigations & Defensive Controls
| Threat Vector | Defensive Control | Validation Test |
|---|---|---|
| Forged Approval ID | Ephemeral token lookup in `ApprovalService` | `test_t25_002_forged_approval_id` |
| Cross-Tenant Snooping | `TenantGuard` middleware and `PermissionGuard` scoping | `test_t25_005_client_a_accesses_client_b` |
| CoT / Secret Leakage | `DTOSanitizer` recursive scrubbing | `test_t25_013_chain_of_thought_leakage`, `test_t25_014_secret_leakage_through_dto` |
| Replay & Race Conditions | `expected_version` lock matching (409 Conflict) | `test_t25_018_stale_dashboard_action` |
| WebSocket Eavesdropping | Tenant-client scoped event stream bus | `test_t25_020_cross_client_websocket_leakage` |
