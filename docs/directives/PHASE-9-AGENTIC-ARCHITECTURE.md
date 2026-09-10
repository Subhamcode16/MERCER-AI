# Phase 9 Agentic Architecture Specification: Persistent Learning, Knowledge & Workflow Optimization Boundary

**Document Status:** RATIFIED ARCHITECTURE SPECIFICATION  
**Phase:** 9 (Persistent Learning, Knowledge & Workflow Optimization Boundary)  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`, Phase 8 Agentic Work Governance  
**Prerequisites:** Phase 1–8 COMPLETE & RATIFIED (247/247 Pytests PASSED)

---

## 1. Executive Summary & Epistemic Boundary

Phase 9 converts the Phase 8 bounded agentic work layer into a **persistent, measurable, versioned learning and workflow-optimization boundary**.

It allows the system to remember prior workflow outcomes, retain structured feedback, ingest external visual/design/trend observations as untrusted knowledge, track complete machine-verifiable artifact lineage, compare new strategy configurations against historical benchmarks, execute reversible self-improvements, and roll back failing adaptations.

### Non-Negotiable Core Equations

$$
\mathbf{Learning \neq Authorization} \quad \text{and} \quad \mathbf{Knowledge \neq Truth}
$$

$$
\mathbf{Optimization \neq Security\ Policy\ Mutation} \quad \text{and} \quad \mathbf{Self\!-!Improvement \neq Execution\ Authority}
$$

$$
\mathbf{External\ Observation \neq Trusted\ Fact} \quad \text{and} \quad \mathbf{User\ Feedback \neq Automatic\ Policy\ Override}
$$

---

## 2. Layer Architecture

```text
USER / WORKFLOW REQUEST
          |
          v
PHASE 8 WORK ORCHESTRATOR
Staff • Task Graph • Critique • Review • Workflow
          |
          v
PHASE 9 LEARNING BOUNDARY
Workflow Memory -> Feedback Engine -> Benchmark Suite -> Persistent Improvement Engine
       ^                ^                    |                    |
Knowledge Store -> Artifact Lineage -> Strategy Store -> Rollback Controller
          |
          v
PHASE 1–7 SECURITY SUBSTRATE
Evidence • Decision • Attestation • Audit • Recovery
Epistemic State • Execution Gate (LOCKED = False)
```

---

## 3. Core Modules & Component Specifications

### 3.1 Workflow Memory Store (`src/agentic_work/memory_store.py`)
- Provides controlled file-backed storage (`data/phase9_memory/`) for `WorkflowMemoryRecord` objects.
- Uses atomic write semantics (`tempfile` + `os.replace`) to prevent partial writes.
- Enforces SHA-256 record hash verification on load to detect file tampering.
- Raises `SecretStorageForbiddenError` if any raw credentials, secrets, or private keys are detected.

### 3.2 Persistent Feedback Engine (`src/agentic_work/persistent_feedback.py`)
- Records structured user and critic feedback into `data/phase9_feedback/`.
- Implements feedback replay defense (`DuplicateFeedbackError`) tracking feedback IDs.
- Aggregates learning patterns ONLY when $N \ge 3$ consistent feedback signals or recurring defects occur.

### 3.3 Persistent Knowledge Store (`src/agentic_work/persistent_knowledge.py`)
- Stores external visual trend observations in `data/phase9_knowledge/`.
- Forcing status to `UNTRUSTED_EXTERNAL_OBSERVATION` to prevent privilege escalation.
- Sanitizes input content to strip prompt injection tags (`<SYSTEM_MESSAGE>`, `IGNORE ALL PREVIOUS INSTRUCTIONS`), treating external text strictly as passive data.

### 3.4 Artifact Lineage Tracker (`src/agentic_work/artifact_lineage.py`)
- Tracks machine-verifiable ancestry in `data/phase9_lineage/`.
- Links artifact output to Workflow ID, Task Graph Version, Staff Role Contributions, Observation IDs, Critique Scores, and Strategy Version ID.
- Computes SHA-256 lineage payload hash; raises `LineageTamperError` on mismatch.

### 3.5 Adaptive Strategy & Allowlist Engine (`src/agentic_work/adaptive_strategy.py`)
- Manages versioned strategy configurations in `data/phase9_strategies/`.
- Enforces explicit **Operational & Tactical Allowlist**:
  - `staff_ordering`
  - `task_graph_depth`
  - `critique_weights`
  - `context_limits`
  - `research_depth`
  - `versioned_role_prompts`
  - `revision_iteration_cap`
  - `benchmark_selection_weights`
- Raises `SecurityBoundaryViolation` if any forbidden security field (`execution_gate`, `epistemic_state`, `audit_integrity`, `recovery_manager`) is targeted.

### 3.6 5-Category Benchmark Suite (`src/agentic_work/benchmark_suite.py`)
- Quantitative evaluation runner covering:
  1. Visual Identity Research
  2. Brand Campaign Strategy
  3. Visual Design Direction
  4. Social Content System
  5. Revision Recovery

### 3.7 Persistent Improvement Engine (`src/agentic_work/persistent_improvement.py`)
- Governs candidate lifecycle: `CANDIDATE` -> `OFFLINE_EVALUATION` -> `BENCHMARK_COMPARISON` -> `APPROVED` -> `ACTIVE` -> `ROLLBACK`.
- Raises `DegradationRejectedError` if a candidate scores lower than the active strategy.
- Implements `rollback_active_strategy()`, reverting to the parent version cleanly.

### 3.8 Security Substrate Barrier (`src/agentic_work/learning_governance.py`)
- Audits operations to `AuditStore` and asserts `ExecutionGate.is_permitted()` is `False` at all times.
