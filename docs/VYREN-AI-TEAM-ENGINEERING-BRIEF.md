# VYREN — AI Team Frontend Engineering Brief

**Scope:** AI Team only  
**Goal:** Redesign AI Team as VYREN's persistent digital creative organization, not an agent administration console.

## Product definition
AI Team answers: **“Who is working with me, what are they doing, how do they collaborate, and what needs my attention?”**

The user should understand:
`WHO → WHAT → WHY → OUTPUT → HANDOFF → HUMAN ATTENTION`

## Workforce model
Coworkers may span:
`Strategy | Creative | Intelligence | Production | Quality`

Each coworker has:
- identity
- role
- department
- responsibilities
- current work
- campaign context
- status
- recent contributions
- skills
- bounded tools/capabilities
- memory scope
- approval requirements

Never make technical IDs such as `creative_director_01` the primary identity.

## Team information architecture
One global sidebar entry: **AI Team**.

Inside it:
`My Team | Active Work | Campaign Rooms | Conversations | Handoffs | Skills | Routines | Activity`

These should be internal views, not additional global navigation.

## Team Home
Header:
`AI TEAM — Your creative organization`

Show:
- active coworkers
- working/waiting/needs-you states
- organizational workload
- attention count

Do not lead with raw telemetry.

## Department overview
Show Strategy, Creative, Intelligence, Production, Quality with:
- coworker count
- active workload
- campaigns involved
- attention required

Counts must come from data.

## Coworker cards
Human-readable card:
- name
- role
- department
- status
- current campaign/task
- recent contribution
- Open

Avoid dense technical metadata.

## Coworker detail
Show:
- identity
- current work
- progress
- responsibilities
- recent contributions
- collaboration history
- received/sent handoffs
- skills
- bounded capabilities
- approval boundaries

Example:
`Can research, analyze Visual DNA, develop directions; final campaign selection/production/external execution requires appropriate approval.`

## Active Work
Show work relationships rather than an agent list:
`Campaign → coworker → task → status`

Example:
Autumn/Winter 2026:
- Creative Director → Creative Direction
- Visual Intelligence → Visual validation
- Brand Strategist → Audience positioning

## Campaign Rooms
Connect Team to Campaign Studio:
- campaign
- team members
- current phase
- active handoffs
- human decision required
- Open in Campaign Studio

Do not duplicate the complete campaign UI.

## Conversations
Chat is an interaction mode, not the entire Team product.

Support:
- talk to team
- @mention coworker
- ask status
- request bounded task
- review handoff
- challenge recommendation

Responses should identify coworker, context, result, evidence, and next action. Never expose hidden chain-of-thought.

## Handoffs
First-class object:
`Proposed | Accepted | Working | Returned | Completed | Blocked`

Show sender, receiver, purpose, attached outputs/evidence, and status.

A handoff does not grant authority.

## Skills
Show reusable governed capabilities:
- skill name
- owner
- version
- usage
- scope

Do not build an unrestricted skill marketplace.

## Routines
Show bounded recurring work:
- name
- owner
- cadence/trigger
- current status

Explicitly preserve: scheduled work is not authorization for consequential execution.

## Memory
Human-readable scope:
`Campaign Memory | Brand Memory | Skill Memory | Worker Memory | Institutional Knowledge`

Show what a worker can access and what it cannot. Do not expose raw vector/database terminology.

## Activity
Show organizational history:
- AI action
- human action
- system event
- approval
- handoff
- error

Do not claim real-time telemetry unless backend data exists.

## Attention queue
Prominently show:
- decisions
- approvals
- blocked work
- conflicts

Example:
`Select Creative Direction / Approve Production Package / Resolve conflict`

## Status model
`Available | Thinking | Working | Waiting | Needs You | Blocked | Paused | Completed`

Use deterministic mock state until real backend events exist.

## Integration with Campaign Studio
Shared objects:
`campaign, task, contribution, handoff, decision, approval, asset`

Team → Open in Campaign Studio  
Studio → View Team

Do not create disconnected duplicate datasets.

## Mock-data architecture
Centralize typed fixtures:
`Worker, Department, Task, Contribution, Handoff, CampaignRoom, Skill, Routine, ApprovalRequest, ActivityEvent`

Fixtures must be replaceable by future APIs.

## Preserve Phase-26 concepts
Where compatible, preserve:
- worker identity/lifecycle
- roles/capabilities
- versioned skills
- scoped memory
- campaign rooms
- collaboration
- handoffs
- bounded delegation
- routines
- tool bindings
- human approvals
- evidence
- audit/activity

This is a product-layer transformation, not a backend rewrite.

## Visual language
Premium VYREN editorial:
near-black, warm ivory, subtle borders, restrained accents, elegant typography, generous spacing.

Avoid:
- excessive neon
- dense telemetry
- raw IDs
- endless agent rows
- oversized technical badges
- an empty chat canvas dominating the screen

## Required states
No team, populated, available, working, waiting, blocked, needs-you, handoff pending, approval pending, no campaign, campaign-linked, unavailable, error, stale activity.

## Governance invariants
`Intelligence ≠ Authorization`  
`Recommendation ≠ Decision`  
`Decision ≠ Execution Permission`  
`Role ≠ Permission`  
`Skill ≠ Authority`  
`Routine ≠ Authorization`  
`Collaboration ≠ Privilege Transfer`  
`Shared Context ≠ Shared Authority`  
`Natural Language Command ≠ Permission`  
`Model Output ≠ Truth`  
`Tool Result ≠ Authority`  
`Learning ≠ Policy Mutation`  
`Self-Improvement ≠ Self-Authorization`

## Acceptance checklist
- [ ] Feels like a persistent creative organization
- [ ] Human-readable coworker identities
- [ ] Active work visible
- [ ] Campaign Rooms connect to Studio
- [ ] Handoffs are first-class
- [ ] Attention/approval queue visible
- [ ] Coworker detail communicates role/work/boundaries
- [ ] Skills/routines understandable and governed
- [ ] Memory scope visible
- [ ] Chat does not dominate
- [ ] Activity communicates history
- [ ] Mock data centralized/replacable
- [ ] Existing workforce concepts preserved
- [ ] Required states implemented
- [ ] Accessibility/responsive checks pass
- [ ] Typecheck/build/regression pass
- [ ] No unrelated tabs redesigned

## Required engineering report
Return:
1. files/components changed
2. routes changed
3. new components
4. worker/team data changes
5. campaign-room integration
6. handoff implementation
7. skills/routines/memory surfaces
8. activity/attention surfaces
9. preserved infrastructure
10. tests
11. typecheck/build results
12. limitations
13. visual verification
14. backend assumptions
15. confirmation that unrelated tabs were not redesigned

Do not call the surface production-ready merely because it builds.
