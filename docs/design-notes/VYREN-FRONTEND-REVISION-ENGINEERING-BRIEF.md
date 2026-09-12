# VYREN Frontend Revision — Engineering Implementation Brief

**Parent Company:** ILYREN  
**Product:** VYREN  
**Definition:** VYREN is an AI-powered Brand Intelligence & Creative Operating System that helps brands create, decide, design, learn, improve, and evolve.

## 1. Objective

Revise the existing frontend into the actual VYREN product experience.

**Do not rebuild from scratch. Do not delete existing functionality. Do not create another architectural phase.**

The existing Phase 20–30 functionality is valuable infrastructure. Reorganize, simplify, rebrand, and improve the experience around the VYREN product vision.

The target feeling is a **premium AI creative headquarters / intelligent creative organization for brands**, rather than an enterprise control dashboard exposing internal architecture.

## 2. Canonical Product Context

VYREN serves new brands, existing brands, brands undergoing rebranding/evolution, founders, creative teams, agencies, and established organizations.

VYREN is **not limited to visual consumer brands**.

The AI workforce is a core product experience. Visual DNA is a core intelligence subsystem, not the entire product.

### New Brand

Brand idea → research → audience/market understanding → positioning → brand strategy → identity exploration → visual identity → creative system → campaign → launch → learning → evolution.

### Existing Brand

Existing website/social/packaging/products/campaigns/guidelines/assets/history/outcomes → understand → audit → identify gaps → discover opportunities → recommend → evolve → create → measure → learn → improve.

**Do not assume every existing brand needs a new identity.**

## 3. Critical Branding Change

Remove every product-facing occurrence of:

- MERCERAI
- MERCER AI
- MERCER

Replace with:

- **VYREN** for the product.
- **ILYREN** where the parent company is relevant.

Audit sidebar, logo/wordmark, page titles, browser metadata, breadcrumbs, demo tenant labels, sample data, empty states, worker descriptions, campaigns, settings, and infrastructure screens.

**Required result: MERCER references remaining in product UI = 0.**

Do not introduce another product name.

## 4. Current UX Problem

The existing frontend exposes too much underlying architecture as primary navigation, including Observatory, Foresight Matrix, Attribution & Radar, Campaign Studio, Team Mode, Material Library, Atlas, Research, Knowledge, Archive, Model & MCP Gateways, Notifications, Settings, and FAQ.

These are useful capabilities, but the current presentation makes the product feel like an AI infrastructure/intelligence control system.

The target is:

> **A premium creative headquarters where an intelligent AI organization helps build and evolve brands.**

## 5. Target Primary Navigation

### WORKSPACE
- Home
- Brand
- Projects
- Campaigns

### CREATE
- Creative Studio
- Visual DNA
- Assets

### INTELLIGENCE
- Research
- Knowledge

### WORKFORCE
- AI Team

### UTILITY
- Activity
- Settings

Do not expose every Phase 20–30 subsystem in the primary sidebar.

## 6. Existing → New Mapping

| Existing Surface | Target Location |
|---|---|
| Observatory | Intelligence → Advanced Intelligence / Activity |
| Foresight Matrix | Intelligence → Strategic Intelligence |
| Attribution & Radar | Campaign → Outcomes |
| Campaign Studio | Campaigns |
| Team Mode | AI Team |
| Material Library | Visual DNA / Assets |
| Atlas | Brand / Intelligence |
| Research | Research |
| Knowledge | Knowledge |
| Archive | Projects / Assets |
| Model & MCP Gateways | Settings → Infrastructure |
| Notifications | Activity |
| Settings | Settings |
| FAQ | Settings → Help |

**Do not delete existing functionality.** Preserve routes where practical; use nested routes, redirects, or compatibility paths when necessary.

## 7. Home — Highest Priority

Home should not be an observability dashboard.

Primary question:

> **What are we building?**

Primary interaction:

```text
What are we building?

[ Tell VYREN what you're working on... ]

                     Start with VYREN →
```

Provide two clear paths:

**Start a new brand** — Build a brand from an idea.

**Bring an existing brand** — Give VYREN your existing brand and let it understand, audit, and evolve it.

Below this, surface:

- Your Brands
- Recent Projects
- Recent Campaigns
- AI Team activity
- useful intelligence/insights

Do not lead with graphs, governance counters, Phase numbers, model infrastructure, or telemetry.

The Home experience should feel calm, premium, intelligent, creative, and immediately understandable.

## 8. Brand Workspace

The Brand page should become the central context surface.

Surface:

- brand identity;
- positioning;
- audience;
- products;
- brand status;
- Visual DNA summary;
- strategic questions;
- research;
- active projects;
- active campaigns;
- AI workforce activity;
- recent decisions;
- next recommended action.

Desired perception:

> **“VYREN understands my brand.”**

## 9. AI Team

Use the existing Team Mode implementation as the foundation.

Reframe it as **AI Team / AI Creative Workforce**.

Example roles:

- Strategy
- Research / Intelligence
- Creative Director
- Visual Intelligence
- Content
- Review

The experience should communicate:

> **“These are persistent AI coworkers working on my brand.”**

Preserve useful existing capabilities including worker status, collaboration, mentions, handoffs, scoped tools, references, canvas where useful, model selection where useful, approvals, and existing worker architecture.

Do not expose hidden model reasoning.

Maintain authority and approval boundaries.

## 10. Creative Studio

Creative Studio should become a major user-facing creation surface.

Target workflow:

