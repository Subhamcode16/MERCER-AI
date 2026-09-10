# PHASE 28 — ILYREN CREATIVE INTELLIGENCE OPERATING LOOP
## Campaign-to-Outcome Learning, Calibration & Governed Optimization

**Document Type:** Engineering Directive  
**Program:** ILYREN Creative Intelligence Platform / Creative Operating System  
**Phase:** 28  
**Predecessor:** Phase 27 — ILYREN Creative Campaign Studio  
**Status:** READY FOR IMPLEMENTATION

---

# 1. Executive Directive

Phase 28 shall establish the **ILYREN Creative Intelligence Operating Loop**.

Phase 27 completed the campaign-centered product surface. ILYREN can now move from product understanding through discovery, creative intelligence, direction, visual development, review, approval, production, launch, and outcomes.

The next requirement is to make completed campaigns continuously improve the intelligence system **without allowing learning to mutate authority**.

Canonical loop:

```text
CAMPAIGN
   ↓
DECISION
   ↓
CREATIVE OUTPUT
   ↓
PRODUCTION
   ↓
LAUNCH
   ↓
OBSERVED OUTCOME
   ↓
EVALUATION
   ↓
LEARNING SIGNAL
   ↓
CALIBRATION
   ↓
GOVERNED KNOWLEDGE UPDATE
   ↓
FUTURE CREATIVE DECISION
```

The objective is not a generic analytics layer. It is the governed bridge between **what ILYREN believed, what it recommended, what was created, what happened, and what can legitimately be learned**.

---

# 2. Critical Review of Phase 27

The supplied Phase 27 walkthrough reports:

```text
50 / 50 Phase 27 tests
351 / 351 cross-phase tests
25 / 25 security scenarios
5 / 5 integration workflows
3 / 3 adversarial/usability tests
1 / 1 canonical 21-step benchmark
```

These results provide strong implementation evidence for the reported test corpus. They do not establish universal product correctness, causal validity, or real-world generalization.

Phase 28 must therefore make **learning evidence explicit**.

In particular:

- outcome correlation must not become causal truth;
- successful campaigns must not automatically validate every preceding decision;
- failed campaigns must not automatically invalidate every preceding decision;
- model confidence must not be treated as empirical confidence;
- postmortem conclusions must remain distinguishable from observed outcomes;
- learning promotion must require provenance and governance;
- optimization must not modify security policy;
- optimization must not silently expand worker authority;
- historical campaign context must remain immutable.

---

# 3. Why Phase 28 Exists

Phases 18–19 established studio intelligence and institutional intelligence. Phase 27 established the complete campaign product surface.

Phase 28 closes the operational learning loop at the **product decision level**.

The system must be able to answer:

```text
What did we believe?
Why did we believe it?
What did we do?
What actually happened?
What evidence supports the outcome?
What remains uncertain?
What should change next time?
How confident are we in that change?
```

---

# 4. Core Invariants

```text
Outcome ≠ Causation
Correlation ≠ Causal Proof
Learning ≠ Policy Mutation
Learning ≠ Authority
Performance ≠ Truth
Failure ≠ Universal Invalidity
Evidence ≠ Interpretation
Historical Record ≠ Current Recommendation
Optimization ≠ Self-Authorization
Model Confidence ≠ Empirical Confidence
Institutional Learning ≠ Cross-Client Leakage
Unknown Must Survive
```

These are mandatory architecture invariants, not documentation slogans.

---

# 5. Scope

Phase 28 includes:

1. Decision ledger.
2. Outcome evidence ingestion.
3. Campaign outcome normalization.
4. Creative-performance linkage.
5. Attribution confidence.
6. Learning-signal generation.
7. Hypothesis generation.
8. Counterfactual representation.
9. Experiment registry.
10. Calibration tracking.
11. Knowledge promotion proposals.
12. Learning review.
13. Institutional learning integration.
14. Skill improvement proposals.
15. Worker performance learning.
16. Creative pattern discovery.
17. Regression protection.
18. Learning provenance.
19. Learning observability.
20. Product-facing learning surfaces.
21. Adversarial validation.
22. Cross-phase compatibility.

---

