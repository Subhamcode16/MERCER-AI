# Phase 25: Institutional Production Control Plane & Productization Boundary Architecture

## 1. Executive Summary & Core Invariant

Phase 25 establishes the definitive human-facing operational control plane and productization boundary for the Mercer Visual-Intelligence platform. It transforms the autonomous intelligence and workflow engines into an auditable, multi-tenant, operator-governed institutional environment.

The system strictly enforces the non-negotiable architectural invariant:
$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$
$$\mathbf{Visibility \neq Authorization} \quad \mathbf{Recommendation \neq Command} \quad \mathbf{Model\ Output \neq Truth \neq Permission}$$
$$\mathbf{Dashboard\ Access \neq Execution\ Authority} \quad \mathbf{Cross\text{-}Client\ Pattern \neq Cross\text{-}Client\ Data}$$

```
+-----------------------------------------------------------------------------------------+
|                                OPERATOR CONSOLE / CLIENT UI                             |
|  - Role-based navigation & views                                                        |
|  - Real-time scoped event stream                                                        |
|  - Zero Secret & Zero CoT leakage DTOs                                                  |
+--------------------------------------------+--------------------------------------------+
                                             | HTTP / REST (Scoped Bearer Token)
                                             v
+-----------------------------------------------------------------------------------------+
|                                      API BOUNDARY                                       |
|  - TenantGuard Middleware (Subdomain / Path / Header resolution)                        |
|  - SecurityContext extraction & Token validation                                        |
|  - RateLimiter (SlowAPI token bucket)                                                   |
+--------------------------------------------+--------------------------------------------+
                                             | Scoped Request Context
                                             v
+-----------------------------------------------------------------------------------------+
|                                  CONTROL PLANE SERVICE                                  |
|  - PermissionGuard: Server-side RBAC & Capability check                                 |
|  - Optimistic Concurrency Engine (Expected Version checking)                            |
|  - Comprehensive Audit Logger                                                           |
+-----+-------------------+-------------------+-------------------+-------------------+---+
      |                   |                   |                   |                   |
      v                   v                   v                   v                   v
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
|  CAMPAIGN   |     |AUTHORIZATION|     |INTELLIGENCE |     |  PROVIDER   |     |   VISUAL    |
|   COMMAND   |     |   CENTER    |     | OBSERVATORY |     | & MCP CNTRL |     | OBSERVATORY |
| State/Deps/ |     | Multi-role  |     | Advisory    |     | Circuit Brk |     | Drift/Qual/ |
| Deliverable |     | Expiry/Token|     | Metrics/Gaps|     | Masked Creds|     | Quarantine  |
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
```

## 2. Core Architectural Pillars

### 2.1 Server-Side RBAC & Capability Guard
All UI actions must pass through `PermissionGuard.validate_access(context, required_capability, resource_tenant_id, resource_client_id)`. The UI holds zero authority:
- `SUPER_ADMIN`: Cross-tenant administrative operations.
- `OPERATOR`: Operational execution within assigned tenant.
- `AUDITOR`: Read-only telemetry, evidence, and compliance views.
- `CLIENT_USER`: Scoped strictly to assigned `tenant_id` and `client_id`.

### 2.2 DTO Sanitization & Data Boundary
Before any data leaves the server boundary to the event bus or HTTP responses, `DTOSanitizer.sanitize()` recursively strips:
- API keys, credentials, secret hashes, passwords, and private tokens.
- Internal chain-of-thought (CoT), model system prompts, raw reasoning traces, and hidden scratchpads.
- Public reference tokens (`execution_token_id`, `token_id`, `brand_tokens`, `total_tokens`) are retained strictly for reference tracking.

### 2.3 Optimistic Concurrency & Replay Protection
Every mutating payload requires `expected_version`. If the state version in memory or database does not match, a `409 Conflict` is raised. Retried or duplicated operations with obsolete versions are safely rejected without state corruption.

### 2.4 Controlled Event Stream Isolation
The in-memory event stream bus enforces tenant/client scoping:
- `tenant:client` channels receive strictly tenant/client matched events.
- Client listeners never receive broadcast events belonging to adjacent clients or global administrative telemetry.
