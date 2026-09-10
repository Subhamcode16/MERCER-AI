# Phase 26: ILYREN Creative Workforce Product Layer Architecture

## 1. Executive Summary & Core Invariant

Phase 26 establishes the **Creative Workforce Product Layer** for the ILYREN Creative Intelligence Platform. It transitions the system from an "agent execution engine" to a **governed digital creative organization** where persistent AI coworkers with stable identities collaborate with humans in Campaign Rooms under strict policy controls.

```
                    HUMAN / CLIENT / STUDIO
                             |
                             v
                  +-----------------------+
                  | Workforce Experience  |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Workforce Orchestrator|
                  +-----------+-----------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
   Worker Identity       Campaign Rooms      Routines
          |                   |                   |
          v                   v                   v
       Skills             Handoffs          Work Triggers
          |                   |                   |
          +-------------------+-------------------+
                              |
                              v
                  +-----------------------+
                  | Capability / Tool     |
                  | Binding Boundary      |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Intelligence Layer    |
                  | Visual DNA / Knowledge|
                  | Strategy / Reasoning  |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Production Fabric     |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Authorization /       |
                  | Execution Control     |
                  +-----------+-----------+
                              |
                              v
                       EXTERNAL SYSTEMS
```

### Governing Invariants:
$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$
$$\mathbf{Role \neq Permission} \quad \mathbf{Skill \neq Authority} \quad \mathbf{Routine \neq Authorization} \quad \mathbf{Collaboration \neq Privilege\ Transfer}$$
$$\mathbf{Worker\ Output \neq Truth \neq Permission} \quad \mathbf{Memory \neq Policy} \quad \mathbf{Shared\ Context \neq Shared\ Authority}$$

## 2. Core Subsystems

1. **Worker Identity & Lifecycle**: Stable persistent IDs, distinct from runtime/session IDs. Lifecycle: `DRAFT`, `ACTIVE`, `PAUSED`, `RESTRICTED`, `SUSPENDED`, `RETIRED`.
2. **Capability Binding**: Explicit capability manifests with deterministic resolution and zero wildcard allowances (`*` forbidden).
3. **Skill Registry & Runtime**: Immutable SemVer skills (`skill_id@version`) evaluated against boundary tests.
4. **Scoped Memory Store**: 6-tier partitioning (`SESSION`, `CAMPAIGN`, `CLIENT`, `BRAND`, `WORKER`, `INSTITUTIONAL`) with anti-poisoning and cross-client isolation.
5. **Campaign Rooms & Collaboration Hub**: Structured workspaces with shared artifacts, discussions, and decision tracking.
6. **Governed Handoffs & Bounded Delegation**: Cryptographic SHA-256 artifact hashes, depth limits (Max Depth 3), and zero privilege transfer.
7. **Routines & Approval Bridge**: Advisory dry-run routines, replay protection, and direct integration into Phase 25 `ApprovalService`.
8. **Workforce Observability & Activity Stream**: 20+ typed events sanitized of secrets and chain-of-thought.
