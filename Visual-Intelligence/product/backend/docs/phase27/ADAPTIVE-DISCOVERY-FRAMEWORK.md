# Phase 27: Adaptive Epistemic Discovery Framework

## 1. Epistemic Taxonomy
The discovery engine tracks client and campaign information across 5 formal epistemic states:

| State | Definition | Action Taken |
|---|---|---|
| `KNOWN` | Explicitly confirmed by human operator or authenticated brief. | Locked into prompt compile pipeline. |
| `INFERRED` | Statistically derived from calendar, past campaigns, or brand archetype. | Presented to human with confidence score. |
| `MISSING` | Required parameter is completely absent. | Triggers a `ConsequentialQuestion`. |
| `CONFLICTING` | Two sources provide divergent guidelines (e.g., brief says neon, brand guidelines forbid saturated color). | Flagged for operator arbitration. |
| `UNKNOWN` | Domain parameters not yet scanned or analyzed. | Scanned in background. |

## 2. Consequential Questioning Protocol
Rather than endless generic surveys, the engine formulates high-leverage multiple-choice options with explicit impact descriptions explaining how the choice affects visual styling, model weighting, and prompt compilation.
