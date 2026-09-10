# Phase 8 Agentic Threat Model: Agentic Work Layer & Governance Isolation

**Document Status:** RATIFIED THREAT MODEL  
**Phase:** 8 (Agentic Work Orchestration & Real Workflow Boundary)  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`, `PHASE-8-AGENTIC-WORK-ORCHESTRATION-DIRECTIVE.md`

---

## 1. System Boundary & Assets

### System Assets
1. **AI Staff Profiles & Capabilities:** Configured worker profiles for 7 composable roles.
2. **Task Graph DAG:** Dependency structures, status state machines, and revision iteration counters.
3. **Work Packages:** Generated visual, brand, strategy, and content artifacts.
4. **Learning Signals & Adaptive Changes:** Versioned, auditable, and reversible configuration updates.
5. **Visual Trend Observations:** Provenance-tracked external aesthetic intake.

### System Boundaries
- **In-Scope:** Orchestration, staff delegation, task graph DAG, context scoping, self-critique, independent review, feedback signals, adaptive learning, threat matrix testing (T8-1 – T8-12).
- **Out-of-Scope:** Security substrate modification, epistemic state mutation, execution gate unlocking, production cryptographic key generation.

---

## 2. Formal Invariants (INV-8.1 – INV-8.8)

### INV-8.1 Intelligence Does Not Equal Authority
```text
Staff Reasoning / Generated Output != Execution Authorization
```

### INV-8.2 Orchestrator Does Not Become Security Root
```text
WorkOrchestrator cannot unlock ExecutionGate or modify EpistemicState
```

### INV-8.3 Staff Are Workers, Not Security Principals
```text
Staff Role != Security Principal
```

### INV-8.4 Self-Critique Is Not Self-Authorization
```text
Critic PASS / Reviewer Approval != Execution Permission
```

### INV-8.5 Learning Is Not Security-Policy Mutation
```text
Learning Output -> Prompts / Routing ONLY (Security Policy Immutable)
```

### INV-8.6 External Knowledge Is Evidence
```text
External Observation -> UNTRUSTED_EXTERNAL_OBSERVATION
```

### INV-8.7 Improvement Must Be Reversible
```text
AdaptiveChange -> Versioned, Attributable, Reversible
```

### INV-8.8 Real Work Must Be Observable
```text
Workflow Run -> Inspectable Plan, Tasks, Revisions, Critiques, Feedback
```

---

## 3. Threat Matrix & Countermeasure Verification

All 12 threat scenarios (T8-1 through T8-12) were verified via automated unit and integration tests in `tests/agentic_work/test_security_boundary.py`, achieving a 100% pass rate.