# 6. Explicit Non-Scope

Do not introduce:

- autonomous causal inference presented as fact;
- automatic policy mutation;
- automatic privilege expansion;
- automatic worker promotion to higher authority;
- automatic deletion of contradictory evidence;
- automatic conversion of correlation into causal knowledge;
- hidden learning from private client data;
- irreversible knowledge promotion;
- silent replacement of historical campaign records;
- optimizer-controlled security configuration;
- model-generated evidence without provenance;
- self-modifying production execution logic.

---

# 7. Decision Ledger

Every material campaign decision should be recordable as:

```text
decision_id
campaign_id
decision_type
decision_version
actor
worker_id
timestamp
context_snapshot
decision
rationale
evidence_refs
alternatives
confidence
assumptions
unknowns
result
status
```

Examples include:

```text
audience_selection
creative_territory
visual_direction
channel_selection
copy_direction
asset_variant
launch_timing
```

Once a decision participates in production or launch, its historical record must be immutable. Corrections create explicit corrective records rather than overwriting history.

---

# 8. Outcome Evidence Model

Observed outcome data must remain separated into:

```text
OBSERVATION
MEASUREMENT
ATTRIBUTION
INTERPRETATION
HYPOTHESIS
```

Example:

```text
Observation:
CTR increased 14%.

Measurement:
CTR = 2.31%.

Attribution:
Variant B received the highest attributed conversions.

Interpretation:
Variant B may have improved message resonance.

Hypothesis:
The visual hierarchy contributed to the improvement.

Causal status:
UNPROVEN
```

---

# 9. Outcome Normalization and Linkage

External metrics may differ in definitions, windows, attribution models, sampling, latency, identity resolution, currency, and channel semantics.

Normalize them without erasing source meaning. Every normalized metric must retain:

```text
source
source_metric
normalization_rule
time_window
attribution_model
confidence
```

Link outcomes to exact:

```text
campaign
direction
asset
variant
channel
audience
experiment
production_version
launch_version
```

If an asset changes after launch, the outcome must remain associated with the actual launched version.

---

# 10. Learning Signals and Hypotheses

Use explicit signals:

```text
POSITIVE_SIGNAL
NEGATIVE_SIGNAL
MIXED_SIGNAL
NO_SIGNAL
INSUFFICIENT_EVIDENCE
CONTRADICTORY_SIGNAL
```

A learning hypothesis must contain:

```text
hypothesis_id
statement
originating_campaigns
supporting_evidence
contradicting_evidence
scope
confidence
known_limitations
test_recommendation
status
```

A hypothesis is not a universal rule.

---

# 11. Counterfactual Integrity

Where causal claims are considered, represent the missing counterfactual explicitly.

```text
Observed:
Variant A performance

Unobserved:
Performance if the same audience had received Variant B
```

Never fabricate counterfactual outcomes. Without controlled evidence:

```text
COUNTERFACTUAL_UNKNOWN
```

---

# 12. Experiment Registry

Introduce a governed experiment registry with:

```text
experiment_id
campaign_id
hypothesis_id
variants
population
allocation
success_metrics
guardrail_metrics
duration
status
result
analysis
limitations
owner
```

Lifecycle:

```text
HYPOTHESIS
   ↓
DESIGN
   ↓
REVIEW
   ↓
APPROVAL
   ↓
RUN
   ↓
COLLECT
   ↓
ANALYZE
   ↓
INTERPRET
   ↓
PROMOTE / REJECT / RETAIN
```

Experiments never independently authorize consequential external actions.

---

# 13. Calibration

Track calibration between predicted confidence and observed evidence for:

```text
creative recommendation confidence
visual-quality confidence
audience-fit confidence
performance expectation confidence
```

Suggested buckets:

```text
0.00–0.20
0.20–0.40
0.40–0.60
0.60–0.80
0.80–1.00
```

Track prediction count, success rate, calibration error, sample size, and uncertainty where appropriate. Do not infer strong calibration from tiny samples.

---

# 14. Learning Promotion

Learning progresses through:

```text
OBSERVED
   ↓
PROVISIONAL
   ↓
REVIEWED
   ↓
VALIDATED
   ↓
PROMOTED
   ↓
RETIRED
```

