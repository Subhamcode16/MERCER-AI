# PHASE 20 — ILYREN Model Integration, MCP Connectivity & Visual Intelligence Benchmark Boundary

**Status:** ENGINEERING DIRECTIVE — NOT YET IMPLEMENTED  
**Predecessor:** Phase 19 — Creative Intelligence Network & Institutional Intelligence Boundary  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`

## 1. Objective

Phase 20 turns the governed ILYREN control plane into a **real model-backed creative workforce** and empirically measures its visual intelligence.

The engineer must implement and validate four capabilities:

1. Real LLM integration behind a provider-neutral model gateway.
2. Real image-generation and/or vision-model integration behind a visual model gateway.
3. Controlled external MCP connectivity behind an explicit capability and credential boundary.
4. A rigorous visual-knowledge benchmark that determines what ILYREN can recognize, reason about, generate, critique, generalize, and where it fails.

**Do not begin by fine-tuning. Measure the baseline first.**

## 2. Immutable Governance Invariants

The following remain non-negotiable:

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$

$$\mathbf{Learning \neq Security\ Policy\ Mutation}$$

$$\mathbf{External\ Observation \neq Trusted\ Fact}$$

$$\mathbf{Self\!\!-\!Improvement \neq Self\!\!-\!Authorization}$$

$$\mathbf{Creative\ Review \neq Execution\ Authorization}$$

$$\mathbf{External\ Tool\ Access \neq Blanket\ Provider\ Access}$$

$$\mathbf{Model\ Output \neq Truth \neq Permission}$$

Phase 20 MUST NOT give a model, MCP server, reviewer, learning loop, or optimizer execution authorization or the ability to mutate immutable security policy. Human authorization from Phase 10 remains the sole source of execution authority.

## 3. Required Packages

Create:

```text
src/model_gateway/
src/visual_model_gateway/
src/mcp_gateway/
src/intelligence_evaluation/
src/visual_knowledge/
```

These are integration/control boundaries, not vendor-specific application code.

## 4. LLM Model Gateway

Implement:

```text
src/model_gateway/
  exceptions.py
  models.py
  provider.py
  provider_registry.py
  model_policy.py
  request_builder.py
  response_normalizer.py
  structured_output.py
  token_budget.py
  timeout_policy.py
  retry_policy.py
  routing.py
  fallback.py
  redaction.py
  model_ledger.py
  gateway.py
```

The workforce must call:

```text
TASK TYPE
→ REQUIRED CAPABILITY
→ MODEL POLICY
→ APPROVED MODEL ADAPTER
```

Never:

```text
STAFF → arbitrary vendor SDK
```

Model metadata must include provider, model/version, capabilities, context limit, structured-output support, vision/tool support where applicable, latency/cost/reliability class.

Every response must retain provenance:

```text
provider
model
model_version
request_id
timestamp
policy_version
context_scope
source_references
structured_output_validated
```

Classify outputs as model-generated observations/hypotheses/recommendations—not trusted facts or permissions.

## 5. Visual Model Gateway

Implement:

```text
src/visual_model_gateway/
  exceptions.py
  models.py
  provider.py
  provider_registry.py
  generation_policy.py
  prompt_builder.py
  image_request.py
  image_response.py
  vision_analysis.py
  artifact_validation.py
  visual_lineage.py
  visual_ledger.py
  gateway.py
```

Support:

### Visual generation

```text
Creative Direction
→ generation request
→ image model
→ artifact validation
→ self-critique
→ independent review
→ revision
```

### Visual analysis

```text
Image/reference
→ vision model
→ structured observations
→ Visual DNA
→ evaluation/knowledge boundary
```

Every generated artifact must retain lineage including artifact ID, parent artifact, model/version, request hash, creative-direction hash, Visual DNA reference, timestamp, and validation status.

## 6. MCP Gateway

Implement:

```text
src/mcp_gateway/
  exceptions.py
  models.py
  server_registry.py
  tool_registry.py
  capability_policy.py
  schema_validator.py
  request_guard.py
  result_sanitizer.py
  credential_boundary.py
  rate_limit.py
  circuit_breaker.py
  idempotency.py
  environment_guard.py
  mcp_ledger.py
  gateway.py
