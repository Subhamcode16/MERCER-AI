# VYREN — Campaign Studio Frontend Engineering Brief

**Scope:** Campaign Studio only  
**Goal:** Redesign Campaign Studio as VYREN's end-to-end creative workspace, not a template gallery.

## Product definition
Campaign Studio answers: **“What are we creating, and how is VYREN helping us create it?”**

Core lifecycle:
`Objective → Understand → Research → Creative Intelligence → Creative Directions → Select/Refine → Visual Development → Assets → Review → Production → Outcomes`

## Required information architecture
Campaign header:
- Campaign name
- Brand
- Objective
- Audience
- Status
- Human owner/decision maker
- AI Team presence

Internal navigation:
`Overview | Intelligence | Directions | Visuals | Assets | Review | Production | Outcomes`

Do not add more global sidebar items.

## Empty state
Replace the current template-first experience with:
- **What are we creating?**
- Start a Campaign
- Start from a brief
- Continue an initiative
- Explore previous campaign

Existing Material Intelligence / Cinematic Campaigns / Brand Archetypes may remain only as optional starting points.

## Overview
Must answer:
1. What are we making?
2. What does VYREN understand?
3. What has been decided?
4. What needs my attention?

Show campaign objective, audience, channels, brand constraints, relevant Visual DNA, discoveries, unknowns, approved decisions, and 3–5 prioritized next actions.

## Intelligence
Show intelligence *before* generation:
- campaign question
- audience signals
- brand context
- Visual DNA
- tensions/trade-offs
- evidence/provenance affordances
- epistemic status: Observed / Supported / Experimental / Correlated / Unknown

Never fabricate certainty.

## Creative Directions
Make this a signature surface. Show multiple direction cards, e.g.:
- controlled evolution
- contemporary reinterpretation
- controlled departure

Each card includes:
- core idea
- narrative
- visual language
- composition
- lighting
- material treatment
- audience rationale
- brand alignment
- risks/tensions
- evidence
- Explore / Compare / Select / Refine / Reject

Human selection remains explicit.

## Visual Development
Provide:
- reference board
- product/reference images
- Visual DNA references
- composition system
- camera/framing
- lighting
- color
- material
- typography
- environment
- shot families: Hero / Detail / Portrait / Product / Editorial / Social

This must be a workspace, not merely an image grid.

## AI Team integration
Show relevant coworkers contextually inside the campaign:
- who is working
- current task
- recent contribution
- next handoff

Example: Creative Director developing Direction 02; Visual Intelligence validating DNA.

Do not turn Campaign Studio into Team administration.

## Assets
Connect every asset to:
campaign, direction, shot, version, channel, status, approval, lineage.

States:
`Draft | In Review | Approved | Rejected | Superseded | Production Ready`

## Review
Separate AI critique from human approval. Provide:
- visual alignment
- brand alignment
- campaign alignment
- technical readiness
- issues
- evidence
- version comparison
- Approve / Request Revision / Reject / Comment

Preserve lineage.

## Production
Show approved deliverables by channel and readiness. Do not imply real publishing/export integrations unless backend support exists.

## Outcomes
Show observed outcome, attribution confidence, experiment context, comparisons, unknowns, and learning candidates. Prefer “Observed lift” over causal language unless causal methodology exists.

## Ask VYREN
Persistent entry point for bounded requests such as:
- Why was Direction 02 recommended?
- Show supporting evidence.
- Develop alternatives without changing locked constraints.
- What remains unknown?
- Prepare for review.

Expose decision-relevant evidence, not hidden chain-of-thought.

## Mock-data rules
Centralize typed fixtures. Prefer models such as:
`Campaign, IntelligenceItem, Direction, VisualStudy, Asset, Review, Outcome, WorkerContribution`.

Mock data must be replaceable by future API contracts. Never scatter hardcoded objects through JSX or imply unsupported live integrations.

## Preserve
Keep compatible:
- routes
- VYREN theme/typography/sidebar
- card/modal primitives
- campaign/backend contracts
- governance indicators
- existing asset components

Refactor only where required.

## Visual language
Premium VYREN editorial:
near-black background, warm ivory, subtle borders, restrained semantic accents, generous whitespace, strong typography, low noise.

Avoid neon-dashboard aesthetics.

## Required states
Empty, loading, populated, partial, error, unavailable integration, permission denied, pending approval, stale intelligence, conflicting intelligence, unknown/unresolved.

## Governance invariants
`Recommendation ≠ Decision`  
`Decision ≠ Execution Permission`  
`AI Critique ≠ Human Approval`  
`Learning ≠ Policy Mutation`  
`Model Output ≠ Truth`  
`External Observation ≠ Trusted Fact`  
`Visual Similarity ≠ Strategic Correctness`  
`Unknown Must Survive`

## Acceptance checklist
- [ ] No longer a template gallery
- [ ] Lifecycle is clear
- [ ] Intelligence precedes generation
- [ ] Multiple directions are comparable
- [ ] Human selection/approval is explicit
- [ ] AI coworkers appear contextually
- [ ] Visual development is a real workspace
- [ ] Asset lineage/version/status visible
- [ ] Review separated from AI critique
- [ ] Production readiness explicit
- [ ] Outcomes avoid unsupported causal claims
- [ ] Mock data centralized and replaceable
- [ ] All required states implemented
- [ ] Existing compatible infrastructure preserved
- [ ] No unrelated tabs redesigned
- [ ] Typecheck/build/regression pass

## Required engineering report
Return:
1. files/components changed
2. routes changed
3. new components
4. data/mock changes
5. screens implemented
6. preserved infrastructure
7. tests
8. typecheck/build results
9. limitations
10. visual verification
11. backend assumptions
12. confirmation that unrelated tabs were not redesigned

Do not call the surface production-ready merely because it builds.