```text
Brief / Question
      ↓
Research & Intelligence
      ↓
Creative Exploration
      ↓
Creative Directions
      ↓
Visual Development
      ↓
Review
      ↓
Assets / Campaign
```

The user should move naturally from **thinking → direction → creation**.

## 11. Visual DNA

Retain existing material/visual intelligence work.

Position it as:

> **VYREN Visual DNA**

Surface:

- visual references;
- extracted visual characteristics;
- typography;
- color;
- composition;
- texture/material;
- visual relationships;
- evidence/provenance where supported;
- creative implications.

Do not reduce Visual DNA to a generic moodboard or image gallery.

Desired perception:

> **“This is how VYREN understands what my brand looks and feels like.”**

## 12. Campaigns

Campaign Studio becomes the user-facing **Campaigns** area.

A campaign should connect:

**Objective → Intelligence → Creative Direction → Assets → Review → Production → Outcome**

Do not expose every Phase 28/29/30 mechanism as separate navigation.

Those systems should power the experience underneath.

## 13. Research and Knowledge

Keep both as distinct destinations.

**Research:** What should VYREN investigate?

**Knowledge:** What does VYREN already know about this brand?

Make the distinction clear.

## 14. Advanced Intelligence Surfaces

Existing screens such as Strategic Intelligence Observatory, Foresight Matrix, Attribution/Calibration, Model & MCP Gateways, governance, and institutional operations are **not to be deleted**.

Move them deeper into the application as advanced/power-user surfaces.

Change hierarchy, not functionality.

## 15. Visual Design Direction

Preserve the existing foundation:

- dark environment;
- premium/editorial aesthetic;
- restrained borders;
- refined typography;
- subtle gradients;
- controlled accent colors;
- sophisticated data visualization;
- strong information hierarchy.

Shift the overall feeling from:

> **AI command center**

to:

> **premium creative headquarters.**

Avoid excessive dashboard metrics, system counters, Phase labels, infrastructure terminology, and technical status panels on primary user-facing screens.

## 16. UX Principle

The user should never need to ask:

> “Which subsystem should I open?”

The product should make them think:

> **“I have a brand problem. VYREN can help me solve it.”**

Natural language should be an important entry point.

## 17. Technical Implementation Rules

Before changing the UI:

1. Inspect the existing repository.
2. Inventory routes.
3. Inventory reusable components.
4. Inventory design tokens.
5. Inspect existing API/backend integrations.
6. Identify functional screens.
7. Identify reusable components.
8. Preserve authentication and data flows.

Implement in this order:

### P0 — Core Product Experience
1. Rebrand MERCER → VYREN.
2. New navigation architecture.
3. Application shell.
4. Home.
5. Brand Workspace.
6. AI Team.

### P1 — Core Creative Workflow
7. Creative Studio.
8. Visual DNA.
9. Campaigns.
10. Assets.
11. Research.
12. Knowledge.

### P2 — Advanced Surfaces
13. Reorganize advanced intelligence surfaces.
14. Activity.
15. Settings / infrastructure.
16. Responsive and accessibility refinement.

## 18. Do Not

Do not:

- rebuild the backend;
- delete Phase 20–30 functionality;
- create Phase 31;
- start another architecture expansion;
- turn every screen into a dashboard;
- make Home an analytics dashboard;
- expose every internal intelligence subsystem;
- replace the AI workforce with a generic chatbot;
- reduce Visual DNA to a moodboard;
- make VYREN fashion-only;
- make VYREN existing-brand-only;
- assume all brands need rebranding;
- introduce MERCER again;
- introduce another product name;
- add unnecessary dependencies.

## 19. Validation

Run:

- lint;
- typecheck;
- tests;
- production build.

Visually verify at minimum:

- Home;
- Brand;
- AI Team;
- Creative Studio;
- Visual DNA;
- Campaigns;
- Research;
- Knowledge;
- one advanced intelligence surface;
- Settings.

Verify responsive behavior and basic accessibility:

- semantic navigation;
- keyboard focus;
- labels;
- reasonable contrast;
- reduced-motion consideration;
- responsive layouts.

## 20. Final Engineering Report

Return:

```text
VYREN FRONTEND REVISION
────────────────────────

Status:
COMPLETE / BLOCKED

Repository inspected:
YES / NO

Routes changed:
...

Routes added:
...

Routes preserved:
...

Components changed:
...

Components created:
...

Components removed:
...

MERCER references remaining:
0 / [number]

Authentication:
PASS / FAIL

Workspace:
PASS / FAIL

Brand:
PASS / FAIL

AI Team:
PASS / FAIL

Creative Studio:
PASS / FAIL

Visual DNA:
PASS / FAIL

Campaigns:
PASS / FAIL

Research:
PASS / FAIL

Knowledge:
PASS / FAIL

Advanced Intelligence:
PASS / FAIL

Lint:
PASS / FAIL

Typecheck:
PASS / FAIL

Tests:
PASS / FAIL

Production Build:
PASS / FAIL

Visual Verification:
PASS / FAIL

Known Issues:
...

Human Decisions Required:
...
```

## 21. Final Engineering Instruction

> **Do not treat the existing frontend as something to throw away. It is the first-generation implementation of a much larger architecture. Transform it into the first-generation VYREN product experience: simpler on the surface, deeper underneath, brand-centric, creative, intelligent, premium, and immediately understandable.**
>
> **Preserve the machinery. Redesign the experience. Optimize for a usable prototype.**
