# II-001 — Campaign Intelligence Layer Master Specification

**Status:** Engineering Specification — Established  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Campaign Intelligence / Knowledge Layer

## Mission

The Campaign Intelligence Layer transforms campaign context and authoritative knowledge into a structured, explainable campaign system:

`Campaign Context → Communication Intents → Evidence Requirements → Asset Strategy → Optimal Asset Set → Canonical Narrative → Channel Projections → Evaluation → Adaptive Replanning`

It is a campaign reasoning and optimization system, not merely a prompt generator or image-generation planner.

## Intelligence Boundary

**Intelligence Layer:** determines what should be communicated, why, how much evidence is required, which assets should exist, which combination is optimal, how assets relate, and what should change.

**Engineering / Execution Layer:** determines how decisions are executed, generated, rendered, stored, and run.

`Intelligence → Decision / Specification → Engineering → Execution`

## Canonical Pipeline

```text
CAMPAIGN INPUT
    ↓
KNOWLEDGE ASSEMBLY
    ↓
CONTEXT VALIDATION
    ↓
COMMUNICATION INTENT ENGINE
    ↓
EVIDENCE REQUIREMENT ENGINE
    ↓
ASSET STRATEGY
    ↓
ASSET SET OPTIMIZER
    ↓
NARRATIVE ENGINE
    ↓
CHANNEL PROJECTION ENGINE
    ↓
GENERATION PLAN
    ↓
EXECUTION
    ↓
EVALUATION
    ↓
FEEDBACK / DIAGNOSIS
    ↓
ADAPTIVE REPLANNING
```

## Four Core Responsibilities

1. **DERIVE** — determine what should be communicated and what evidence supports it.
2. **OPTIMIZE** — determine the strongest campaign configuration.
3. **EVALUATE** — determine whether the resulting campaign satisfies its intended architecture.
4. **ADAPT** — determine the smallest sufficient correction when evaluation reveals a problem.

`DERIVE → OPTIMIZE → EVALUATE → ADAPT → REPEAT`

## Canonical Intelligence Objects

- Campaign
- Campaign Objective
- Campaign Context
- Communication Intent
- Evidence Requirement
- Asset Strategy
- Asset Requirement
- Asset
- Narrative Graph
- Channel Projection
- Knowledge Gap
- Evaluation Result
- Revision

## Provenance

Every derived intelligence object must preserve provenance sufficient to answer where a decision came from, what authority produced it, how confident the system is, what evidence supports it, and what rationale produced it.

## Lifecycle

`CANDIDATE → DERIVED → VALIDATED → ACCEPTED → LOCKED`

Alternative paths:

`CANDIDATE → REJECTED`

`LOCKED → REOPENED → REVISED → REVALIDATED → LOCKED`

## Authority Model

**Hard:** product truth, hard brand constraints, locked campaign invariants, explicit locked intent.

**Soft:** derived intent, inferred intent, creative opportunities, narrative preferences, channel optimizations, exploratory concepts.

Soft intelligence may optimize within hard intelligence but may never silently override it.

## Knowledge Is Not Decision

`KNOWLEDGE ≠ DECISION`

Domain knowledge defines what is true; campaign intelligence determines what that truth means for the current campaign.

## Knowledge → Intelligence Boundary

```text
KNOWLEDGE LAYER
    ↓
Product / Brand / Audience / Channel Knowledge
    ↓
INTELLIGENCE LAYER
    ↓
Campaign Reasoning
    ↓
ENGINEERING LAYER
    ↓
Execution
```

## Shared Semantic State

Agents operate against a canonical campaign state / blackboard rather than independently inventing campaign understanding. The detailed blackboard contract is deferred to II-014.

## Agent Responsibility Principle

Specialized agents own specialized reasoning:

- Intent Agent
- Evidence Agent
- Asset Strategy Agent
- Creative Search Agent
- Narrative Agent
- Channel Agent
- Evaluator
- Replanning Agent

They operate through shared semantic state and deterministic contracts rather than as one unconstrained general-purpose agent.

## Prompt Engine Boundary

```text
Campaign Intelligence
    ↓
Finalized Asset Specification
    ↓
Prompt Compiler
    ↓
Generation Model
```

The Prompt Compiler must not independently decide campaign strategy.

## Master Contract

> Given a campaign context and authoritative knowledge, the Intelligence Layer shall derive, validate, optimize, and continuously evaluate a structured campaign system consisting of communication intents, evidence requirements, asset strategy, narrative architecture, and channel projections while preserving product truth, brand constraints, provenance, uncertainty, and human strategic authority.

## Phase II Gate

II-001 establishes the semantic boundary for the remaining engineering specifications. It does not yet prescribe implementation schemas, database technology, numerical thresholds, or runtime code.
