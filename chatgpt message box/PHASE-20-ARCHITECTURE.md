# Phase 20: ILYREN Model Integration, MCP Connectivity & Visual Intelligence Architecture

## Executive Summary

Phase 20 turns the governed ILYREN control plane into a **real model-backed creative workforce** and empirically measures its visual intelligence baseline. It introduces provider-neutral LLM, Visual, and MCP Gateways while maintaining immutable security boundaries:

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$
$$\mathbf{Learning \neq Security\ Policy\ Mutation}$$
$$\mathbf{External\ Observation \neq Trusted\ Fact}$$
$$\mathbf{Self\!\!-\!Improvement \neq Self\!\!-\!Authorization}$$
$$\mathbf{Creative\ Review \neq Execution\ Authorization}$$
$$\mathbf{External\ Tool\ Access \neq Blanket\ Provider\ Access}$$
$$\mathbf{Model\ Output \neq Truth \neq Permission}$$
$$\boxed{\mathbf{ILYREN\ becomes\ more\ capable\ without\ becoming\ more\ authoritative}}$$

---

## High-Level Topology

```
+-----------------------------------------------------------------------------------+
|                           HUMAN / CLIENT GOVERNANCE                              |
+-----------------------------------------------------------------------------------+
                                          | Human Authorization (Phase 10)
                                          v
+-----------------------------------------------------------------------------------+
|                           STUDIO CONTROL PLANE (Phases 14-19)                     |
+-----------------------------------------------------------------------------------+
|  +-------------------------+  +-----------------------+  +---------------------+  |
|  | TREND_ANALYST           |  | STRATEGIST            |  | DESIGNER            |  |
|  | (MCP + LLM + Vision)    |  | (LLM + Institutional) |  | (Visual Model + DNA)|  |
|  +-------------------------+  +-----------------------+  +---------------------+  |
|  +-------------------------+  +-----------------------+  +---------------------+  |
|  | CONTENT_SPECIALIST      |  | CRITIC                |  | REVIEWER            |  |
|  | (LLM + Brand Context)   |  | (Vision Analysis)     |  | (Gov Config)        |  |
|  +-------------------------+  +-----------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                          | Model Generation Requests
                                          v
+-----------------------------------------------------------------------------------+
|                               PHASE 20 GATEWAYS                                   |
+-----------------------------------------------------------------------------------+
|  +-------------------------+  +-----------------------+  +---------------------+  |
|  | LLM Model Gateway       |  | Visual Model Gateway  |  | MCP Gateway         |  |
|  | - Redaction & Policy    |  | - Lineage Tracing     |  | - Allowlisting      |  |
|  | - Token Budget          |  | - Aspect Validation   |  | - Circuit Breaker   |  |
|  +-------------------------+  +-----------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                          | Telemetry & Output
                                          v
+-----------------------------------------------------------------------------------+
|                 INTELLIGENCE EVALUATION & VISUAL KNOWLEDGE BENCHMARK              |
|  - 250 Ground-Truth Cases (18 Categories, Tasks VQ-01..VQ-10)                     |
|  - Failure Taxonomy (GAP-A through GAP-J)                                         |
|  - Cryptographic Audit Ledgers (Model, Visual, MCP)                               |
+-----------------------------------------------------------------------------------+
```

---

## Key Subsystems

### 1. LLM Model Gateway (`src/model_gateway/`)
- Provider-neutral gateway mapping workforce tasks to model capabilities.
- Credentials scrubbed via `CredentialRedactor` before sending prompts.
- Token budgets and timeout/retry policies enforced.
- Provable provenance attached to every response (`ResponseProvenance`).

### 2. Visual Model Gateway (`src/visual_model_gateway/`)
- Handles visual generation and vision analysis.
- Attaches immutable `VisualLineage` (artifact ID, request hash, Visual DNA ref).
- Validates aspect ratios (`1:1`, `9:16`, `16:9`, `4:5`) and resolution bounds.

### 3. MCP Gateway (`src/mcp_gateway/`)
- Controlled transport for external Model Context Protocol tools.
- Rejects wildcard permissions (`*`, `admin`, `full_access`).
- Classifies all tool outputs as `UNTRUSTED_EXTERNAL_OBSERVATION`.
- Protected by rate limiters, circuit breakers, and idempotency controls.

### 4. Visual Knowledge Baseline & Failure Taxonomy (`src/visual_knowledge/`, `src/intelligence_evaluation/`)
- 250 ground-truth evaluation cases across 18 visual categories.
- Evaluates 10 visual tasks (`VQ-01` to `VQ-10`).
- Classifies failures into `GAP-A` through `GAP-J` taxonomy before fine-tuning.
