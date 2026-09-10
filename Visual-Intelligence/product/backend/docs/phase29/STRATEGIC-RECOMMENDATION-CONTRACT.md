# STRATEGIC-RECOMMENDATION-CONTRACT.md
## Phase 29 Architecture Specification: Strategic Recommendation Contract & Quality Engine

---

### 1. Overview

Strategic recommendations are decision-ready proposals presented to human decision-makers. They are strictly informational and hold zero autonomous execution authority.

Under the invariants:
$$\mathbf{Recommendation \neq Truth} \quad \mathbf{Recommendation \neq Execution\ Permission}$$

---

### 2. 12-Stage Recommendation Anatomy

```
1. TITLE & ACTION STATEMENT
2. WHY NOW (Urgency & Catalysts)
3. SUPPORTING EVIDENCE
4. CONTRADICTING EVIDENCE (Counter-theses)
5. ASSUMPTIONS
6. UNKNOWNS (Preserved unobserved states)
7. ALTERNATIVES (Including status quo)
8. EXPECTED CONSEQUENCES
9. REVERSIBILITY RATING (Highly / Moderately / Irreversible)
10. PROPOSED EXPERIMENT (Bounded validation trial)
11. REQUIRED HUMAN AUTHORITY ROLE
12. EXPIRATION & INVALIDATION CONDITIONS
```

---

### 3. Recommendation Quality Contract & Automatic Downgrading

The `RecommendationQualityContract` enforces automatic confidence penalties:
- **No Supporting Evidence:** Downgrades confidence to $\le 0.20$ and sets status to `INSUFFICIENT_EVIDENCE`.
- **High Contradiction Ratio:** If contradicting evidence $\ge$ supporting evidence, confidence is damped by $40\%$ and status transitions to `DOWNGRADED`.
- **Observational Correlation Cap:** Confidence cannot exceed $0.70$ on observational correlations without controlled experiments.
- **Assumptions Exceeding Evidence:** Damps confidence by $15\%$.
