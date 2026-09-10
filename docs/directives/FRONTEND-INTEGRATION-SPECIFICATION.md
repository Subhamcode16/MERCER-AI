# FRONTEND INTEGRATION SPECIFICATION: ILYREN Autonomous Fashion Studio

## Executive Overview

This specification establishes the comprehensive frontend architectural roadmap for the **ILYREN Autonomous Fashion Studio**. It maps backend capabilities across **Phases 14 through 20** to explicit UI components, API client endpoints, state management schemas, user interactions, and security boundary visual indicators.

---

## Governing Invariant UI Principles

1. **Human Authorization Authority:** Side-effecting actions must display explicit `APPROVED_FOR_HUMAN_AUTHORIZATION` badges requiring human sign-off (Phase 10 / Phase 16).
2. **Trust Classification Visibility:** External MCP tool responses and unvalidated trend observations must feature prominent `UNTRUSTED_EXTERNAL_OBSERVATION` visual indicators.
3. **Strict Presentation Policy Filtering:** Client-facing views must strip raw LLM prompts, chain-of-thought reasoning, internal staff discussion logs, and system credentials.
4. **Non-Executable Intelligence Controls:** Workforce evolution recommendations and strategy experiments must present advisory-only action surfaces (`executed = False`).
5. **Client Isolation Scoping:** Client context switchers must enforce strict workspace isolation via `ContextGuard` tokens, preventing cross-client data view leakage.

---

## Detailed Component Matrix by Phase Backend Architecture

### 1. Phase 20: Model Gateway, Visual Gateway & MCP Connectivity

```text
+-----------------------------------------------------------------------------------+
|                           PHASE 20 FRONTEND CONTROL SURFACE                       |
+-----------------------------------------------------------------------------------+
|  +---------------------------+  +-------------------------+  +-----------------+  |
|  | LLM Provider Console      |  | Visual Model Studio     |  | MCP Connector   |  |
|  | - Live Provider Status    |  | - Aspect Ratio Selector |  | - Allowlist     |  |
|  | - Provenance Inspector    |  | - Lineage Graph Viewer  |  | - Trust Badge   |  |
|  | - Redaction Auditor       |  | - Critique Swatches     |  | - Idempotency   |  |
|  +---------------------------+  +-------------------------+  +-----------------+  |
|  +-----------------------------------------------------------------------------+  |
|  | Visual Knowledge Benchmark & Failure Taxonomy (250-Case VQ-01..10 Dashboard)   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

#### A. LLM Provider Management Console (`src/model_gateway/`)
- **Active Provider Status Card:** Real-time indicator for `GeminiLiveProvider` (Google AI Studio `gemini-2.5-flash` / `gemini-1.5-pro`) vs `SandboxLLMProvider` fallback state.
- **Model Request Provenance Inspector:** Modal panel rendering `ResponseProvenance` DTOs (`request_id`, `provider`, `model_version`, `timestamp`, `policy_version`, `structured_output_validated`).
- **Token & Latency Monitor:** Real-time gauge for token budget reservation, latency ($\text{ms}$), and cost tracking.
- **Credential Security Badge:** Status pill verifying active prompt redaction (`CredentialRedactor`).

#### B. Visual Model Studio & Asset Lineage Inspector (`src/visual_model_gateway/`)
- **Asset Generation Control Panel:**
  - Aspect ratio radio selectors (`1:1`, `9:16`, `16:9`, `4:5`).
  - Quality mode toggles (`STANDARD`, `HIGH`, `ULTRA`).
  - Visual DNA reference binder selector.
- **Interactive Visual Lineage Graph Viewer:**
  - Node graph rendering artifact ID, parent artifact link, model/version, prompt request hash, creative direction hash, and Visual DNA ref.
- **Vision Analysis & Critique Overlay:**
  - Image canvas with defect bounding boxes, extracted HSL color swatches, typography tags, and critique confidence meter ($\ge 90\%$).

#### C. MCP Server & Tool Connector Center (`src/mcp_gateway/`)
- **Server Registry Table:** Displays registered servers (`mcp_fashion_trends`), risk class badges (`LOW`, `MEDIUM`, `HIGH`), and approved capability allowlists.
- **Wildcard Capability Warning Banner:** Rejects any `*` / `admin` capability requests with immediate visual error notices.
- **Trust Classification Badges:** Prominent `UNTRUSTED_EXTERNAL_OBSERVATION` badge on all external research and tool results.
- **Resilience Telemetry:** Circuit breaker status (`CLOSED` / `OPEN`), rate-limit meters, and idempotency key (`ik_...`) trackers.

#### D. Visual Knowledge Benchmark & Failure Taxonomy Dashboard (`src/visual_knowledge/`, `src/intelligence_evaluation/`)
- **250-Case Benchmark Summary Grid:** Filterable view across 18 visual categories (Brand Identity, Typography, Color, Layout, Grid, Composition, Fashion, Trend, Adversarial, etc.).
- **Visual Task Scorecards (`VQ-01` through `VQ-10`):** Individual task accuracy meters (Visual Description, Visual DNA, Brand Alignment, Critique Precision, Revision Recovery, Cross-Client Generalization).
- **Failure Taxonomy Inspector (`GAP-A` through `GAP-J`):** Detailed error breakdown tagging missing knowledge, retrieval, reasoning, perception, context, or workflow failures with training candidate indicators.

---

### 2. Phase 19: Creative Intelligence Network & Institutional Memory

- **Dual-Namespace Graph Visualizer (`src/creative_intelligence/knowledge_graph.py`):**
  - Toggle between **Client Namespace** (Client, Campaign, Deliverable) and **Studio-Global Namespace** (Institutional Pattern, Validated Strategy).
  - Cross-client node edge restriction alert (`ClientDataLeakageError`).
- **De-identification Pipeline Verification Badge:** Visual proof that global patterns retain zero raw PII or client metadata (`CrossClientPattern != CrossClientData`).
- **Institutional Strategy Lifecycle Timeline:**
  - Interactive versioned strategy timeline (`PROPOSED` $\rightarrow$ `VALIDATED` $\rightarrow$ `ACTIVE` $\rightarrow$ `RETIRED` $\rightarrow$ `ROLLED_BACK`).
  - One-click baseline rollback control to revert degraded strategies.
- **Workforce Evolution Advisory Panel (`src/creative_intelligence/workforce_evolution.py`):**
  - Non-executable advisory cards (`requires_human_approval = True`, `executed = False`) displaying rationale, evidence pattern IDs, and prompt optimization suggestions.

---

### 3. Phase 18: Studio Intelligence & Closed-Loop Operations

- **Creative Outcome Attribution Dashboard (`src/studio_intelligence/attribution.py`):**
  - Multi-factor attribution cards linking campaign performance to staff roles, visual DNA, and copy strategies.
- **Continuous Studio Optimizer Panel (`src/studio_intelligence/continuous_optimizer.py`):**
  - A/B strategy experiment benchmarking view comparing `CANDIDATE_STRATEGY` vs `BASELINE`.
  - Degradation rejection alert (`OptimizationRejectedError`).

---

### 4. Phase 17: Production Fabric & Delivery Pipeline

- **Fabric Pipeline Tracker (`src/production_fabric/`):**
  - Real-time kanban across production stages: `Intake` $\rightarrow$ `Processing` $\rightarrow$ `Validation` $\rightarrow$ `Review` $\rightarrow$ `Delivery`.
  - Autonomy ceiling indicator.

---

### 5. Phase 16: Client Experience Command Center

- **Governed Client Presentation Surface (`src/client_experience/`):**
  - Clean client DTO views stripped of internal chain-of-thought, system prompts, or raw model logs.
- **Human Authorization Gate Modal:**
  - Interactive approval surface for campaign launch, asset delivery, and side-effecting operations.

---

### 6. Phase 14 & 15: Governed Creative Workforce & Studio Operations

- **6 Core Workforce Role Cards:**
  - `TREND_ANALYST`: Tool research & visual analysis.
  - `STRATEGIST`: Institutional intelligence & campaign synthesis.
  - `DESIGNER`: Visual model generation & Visual DNA adherence.
  - `CONTENT_SPECIALIST`: Brand copy creation.
  - `CRITIC`: Automated defect detection & critique.
  - `REVIEWER`: Independent governance evaluation.
- **Context-Scoped Client Switcher:** Enforces strict workspace boundary isolation via `ContextGuard`.

---

## State Management & API DTO Architecture

```typescript
// Shared Types & API DTOs for Frontend State

