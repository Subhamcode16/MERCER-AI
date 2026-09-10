# HYPOTHESIS-LIFECYCLE-SPECIFICATION.md
## Phase 29 Architecture Specification: Hypothesis Lifecycle Engine

---

### 1. Overview

Strategic hypotheses are testable, falsifiable propositions that connect emerging signals to controlled marketing actions.

Under the invariant:
$$\mathbf{Model\ Confidence \neq Empirical\ Confidence}$$

---

### 2. Hypothesis Lifecycle State Machine

```
   [ PROPOSED ] ──> [ UNDER_REVIEW ] ──> [ TESTABLE ] ──> [ TESTING ]
         │                                                    │
         v                                                    v
    [ REJECTED ]                                      [ SUPPORTED ]
         ^                                                    │
         │                                                    v
         └── [ CONTRADICTED ] <── [ WEAKENED ] <─────── [ UNKNOWN ]
```

---

### 3. Falsification & Bounding Rules

1. **Mandatory Falsification Criteria:** A hypothesis without an explicit empirical failure condition is rejected.
2. **Controlled Experiment Requirement:** A hypothesis cannot transition from `TESTING` to `SUPPORTED` without empirical experiment references (`EXP-...`).
3. **Model Overconfidence Penalty:** High model-predicted confidence alone cannot promote a hypothesis; unsupported claims revert to `UNKNOWN`.