Promotion depends on evidence quality, replication, scope, contradiction, sample size, experiment quality, freshness, and domain relevance.

Every promotion proposal must contain:

```text
claim
scope
supporting evidence
contradicting evidence
confidence
affected knowledge objects
expected benefit
known risks
rollback plan
review status
```

---

# 15. Contradiction and Scope Handling

If new evidence conflicts with institutional knowledge:

```text
Existing Claim
      +
New Evidence
      ↓
Conflict Record
      ↓
Evaluation
      ↓
Retain / Revise / Retire
```

Preserve contradiction history.

Every discovered pattern must declare scope:

```text
GLOBAL
DOMAIN
CLIENT
BRAND
CAMPAIGN
```

Private client data must not become global knowledge without governed abstraction and validation.

---

# 16. Skill, Worker and Visual Learning

Campaign outcomes may produce proposals for:

- skill improvement;
- worker specialization;
- work allocation;
- training examples;
- review requirements;
- visual knowledge refinement.

All changes require explicit versioning/evaluation where they affect governed artifacts.

Performance learning must never silently modify:

```text
permissions
tenant scope
approval authority
security policy
credential access
```

Visual learning may identify patterns in composition, color, typography, layout, framing, format, channel adaptation, and brand consistency, but visual similarity must not automatically become strategic correctness.

---

# 17. Freshness and Drift

Learning objects require:

```text
created_at
last_validated_at
last_observed_at
expiry_policy
status
```

Track whether changes in:

```text
model
provider
prompt/compiler
skill version
Visual DNA version
retrieval configuration
```

may have affected outcomes.

Also record relevant confounders where available:

```text
budget
audience change
channel mix
seasonality
pricing
promotion
inventory
competitor activity
model/provider changes
creative format
launch timing
```

The purpose is to avoid unjustified conclusions, not to claim perfect causal inference.

---

# 18. Product Learning Surface

Users should be able to inspect:

```text
What we learned
Why we think we learned it
Evidence
Confidence
What contradicted it
Where it applies
Where it does not apply
Recommended next experiment
```

When future recommendations use learned knowledge, expose the knowledge source, applicability, confidence, and unknowns.

---

# 19. Learning Rollback

Promoted knowledge must support:

```text
rollback
retirement
supersession
scope reduction
confidence reduction
```

Historical campaigns must never be rewritten because a knowledge claim is later retired.

---

# 20. Security Threat Model

Minimum scenarios:

| ID | Threat | Expected Result |
|---|---|---|
| T28-001 | Outcome data injection | Validate source/provenance |
| T28-002 | Fake performance evidence | Reject / flag |
| T28-003 | Correlation presented as causation | Block / qualify |
| T28-004 | Single campaign becomes universal rule | Scope as provisional |
| T28-005 | Contradictory evidence hidden | Preserve contradiction |
| T28-006 | Private client outcome becomes global knowledge | DENY |
| T28-007 | Learning changes authorization | DENY |
| T28-008 | Optimizer modifies security policy | DENY |
| T28-009 | Model confidence treated as empirical proof | Reject interpretation |
| T28-010 | Fabricated counterfactual | DENY |
| T28-011 | Stale learning applied as current truth | Freshness check |
| T28-012 | Provider drift ignored | Flag confounder |
| T28-013 | Skill self-modification | Require promotion |
| T28-014 | Worker privilege changes from performance | DENY |
| T28-015 | Rejected creative treated as universally bad | Preserve scope/context |
| T28-016 | Outcome linked to wrong asset version | DENY / reconcile |
| T28-017 | Experiment result tampering | Detect |
| T28-018 | Calibration based on insufficient sample | Flag |
| T28-019 | Evidence laundering | Require provenance |
| T28-020 | Learning rollback destroys history | Preserve historical record |
| T28-021 | Cross-client pattern leakage | DENY |
| T28-022 | Automated causal claim generation | Require epistemic qualification |
| T28-023 | Hidden outcome-source substitution | Detect |
| T28-024 | Optimizer bypasses human review | DENY |
| T28-025 | Unknown converted into certainty | Preserve UNKNOWN |

