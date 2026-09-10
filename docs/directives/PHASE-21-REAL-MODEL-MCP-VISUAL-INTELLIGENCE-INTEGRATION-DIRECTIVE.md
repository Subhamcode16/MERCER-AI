# PHASE-21 — Real Model, MCP & Visual Intelligence Integration Directive

**Project:** ILYREN Creative Workforce / ILYREN Creative Studio  
**Phase:** 21  
**Status:** READY FOR ENGINEERING EXECUTION  
**Predecessor:** Phase 20 — Model Integration, MCP Connectivity & Visual Intelligence Benchmark Boundary

---

## 1. Executive Objective

Phase 20 established provider-neutral gateways and benchmark infrastructure. Phase 21 must convert those abstractions into **verified real-world capability**.

The engineer must:

1. Integrate real LLM providers through `src/model_gateway/`.
2. Integrate real vision/image-generation providers through `src/visual_model_gateway/`.
3. Integrate real MCP servers/tools through `src/mcp_gateway/`.
4. Connect real models to the Phase 14 creative workforce through `src/model_workforce/`.
5. Empirically measure ILYREN's visual/creative intelligence.
6. Identify and quantify remaining capability gaps.
7. Determine whether each gap requires prompting, retrieval, tools, routing, data, fine-tuning, or architecture changes.
8. Validate a complete real-model NOCAP creative workflow.
9. Preserve every Phase 1–20 security and authorization invariant.

### Governing Equations

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$

$$\mathbf{Model\ Output \neq Truth \neq Permission}$$

$$\mathbf{External\ Tool\ Access \neq Blanket\ Access}$$

$$\mathbf{Learning \neq Security\ Policy\ Mutation}$$

$$\boxed{\mathbf{ILYREN\ becomes\ more\ capable\ without\ becoming\ more\ authoritative}}$$

---

# 2. Ratified Baseline

Phase 20 is the architectural baseline:

```text
src/model_gateway/
src/visual_model_gateway/
src/mcp_gateway/
src/model_workforce/
src/visual_knowledge/
src/intelligence_evaluation/
```

Phase 20 reported:

```text
267 / 267 tests passed
0 failures
0 errors
0 regressions
```

Do not weaken, delete, or rewrite previous tests merely to accommodate Phase 21.

The engineer must distinguish:

```text
IMPLEMENTED
TESTED
SIMULATED
REAL-PROVIDER-VALIDATED
HUMAN-VALIDATED
PRODUCTION-READY
```

These labels are not interchangeable.

---

# 3. Target Architecture

```text
Human / Client
      ↓
Phase 16 Command Center
      ↓
Phase 15 / 17 Operations
      ↓
Phase 14 Creative Workforce
      ↓
Phase 20 / 21 Model Workforce
      ├───────────────┐
      ↓               ↓
LLM Gateway      Visual Gateway
      ↓               ↓
Real LLMs        Vision / Image Models
      │               │
      └───────┬───────┘
              ↓
          MCP Gateway
              ↓
      Controlled External Tools
              ↓
Visual Knowledge + Intelligence Evaluation
              ↓
Phase 18 / 19 Learning & Institutional Intelligence
```

**No Phase 21 component may bypass Phase 10–13 execution controls.**

---

# 4. Workstream A — Real LLM Integration

Implement at least:

- one real primary LLM provider
- one independent fallback provider
- provider health detection
- model capability metadata
- structured output
- token budgets
- timeouts
- retry classification
- fallback routing
- response normalization
- redaction
- model invocation ledger

Required path:

```text
Staff Role
 → Model Workforce Bridge
 → Model Gateway
 → Routing Policy
 → Provider Adapter
 → External Model
```

Staff roles must not directly instantiate provider SDKs or read API keys.

### Tests

For each provider verify:

- successful inference
- structured output
- malformed output
- timeout
- rate limit
- provider failure
- retry
- fallback
- token exhaustion
- prompt redaction
- secret-leak prevention
- audit recording

---

# 5. Workstream B — Real Vision & Image Generation

Integrate real providers for:

- image understanding
- image generation
- visual comparison
- attribute extraction
- brand consistency
- visual critique
- reference matching

Keep these capabilities separate:

