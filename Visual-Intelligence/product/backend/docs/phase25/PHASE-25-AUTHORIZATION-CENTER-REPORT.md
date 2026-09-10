# Phase 25: Authorization Center Subsystem Report

## 1. Overview
The Authorization Center (`src/authorization_center/`) serves as the strict gatekeeper between human governance and autonomous execution.

## 2. Core Architectural Invariant
$$\mathbf{Approval \neq Command} \quad \mathbf{Execution\ Requires\ Valid,\ Unexpired\ Cryptographic\ Token}$$

The Authorization Center enforces:
1. **Multi-Role Separation**: Distinct roles required for requesting vs approving vs executing high-risk operations.
2. **Approval Lifecycle & Expiration**: Approval requests have explicit TTL windows (`expires_at`). Expired or revoked requests are strictly rejected when submitted for execution.
3. **Cryptographic Execution Tokens**: Approved items generate an ephemeral, single-use `execution_token_id` valid only for the specified action, tenant, and client.
4. **Evidence Linkage**: Approvals capture cryptographic hash fingerprints of underlying artifacts, model recommendations, and risk matrices.