---

# 21. Adversarial Validation

Test:

- poisoned outcome feeds;
- manipulated attribution;
- fake experiments;
- contradictory evidence;
- tiny-sample overconfidence;
- client-data leakage;
- provider/model drift;
- optimizer privilege escalation;
- causal-language injection;
- fabricated counterfactuals;
- stale knowledge;
- hidden scope expansion.

Use held-out cases and mutated learning configurations.

---

# 22. Integration Workflows

## A — Campaign Postmortem

```text
Campaign Complete
      ↓
Outcome Collection
      ↓
Decision Ledger
      ↓
Outcome Linkage
      ↓
Confounder Collection
      ↓
Evaluation
      ↓
Learning Signals
      ↓
Postmortem
```

## B — Learning Promotion

```text
Observed Evidence
      ↓
Learning Hypothesis
      ↓
Supporting / Contradicting Evidence
      ↓
Validation
      ↓
Review
      ↓
Promotion Proposal
      ↓
Governed Knowledge Registry
```

## C — Future Recommendation

```text
New Campaign
      ↓
Current Context
      ↓
Relevant Validated Knowledge
      ↓
Visual DNA
      ↓
Fresh Evidence
      ↓
Creative Reasoning
      ↓
Recommendation
      ↓
Confidence + Applicability
```

Historical learning informs; it does not dictate.

## D — Skill Improvement

```text
Campaign Outcomes
      ↓
Worker / Skill Evaluation
      ↓
Failure Pattern
      ↓
Improvement Proposal
      ↓
Skill Version
      ↓
Evaluation
      ↓
Promotion
```

## E — Visual Learning

```text
Visual Output
      ↓
Visual Evaluation
      ↓
Campaign Outcome
      ↓
Pattern Candidate
      ↓
Evidence Accumulation
      ↓
Validation
      ↓
Visual Knowledge Update Proposal
```

---

# 23. Suggested Module Structure

```text
src/creative_learning/
|
+-- decision_ledger/
+-- outcome_ingestion/
+-- outcome_normalization/
+-- outcome_linkage/
+-- attribution/
+-- learning_signals/
+-- hypotheses/
+-- counterfactuals/
+-- experiments/
+-- calibration/
+-- promotion/
+-- contradiction/
+-- pattern_discovery/
+-- skill_improvement/
+-- worker_learning/
+-- visual_learning/
+-- learning_memory/
+-- freshness/
+-- drift/
+-- learning_observability/
+-- learning_api/
+-- learning_governance/
```

Do not duplicate Phase 18/19 learning or knowledge engines. Extend them through explicit interfaces.

---

# 24. API Boundary

Conceptual operations:

```text
POST /learning/decisions
GET  /learning/decisions/:id

POST /learning/outcomes
GET  /learning/campaigns/:id/outcomes

POST /learning/hypotheses
GET  /learning/hypotheses/:id

POST /learning/experiments
GET  /learning/experiments/:id

GET  /learning/calibration
GET  /learning/patterns

POST /learning/promotions
POST /learning/promotions/:id/review
POST /learning/promotions/:id/rollback

GET  /learning/campaigns/:id/postmortem
GET  /learning/campaigns/:id/lessons
```

Exact naming must follow existing API conventions.

---

# 25. Observability and Reliability

Track:

```text
decision_recorded
outcome_ingested
outcome_normalized
outcome_linked
learning_signal_created
hypothesis_created
experiment_started
experiment_completed
calibration_updated
promotion_proposed
promotion_approved
promotion_rejected
knowledge_rolled_back
knowledge_retired
contradiction_detected
drift_detected
learning_blocked
cross_scope_learning_denied
```

The system must tolerate delayed outcomes, duplicate feeds, provider outages, partial campaign records, missing attribution, metric-definition changes, model drift, knowledge rollback, conflicting updates, and late-arriving evidence.

Unknown or incomplete state must remain explicit.

---

# 26. Acceptance Gates

## Gate 01 — Decision Ledger
Material campaign decisions are versioned and immutable.

## Gate 02 — Outcome Provenance
Every outcome retains original source semantics.