```text
IMAGE GENERATION
IMAGE UNDERSTANDING
IMAGE EDITING
VISUAL COMPARISON
ATTRIBUTE EXTRACTION
BRAND CONSISTENCY
LAYOUT UNDERSTANDING
TYPOGRAPHY UNDERSTANDING
STYLE REASONING
CREATIVE DIRECTION
```

Every generated asset must retain:

```text
request_id
provider
model
timestamp
prompt/version reference
parent artifact
content hash
evaluation record
```

Never store credentials in lineage.

---

# 6. Workstream C — Real MCP Connectivity

Integrate real MCP servers incrementally.

Priority categories:

1. research/search
2. filesystem/project workspace
3. documentation/knowledge
4. design/creative tooling
5. analytics
6. notifications
7. project management
8. approved platform operations

Classify tools:

```text
READ_ONLY
ANALYSIS
DRAFTING
TRANSFORMATION
MUTATION
DESTRUCTIVE
```

Default policy:

```text
READ_ONLY       → autonomous eligible
ANALYSIS        → autonomous eligible
DRAFTING        → bounded
TRANSFORMATION  → bounded
MUTATION        → authorization required
DESTRUCTIVE     → explicit human authorization + elevated controls
```

Required invocation path:

```text
Identity
 → Client Context
 → Mission Context
 → Capability Mapping
 → Environment Guard
 → Schema Validation
 → Credential Boundary
 → Rate Limit
 → Idempotency
 → Circuit Breaker
 → Tool Invocation
 → Result Sanitization
 → Audit Ledger
```

A tool description is never an authorization grant.

---

# 7. Workstream D — Visual Intelligence Benchmark

The central scientific question is:

> **How much visual knowledge does ILYREN actually possess, where does it fail, and what must be learned next?**

Do not produce a single unexplained visual-intelligence percentage.

Minimum benchmark categories:

### VQ-01 — Visual Attributes
Color, material, silhouette, texture, object count, spatial relationships.

### VQ-02 — Composition
Hierarchy, balance, alignment, negative space, focal point, grid, scale, rhythm.

### VQ-03 — Typography
Classification, hierarchy, weight, tracking, alignment, contrast, display/body distinction.

### VQ-04 — Brand Identity
Logo, palette, typography, visual language, tone, consistency.

### VQ-05 — Fashion/Product Understanding
Garment type, construction, fit, material, silhouette, styling, accessories.

### VQ-06 — Art Direction
Mood, palette, composition, styling, photography direction, graphic direction.

### VQ-07 — Reference Matching
Reference-to-output fidelity.

### VQ-08 — Visual Difference Detection
Wrong colors, spacing, typography, layout, missing elements, identity inconsistencies.

### VQ-09 — Creative Critique
Real defect identification versus generic aesthetic commentary.

### VQ-10 — Visual-to-Strategy Reasoning
Audience, positioning, emotion, campaign intent, brand strategy.

---

# 8. Benchmark Dataset Governance

Retain the existing Phase 20 benchmark baseline but create a versioned Phase 21 benchmark.

Recommended structure:

```text
visual_benchmark/
  v1/
    core/
    adversarial/
    negative/
    ood/
  v2/
    expert_reviewed/
    failure_recovery/
    brand_specific/
```

Each case must include:

```yaml
case_id:
category:
difficulty:
input_assets:
prompt:
ground_truth:
acceptable_variants:
scoring_method:
expert_rationale:
failure_tags:
source_provenance:
version:
```

Benchmark versions become immutable once results are recorded.

Do not silently alter cases after scoring.

---

# 9. Human Ground Truth

Creative judgments require expert annotation.

For difficult cases:

```text
Case
 ↓
Expert A
Expert B
Expert C
 ↓
Agreement
 ↓
Adjudication
 ↓
Frozen Ground Truth
```

Measure inter-rater agreement.

If disagreement is material, label the case:

```text
AMBIGUOUS_GROUND_TRUTH
```

Do not treat disputed creative judgments as objective truth.

---

# 10. Intelligence Evaluation

Use the Phase 20 `GAP-A` through `GAP-J` failure taxonomy.

Measure task-appropriate metrics such as:

