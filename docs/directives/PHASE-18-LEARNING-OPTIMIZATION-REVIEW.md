# Phase 18 — Learning & Optimization Review

**Status:** RATIFIED & APPROVED  
**Target Substrate:** Phase 18 Continuous Optimizer & Strategy Promotion Controller  

---

## 1. Learning Progression Contract

$$\text{OBSERVED} \longrightarrow \text{ATTRIBUTED} \longrightarrow \text{EVALUATED} \longrightarrow \text{LEARNING\_SIGNAL} \longrightarrow \text{HYPOTHESIS} \longrightarrow \text{CANDIDATE\_STRATEGY} \longrightarrow \text{BENCHMARKED} \longrightarrow \text{ADOPTED / REJECTED}$$

No step in this progression can be skipped.

---

## 2. Strategy Promotion & Rejection Rules

- **Allowed Adaptation Scope:** Staff sequencing, research depth, critique ordering, revision allocation, format selection, scheduling heuristics.
- **Forbidden Scope:** Authorization requirements, role definitions, security policies, execution capabilities, human approval bypasses.
- **Rollback Guarantee:** If candidate performance delta is negative or errors increase, `OptimizationRejectedError` is raised, candidate state is set to `REJECTED`, and baseline configuration remains active.
