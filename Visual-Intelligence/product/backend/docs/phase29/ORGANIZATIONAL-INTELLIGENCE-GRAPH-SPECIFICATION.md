# ORGANIZATIONAL-INTELLIGENCE-GRAPH-SPECIFICATION.md
## Phase 29 Architecture Specification: Organizational Intelligence Graph

---

### 1. Overview & Graph Topology

The **Organizational Intelligence Graph** is a multi-tenant Directed Property Graph that models relationships across creative assets, marketing decisions, empirical outcomes, hypotheses, scenarios, and strategic recommendations.

```
(Campaign) ──[SUPPORTS]──> (Strategic Signal) ──[INFORMS]──> (Hypothesis)
                                 │                               │
                                 └──[INFORMS]──> (Scenario) <────┘
                                                     │
                                                     └──[INFORMS]──> (Recommendation) ──[DECIDED_BY]──> (Human Decision)
```

---

### 2. Supported Entity Types (22 Entities)

- `CLIENT`, `BRAND`, `PRODUCT`, `AUDIENCE`, `CAMPAIGN`, `CAMPAIGN_DECISION`
- `CREATIVE_DIRECTION`, `ASSET`, `ASSET_VERSION`, `OUTCOME`, `EXPERIMENT`
- `LEARNING_SIGNAL`, `KNOWLEDGE_CLAIM`, `VISUAL_DNA_TOKEN`, `WORKER`, `SKILL`
- `HYPOTHESIS`, `STRATEGIC_SIGNAL`, `SCENARIO`, `RECOMMENDATION`, `HUMAN_DECISION`
- `RISK`, `OPPORTUNITY`, `EXTERNAL_OBSERVATION`

---

### 3. Cryptographic Provenance & Invariant Guarantees

1. **Entity Provenance Hashing:** Each entity carries a deterministic SHA-256 hash of its core attributes and provenance chain.
2. **Strict Multi-Tenant Isolation:** Access to `CLIENT_PRIVATE` entities is strictly gated by tenant key. Traversal attempts by foreign tenants raise `TenantAccessViolation`.
3. **Institutional & Public Linking:** Private tenant entities may link to `INSTITUTIONAL` or `PUBLIC_EXTERNAL` nodes, but bridging distinct client-private nodes is strictly prohibited.
4. **Bidirectional Evidence Traversal:** Supports reverse lineage tracing from recommendations back to raw campaign decisions and empirical metrics.