## Gate 03 — Version-Aware Linkage
Outcomes map to the actual launched asset/version.

## Gate 04 — Epistemic Separation
Observation, attribution, interpretation, hypothesis, and causal claim remain distinct.

## Gate 05 — Counterfactual Integrity
No counterfactual result is fabricated.

## Gate 06 — Experiment Registry
Controlled experiments are represented separately from ordinary observations.

## Gate 07 — Calibration
Prediction confidence can be compared with observed evidence.

## Gate 08 — Learning Promotion
Knowledge requires governed promotion.

## Gate 09 — Contradiction Preservation
Conflicting evidence remains visible.

## Gate 10 — Scope
Every learning object has explicit applicability.

## Gate 11 — Client Isolation
Private learning cannot leak into global knowledge.

## Gate 12 — Visual Learning
Visual observations remain evidence-backed and scoped.

## Gate 13 — Skill Improvement
Skill changes require versioning and evaluation.

## Gate 14 — Worker Governance
Performance cannot silently change authority.

## Gate 15 — Freshness
Stale knowledge is detected.

## Gate 16 — Drift
Model/provider/environment changes are observable.

## Gate 17 — Rollback
Promoted knowledge can be rolled back without destroying history.

## Gate 18 — Adversarial Security
All 25 Phase 28 security scenarios pass.

## Gate 19 — Cross-Phase Regression
Phases 1–27 remain green.

## Gate 20 — End-to-End Learning Loop
Campaign → outcome → learning → future recommendation works.

## Gate 21 — Human Review
Material learning promotion is reviewable.

## Gate 22 — Independent Validation
At least one validation path is meaningfully independent of the implementation under test.

---

# 27. Required Validation Standard

Phase 28 must not be declared complete merely because its unit tests pass.

For every major learning/security claim document:

```text
Claim
Threat
Assumption
Counterexample
Test
Observed Result
Confidence
Residual Risk
```

At minimum, validation must include:

- dedicated Phase 28 tests;
- cross-phase regression;
- 25 threat scenarios;
- integration workflows;
- adversarial/held-out tests;
- mutation testing where feasible;
- campaign-to-learning end-to-end validation;
- independent review of at least one critical learning path.

---

# 28. Definition of Done

Phase 28 is complete only when:

- material decisions are recorded;
- outcomes are normalized without loss of source meaning;
- outcomes link to exact campaign/asset versions;
- attribution limitations are explicit;
- learning signals are generated;
- hypotheses retain supporting and contradicting evidence;
- experiments are represented separately;
- calibration is measurable;
- learning promotion is governed;
- contradictions are preserved;
- learning scope is explicit;
- client confidentiality remains intact;
- visual learning is supported;
- worker/skill improvement is governed;
- knowledge freshness is enforced;
- provider/model drift is observable;
- rollback works;
- adversarial tests pass;
- cross-phase regression remains green;
- complete campaign-to-learning integration passes;
- documentation is complete;
- governance signs off.

---

# 29. Product Outcome

After Phase 28, ILYREN should be capable of expressing:

```text
We recommended X because of A, B, and C.

We executed X.

We observed Y.

We cannot prove X caused Y.

Evidence suggests Z may be worth testing.

Z applies to this type of campaign, not universally.

Confidence is moderate.

Here is the evidence.

Here is the contradictory evidence.

Here is the next experiment.
```

That is the required standard for an intelligence platform that learns without pretending to know more than the evidence supports.

---

# 30. Final Engineering Directive

**Implement Phase 28 as the ILYREN Creative Intelligence Operating Loop.**

Make every campaign capable of becoming structured organizational learning.

Do not turn performance analytics into simplistic “AI learned X” claims.

Do not turn correlation into causation.

Do not let successful outcomes silently validate every upstream decision.

Do not let failed outcomes erase useful context.

Do not let optimization mutate security.

Do not let learning expand authority.

Do not let private client information become global knowledge.

Preserve uncertainty.

Preserve contradiction.

Preserve history.

Preserve provenance.

The desired outcome is not:

> “ILYREN has analytics.”

The desired outcome is:

> **“ILYREN can learn from creative work while remaining honest about what the evidence actually proves.”**