```text
accuracy
precision
recall
F1
attribute accuracy
semantic similarity
visual difference accuracy
brand consistency
creative-direction quality
critique precision
critique recall
hallucination rate
instruction following
reference fidelity
latency
cost
reliability
```

Report a capability profile, for example:

```text
Visual Attribute Recognition    XX%
Composition Understanding       XX%
Typography Understanding        XX%
Brand Consistency               XX%
Fashion Understanding           XX%
Art Direction                   XX%
Reference Matching              XX%
Difference Detection            XX%
Creative Critique               XX%
Visual→Strategy Reasoning       XX%
```

Also report:

```text
weighted score
confidence interval
sample count
benchmark version
model/provider
failure distribution
OOD performance
adversarial performance
human agreement
```

**Never invent these numbers.**

---

# 11. Capability Gap Discovery

Produce an evidence-derived matrix:

| Gap | Evidence | Severity | Frequency | Business Impact | Next Action |
|---|---|---:|---:|---:|---|
| Example | VQ-03 | High | High | High | Evidence required |

Every weakness must be classified as:

```text
A. Prompt/instruction problem
B. Model-selection problem
C. Context/retrieval problem
D. Knowledge-base problem
E. Tooling problem
F. Benchmark problem
G. Data-quality problem
H. Fine-tuning problem
I. Multimodal architecture problem
J. Fundamental model limitation
```

Test the cheapest viable intervention first:

```text
Prompt
 ↓
Context / Retrieval
 ↓
Tools
 ↓
Model Routing
 ↓
Better Data / Benchmark
 ↓
Fine-Tuning
 ↓
Architecture
```

Do not fine-tune merely because a model fails.

---

# 12. Model Routing Evaluation

Measure role-specific model performance.

Candidate mapping:

```text
TREND_ANALYST        → research/reasoning model
STRATEGIST           → reasoning + long-context model
DESIGNER             → multimodal + image generation
CONTENT_SPECIALIST   → language/content model
CRITIC               → multimodal evaluator
REVIEWER             → independent evaluator
```

The final routing policy must be evidence-driven.

Compare:

```text
quality
latency
cost
reliability
structured-output compliance
visual accuracy
failure recovery
```

Do not select providers solely by reputation.

---

# 13. Real NOCAP Workflow Benchmark

Execute a real model-backed workflow:

```text
Client Objective
 → Trend Research
 → Trend Validation
 → Brand DNA Retrieval
 → Creative Direction
 → Visual Reference Analysis
 → Concept Generation
 → Image Generation
 → Copy Generation
 → Self-Critique
 → Independent Review
 → Revision
 → Human Approval
 → Sandbox External Execution
 → Outcome Observation
 → Performance Evaluation
 → Learning Signal
```

The benchmark must use real providers where credentials/network access permit.

If unavailable, report the exact blocker. Never simulate a real-provider success and label it real.

---

# 14. Multi-Model Creative Council

Run an optional controlled experiment:

```text
Model A → Proposal
Model B → Independent Critique
Model C → Alternative Proposal
Model D → Final Evaluation
Human → Authorization
```

Compare against a single-model baseline on:

```text
quality
revision count
visual errors
brand consistency
time
cost
reviewer agreement
```

Do not assume multi-model collaboration improves results.

---

# 15. Security Invariants

Implement threat tests for:

```text
S21-001  Model self-authorization
S21-002  MCP capability escalation
S21-003  Credential exposure
S21-004  Prompt injection through tool output
S21-005  Prompt injection through image content
S21-006  Cross-client visual memory leakage
S21-007  Cross-client MCP-result leakage
S21-008  Provider fallback bypass
S21-009  Token-budget bypass
S21-010  Model output treated as authorization
S21-011  Image metadata injection
S21-012  Benchmark contamination
S21-013  Ground-truth poisoning
S21-014  Benchmark result tampering
S21-015  Visual lineage tampering
S21-016  Provider replay
S21-017  MCP replay
S21-018  Unauthorized routing mutation
S21-019  Learning-induced security-policy mutation
S21-020  Autonomous destructive MCP invocation
S21-021  Stale authorization reuse
S21-022  Cross-mission authorization reuse
S21-023  Tool-result hallucination acceptance
S21-024  Provider outage cascade
S21-025  Untrusted observation promoted to truth
```