```

MCP is an **external capability transport**, never an authority layer.

Every server/tool requires:

```text
server_id
provider
environment
declared_capabilities
approved_capabilities
risk_class
credential_requirements
data_scopes
rate_limits
timeout
approval_requirements
```

Reject wildcard capabilities such as `*`, `admin`, or `full_access`.

Tool calling must be:

```text
LLM proposed tool intent
→ Tool Policy Validator
→ Capability Mapping
→ Context Guard
→ Authorization requirement check
→ Tool invocation
→ Result sanitization
→ Provenance/trust classification
→ Return structured result
```

Credentials must never enter model prompts, model context, MCP result payloads, client DTOs, or ordinary audit logs.

External results remain untrusted until evaluated.

## 7. Workforce Integration

At minimum, connect real model-backed intelligence to:

```text
TREND_ANALYST
  → LLM + approved research/MCP + visual analysis

STRATEGIST
  → LLM + institutional intelligence

DESIGNER
  → visual model + Visual DNA + Creative Direction

CONTENT_SPECIALIST
  → LLM + brand context

CRITIC
  → vision model + structured critique

REVIEWER
  → independent evaluation configuration
```

The model is the intelligence substrate; the existing workforce remains the organizational control layer.

## 8. Visual Knowledge Baseline

Before any training/fine-tuning, build a benchmark of at least **250 visual evaluation cases**, preferably 500+, with provenance and validated annotations.

Recommended categories:

```text
brand identity
typography
color
layout
grid
composition
photography
fashion
art direction
social content
campaign systems
trend recognition
Visual DNA
brand consistency
revision critique
cross-style generalization
ambiguous cases
adversarial cases
```

Each case should include:

```text
case_id
reference/image
category
question
expected observation
acceptable variations
ground-truth source
difficulty
confidence requirement
client scope
provenance
```

## 9. Mandatory Visual Benchmark Tasks

### VQ-01 Visual Description
Measure correspondence between image and structured description.

### VQ-02 Visual DNA Extraction
Measure palette, typography, composition, grid, spacing, imagery, personality, and related fields.

### VQ-03 Comparative Analysis
Given two references, identify structural similarities/differences rather than superficial resemblance.

### VQ-04 Brand Consistency
Given brand DNA + candidate artifact, produce alignment, violations, evidence, and revision recommendations.

### VQ-05 Trend Recognition
Identify trend observations with confidence, evidence, time context, and uncertainty. Keep observations untrusted until evaluated.

### VQ-06 Creative Direction Synthesis
Convert brand DNA + campaign objective + audience + constraints + trend observations into an inspectable CreativeDirectionBrief.

### VQ-07 Critique
Detect defects, severity, evidence, and revision actions.

### VQ-08 Revision Recovery
Determine whether a revision actually solved the defects identified by critique.

### VQ-09 Cross-Client Generalization
Measure abstract pattern transfer without client-data transfer.

### VQ-10 Adversarial Cases
Include misleading layouts, near-identical palettes, trend lookalikes, ambiguous composition, low-quality images, conflicting metadata, and prompt injection embedded in images.

## 10. Metrics

Measure individually:

```text
Visual Observation Accuracy
Visual DNA Accuracy
Brand Alignment Accuracy
Trend Classification Accuracy
Critique Precision
Critique Recall
Revision Success Rate
Creative Direction Utility
Cross-Client Generalization
Hallucination Rate
Unsupported Claim Rate
Uncertainty Calibration
Latency
Cost
Reliability
```

Do not hide a critical failure behind an aggregate average. Critical metric failure must fail the relevant benchmark gate.

## 11. Failure Taxonomy

Every meaningful failure must be classified:

```text
GAP-A Missing knowledge
GAP-B Retrieval failure
GAP-C Reasoning failure
GAP-D Vision/perception failure
GAP-E Context failure
GAP-F Instruction-following failure
GAP-G Evaluation/calibration failure
GAP-H Data/provenance problem
GAP-I Model capability limitation
GAP-J Workflow/orchestration failure
```

This classification is mandatory before deciding to train anything.

## 12. Training vs Retrieval vs Evaluation

Use retrieval when knowledge is external, current, and provenance-sensitive.

Use structured knowledge for stable deterministic information.

Use prompt/instruction improvements for output-structure and task-decomposition problems.

Use critique/review/evaluation loops when errors are detectable and correctable without changing model weights.

Consider fine-tuning only when:

- the capability is repeatedly required;
- high-quality examples exist;
- the task is sufficiently stable;
- retrieval/instruction/evaluation are insufficient;
- measurable improvement can be demonstrated;
- regression testing exists.

A benchmark failure is **not automatically a training problem**.

## 13. Real Workflow Benchmark

Create:

```text
tests/phase20/
  test_model_gateway.py
  test_visual_model_gateway.py
  test_mcp_gateway.py
  test_visual_knowledge_benchmark.py
  test_workforce_model_integration.py
  test_phase20_security_boundary.py
  test_phase20_real_workflow.py
  test_phase20_regression.py