export type TrustClassification = 'UNTRUSTED_EXTERNAL_OBSERVATION' | 'EVALUATED_FACT';

export interface ResponseProvenanceDTO {
  provider: string;
  model: string;
  modelVersion: string;
  requestId: string;
  timestamp: number;
  policyVersion: string;
  structuredOutputValidated: boolean;
  requestHash: string;
}

export interface ImageGenerationResponseDTO {
  artifactId: string;
  requestId: string;
  imageUrlOrBytes: string;
  aspectRatio: '1:1' | '9:16' | '16:9' | '4:5';
  width: number;
  height: number;
  lineage: {
    artifact_id: string;
    parent_artifact_id?: string;
    model_name: string;
    request_hash: string;
    creative_direction_hash: str;
    visual_dna_ref?: string;
    validation_status: 'VALIDATED' | 'FAILED';
  };
  status: 'SUCCESS' | 'FAILED';
}

export interface MCPInvocationResultDTO {
  invocationId: string;
  requestId: string;
  serverId: string;
  toolName: string;
  success: boolean;
  sanitizedOutput: Record<string, any>;
  trustClassification: TrustClassification;
}

export interface BenchmarkMetricsDTO {
  visualObservationAccuracy: number;
  visualDnaAccuracy: number;
  brandAlignmentAccuracy: number;
  critiquePrecision: number;
  revisionSuccessRate: number;
  reliabilityScore: number;
  passedAllGates: boolean;
}
```

---

## Implementation Checklist for Frontend Engineers

- [ ] Connect `ModelGateway` API client to LLM Provider Status Console.
- [ ] Build `VisualModelStudio` component with aspect ratio selector & Lineage Graph modal.
- [ ] Implement `MCPConnectorCenter` table with capability allowlist badges & trust classification pills.
- [ ] Build `VisualKnowledgeBenchmark` dashboard rendering 250 cases, 10 VQ tasks, and GAP-A..J failure taxonomy cards.
- [ ] Integrate Dual-Namespace Graph visualizer with client isolation filters.
- [ ] Build Advisory Workforce Evolution cards with non-executable UI states.
- [ ] Connect Human Authorization Gate modal for side-effect approvals.
- [ ] Verify Presentation Policy filter on all client-facing DTOs.