All must fail closed.

---

# 16. Observability

Expose:

```text
model_calls_total
model_failures_total
model_latency_ms
model_tokens
model_cost_estimate
provider_fallback_count

vision_calls_total
vision_failures_total
generation_success_rate
artifact_validation_failures

mcp_calls_total
mcp_failures_total
mcp_denials_total
mcp_rate_limits
mcp_circuit_opens

benchmark_cases_total
benchmark_accuracy
benchmark_failure_rate
benchmark_ood_accuracy
benchmark_adversarial_accuracy

workforce_task_success_rate
revision_rate
human_approval_latency
creative_quality_score
```

Never expose or log:

```text
API keys
credentials
access tokens
private secrets
hidden chain-of-thought
```

---

# 17. Cost Governance

Track:

```text
cost per task
cost per staff role
cost per campaign
cost per generated asset
cost per successful deliverable
cost per revision
```

Use operational utility metrics such as:

$$
Utility =
\frac{Creative\ Quality \times Reliability}
{Cost \times Latency}
$$

This is an optimization metric, not a security policy.

---

# 18. Provenance & Data Governance

For external visual references record:

```text
source
collection timestamp
license/usage status where applicable
content hash
dataset version
annotation version
```

Do not silently add external images to training/fine-tuning datasets.

Training eligibility must be explicit.

---

# 19. Required Deliverables

Create/update:

```text
src/model_gateway/
src/visual_model_gateway/
src/mcp_gateway/
src/model_workforce/
src/visual_knowledge/
src/intelligence_evaluation/
```

Add:

```text
tests/phase21/
tests/model_gateway/
tests/visual_model_gateway/
tests/mcp_gateway/
tests/model_workforce/
tests/visual_knowledge/
tests/intelligence_evaluation/
```

Documentation:

```text
PHASE-21-ARCHITECTURE.md
PHASE-21-REAL-MODEL-INTEGRATION-REPORT.md
PHASE-21-VISUAL-INTELLIGENCE-BENCHMARK.md
PHASE-21-CAPABILITY-GAP-REPORT.md
PHASE-21-MCP-CONNECTIVITY-REPORT.md
PHASE-21-MODEL-ROUTING-REPORT.md
PHASE-21-REAL-WORKFLOW-REPORT.md
PHASE-21-SECURITY-REVIEW.md
PHASE-21-THREAT-MODEL.md
PHASE-21-TEST-REPORT.md
PHASE-21-COST-AND-PERFORMANCE-REPORT.md
PHASE-21-GOVERNANCE-GATE.md
```

---

# 20. Acceptance Criteria

## Real Models

- [ ] Primary real LLM provider works through `ModelGateway`.
- [ ] Independent fallback provider works.
- [ ] Structured output validated.
- [ ] Timeout/retry/fallback verified.
- [ ] Cost and latency measured.

## Visual Models

- [ ] Real vision provider integrated.
- [ ] Real image-generation provider integrated.
- [ ] Generated artifacts retain cryptographic lineage.
- [ ] Visual outputs evaluated against references.
- [ ] Failure modes recorded.

## MCP

- [ ] At least 2 real MCP servers integrated.
- [ ] At least 5 real tools exercised.
- [ ] Read-only workflow completed.
- [ ] Bounded drafting/transformation workflow completed.
- [ ] Mutation remains authorization-controlled.
- [ ] Failure and replay behavior verified.

## Visual Intelligence

- [ ] Versioned benchmark created.
- [ ] Minimum 250 cases retained or formally superseded.
- [ ] Adversarial cases included.
- [ ] OOD cases included.
- [ ] Expert-reviewed cases included.
- [ ] Human agreement measured.
- [ ] Capability profile produced.
- [ ] GAP-A through GAP-J distribution produced.

## Workforce

- [ ] Real model-backed staff roles execute.
- [ ] Role-to-model routing measured.
- [ ] Multi-model experiment evaluated.
- [ ] Critic/reviewer independence preserved.
- [ ] Model output cannot authorize execution.

## Security

- [ ] T/S21-001 through T/S21-025 pass.
- [ ] No credential leakage.
- [ ] Cross-client isolation verified.
- [ ] No execution-gate mutation.
- [ ] No security-policy mutation.
- [ ] No unauthorized MCP mutation.

