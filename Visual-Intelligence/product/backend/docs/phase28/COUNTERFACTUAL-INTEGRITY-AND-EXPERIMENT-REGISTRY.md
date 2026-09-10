# Phase 28: Counterfactual Integrity & Experiment Registry

## 1. Counterfactual Integrity
Unobserved alternative paths are modeled explicitly as `COUNTERFACTUAL_UNKNOWN`. The system strictly forbids fabricating counterfactual outcomes based purely on regression heuristics or model hallucinations.

## 2. Controlled Experiment Registry
Experiments follow an explicit governed lifecycle:
`HYPOTHESIS` $\rightarrow$ `DESIGN` $\rightarrow$ `REVIEW` $\rightarrow$ `APPROVAL` $\rightarrow$ `RUN` $\rightarrow$ `COLLECT` $\rightarrow$ `ANALYZE` $\rightarrow$ `PROMOTE / REJECT / RETAIN`.

Experiments test hypotheses with statistical significance ($p < 0.05$) while remaining completely isolated from autonomous execution privileges.