```

Mandatory benchmark:

**ILYREN NOCAP Campaign — Model-Backed Production Cycle**

Run:

```text
client objective
→ context
→ mission
→ workforce decomposition
→ trend research
→ visual analysis
→ creative direction
→ asset generation
→ copy generation
→ self-critique
→ revision
→ independent review
→ human authorization
→ sandbox execution
→ outcome observation
→ learning signal
→ strategy experiment
→ benchmark
→ adoption/rejection
→ ledger verification
```

Use real providers where credentials/access exist.

If a provider is unavailable:

```text
STATUS = BLOCKED / NOT VERIFIED
```

Never convert unavailable provider stages into fake passes.

## 14. Security Threat Matrix

At minimum test:

```text
T20-1  Model self-authorization attempt
T20-2  Model policy mutation attempt
T20-3  External prompt injection
T20-4  Image-embedded prompt injection
T20-5  MCP wildcard capability
T20-6  Unauthorized MCP server
T20-7  Cross-client MCP access
T20-8  Credential leakage to model
T20-9  Credential leakage to logs
T20-10 Tool result treated as truth
T20-11 Unauthorized provider capability selection
T20-12 External mutation replay
T20-13 Unapproved provider/model substitution
T20-14 Artifact lineage forgery
T20-15 Benchmark contamination
T20-16 Client data entering institutional benchmark
T20-17 Confidential client data used for fine-tuning
T20-18 Feedback mutating security policy
T20-19 Generator/reviewer correlated failure
T20-20 Model-generated execution bypass
T20-21 MCP timeout/retry duplicate mutation
T20-22 Malicious provider payload
T20-23 Hallucinated trend treated as fact
T20-24 Benchmark score manipulation
T20-25 Self-improvement bypassing benchmark
```

All must fail closed.

## 15. Acceptance Criteria

### Model
- [ ] At least one real LLM provider connected.
- [ ] Provider SDK isolated behind adapter.
- [ ] Structured outputs validated.
- [ ] Timeouts/retries bounded.
- [ ] Provenance recorded.
- [ ] No execution authority exposed.

### Visual
- [ ] At least one real image-generation and/or vision provider connected.
- [ ] Artifact lineage works.
- [ ] Vision observations are structured/provenance-aware.
- [ ] Visual outputs enter critique/review.

### MCP
- [ ] At least one real MCP-compatible integration OR explicitly documented provider-unavailable blocker.
- [ ] Capability allowlisting.
- [ ] Credential boundary.
- [ ] Result sanitization.
- [ ] Environment separation.
- [ ] Replay/idempotency controls.

### Visual knowledge
- [ ] Baseline benchmark.
- [ ] ≥250 cases, or justified pilot size.
- [ ] Category metrics.
- [ ] Failure taxonomy.
- [ ] Quantified knowledge gaps.
- [ ] Training/retrieval/evaluation decisions.
- [ ] No unsupported claim of training.

### Workforce
- [ ] ≥3 real model-backed staff roles.
- [ ] Self-critique.
- [ ] Independent review.
- [ ] Revision loop.
- [ ] Human authorization for side effects.

### End-to-end
- [ ] Real model-backed NOCAP workflow.
- [ ] Sandbox execution.
- [ ] Outcome loop.
- [ ] Learning experiment.
- [ ] Rollback.
- [ ] Ledger integrity.

## 16. Required Documentation

Create:

```text
PHASE-20-ARCHITECTURE.md
PHASE-20-MODEL-CAPABILITY-REPORT.md
PHASE-20-VISUAL-KNOWLEDGE-BENCHMARK.md
PHASE-20-MCP-INTEGRATION-REPORT.md
PHASE-20-REAL-WORKFLOW-REPORT.md
PHASE-20-SECURITY-REVIEW.md
PHASE-20-THREAT-MODEL.md
PHASE-20-TEST-REPORT.md
PHASE-20-GOVERNANCE-GATE.md
```

Maintain the existing engineering log discipline:

```text
INTENT
→ DESIGN
→ IMPLEMENTATION
→ FAILURE
→ ROOT CAUSE
→ FIX
→ VERIFICATION
→ SECURITY IMPLICATION
→ LESSON
```

Do not fabricate tests, benchmark scores, provider access, model capability, training improvements, or production readiness.

## 17. Definition of Learning

Distinguish:

```text
Observed
→ Stored
→ Retrieved
→ Used
→ Evaluated
→ Generalized
→ Experimentally validated
→ Adopted
```

Memory storage or a vector database alone is not evidence of learning.

Successful generation is not evidence of understanding.

Benchmark score is not truth.

## 18. Phase 20 Governance Gate

The final gate must answer:

**G1 Integration:** Can ILYREN use real models?

**G2 Intelligence:** Does model-backed ILYREN materially outperform its pre-model baseline?

**G3 Visual Knowledge:** What visual capabilities and gaps are quantitatively demonstrated?

**G4 Connectivity:** Can ILYREN safely use external MCP/tool capabilities?

**G5 Autonomy:** Can ILYREN continuously perform bounded creative work while human control over side effects remains intact?

Allowed verdicts:

```text
PASS
PASS WITH LIMITATIONS
BLOCKED
FAIL
```

A high test count cannot override a failed governance invariant.

## 19. Target Architecture

```text
HUMAN / CLIENT
      ↓
CLIENT COMMAND CENTER
      ↓
STUDIO OPERATIONS
      ↓
PRODUCTION FABRIC
      ↓
CREATIVE WORKFORCE
      ↓
┌──────────────┬────────────────┬──────────────┐
│ LLM Gateway  │ Visual Gateway │ MCP Gateway  │
└──────────────┴────────────────┴──────────────┘
      ↓
INTELLIGENCE EVALUATION
      ↓
VISUAL KNOWLEDGE
      ↓
LEARNING / EXPERIMENTS
      ↓
INSTITUTIONAL MEMORY
      ↓
AUTHORIZATION / SECURITY / EXECUTION
```

The Phase 20 objective is:

$$\boxed{\mathbf{ILYREN\ becomes\ more\ capable\ without\ becoming\ more\ authoritative}}$$

and:

$$\boxed{\mathbf{Measure\ intelligence\ before\ attempting\ to\ train\ it}}$$

Phase 20 is complete only when the evidence demonstrates what the model-backed creative workforce can actually do.