## Regression

```text
Phase 1–20 baseline
+
Phase 21 additions
=
100% passing
0 regressions
0 unexplained skips
```

Do not delete or weaken old tests.

---

# 21. Evidence Rules

Every major claim must state its evidence class.

Example:

```text
Claim:
"Designer model understands typography hierarchy."

Evidence:
Benchmark: VQ-03
Version: v1.x
Cases: N
Accuracy: measured value
OOD: measured value
Expert agreement: measured value
Failure tags: GAP-x
```

If credentials/network access prevent real validation:

```text
BLOCKED — CREDENTIAL / NETWORK DEPENDENCY
```

Never fabricate:

- benchmark scores
- provider behavior
- latency
- cost
- MCP support
- expert agreement
- production readiness

---

# 22. Definition of "Training Required"

Phase 21 must answer:

> **What does ILYREN need to learn next?**

Produce:

### Already Strong
Capabilities exceeding defined thresholds.

### Weak / Unreliable
Capabilities with meaningful failure rates.

### Missing
Capabilities lacking sufficient evidence or model support.

Every weakness must map to:

```text
Prompt
Retrieval
Knowledge
Tool
Routing
Model Selection
Dataset
Fine-Tuning
Architecture
Fundamental Limitation
```

This becomes the evidence-backed roadmap for Phase 22+.

---

# 23. Recommended Execution Order

```text
1. Audit Phase 20 and freeze baseline
2. Connect primary real LLM
3. Connect real vision/image provider
4. Validate real-provider failure handling
5. Connect first read-only MCP server
6. Connect second MCP server
7. Exercise controlled real workflows
8. Freeze benchmark v1
9. Run visual intelligence evaluation
10. Perform failure analysis
11. Run capability-gap experiments
12. Evaluate model routing
13. Run real NOCAP benchmark
14. Run full security/threat suite
15. Run complete regression suite
16. Produce evidence reports
17. Governance review
```

---

# 24. Governance Gate

Phase 21 may only be marked `RATIFIED` when:

1. Real integrations are actually exercised.
2. Visual intelligence is empirically measured.
3. Capability gaps are documented.
4. Benchmark provenance is preserved.
5. Security boundaries remain intact.
6. Human authorization remains the sole execution authority.
7. Models are treated as untrusted outputs.
8. External observations are not automatically treated as truth.
9. Learning cannot mutate security policy.
10. Full regression passes.

Allowed verdicts:

```text
PASS — PRODUCTION INTEGRATION READY
PASS — CONTROLLED PILOT READY
CONDITIONAL PASS — EVIDENCE GAPS REMAIN
BLOCKED — EXTERNAL DEPENDENCY
FAIL — SECURITY BOUNDARY VIOLATION
FAIL — REGRESSION
```

Never select a stronger verdict than the evidence supports.

---

# 25. Mandatory Governance Statement

> **Phase 21 converts ILYREN's provider-neutral model, visual, and MCP architecture into empirically validated real-world integrations while establishing the actual boundary of its creative and visual intelligence. It does not grant models, MCP tools, workforce roles, evaluators, or optimization systems execution authority. Human authorization remains the sole source of execution authority; external observations and model outputs remain untrusted until evaluated; benchmark evidence remains versioned and provenance-aware; and all capability improvements remain subordinate to immutable security policy.**

$$
\boxed{
\mathbf{Real\ Models}
+
\mathbf{Real\ Tools}
+
\mathbf{Measured\ Visual\ Intelligence}
+
\mathbf{Evidence\ Based\ Learning}
+
\mathbf{Security\ Invariance}
}
$$

---

# 26. Final Engineer Instruction

Do not optimize for a green test suite alone.

The purpose of Phase 21 is to discover the truth about the system.

If the models perform poorly, record it.

If visual understanding is weak, record it.

If an MCP integration fails, record it.

If the benchmark exposes a fundamental limitation, record it.

If the architecture is insufficient, record it.

The most valuable outcome is not a high score.

It is a **reproducible map of what ILYREN can do, what it cannot do, why it fails, and what must be built next.**

That evidence becomes the engineering foundation for the next generation of the ILYREN Creative Workforce.
