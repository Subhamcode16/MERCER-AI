---
VIS-ID: ARC-001
Title: Creative Decision Engine
Version: 1.0.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-29
Depends On:
  - VIS-001
  - VIS-002
  - VIO-001
  - VIO-002
  - VIO-003
  - VIO-004
Next:
  - ARC-002 Planning Engine
  - DNA-001 DNA Framework
---

# Creative Decision Engine

## Purpose

The Creative Decision Engine (CDE) is the reasoning core of the Visual Intelligence Platform.

Its responsibility is to transform structured knowledge into creative decisions before any rendering occurs.

The engine does not generate prompts.

The engine does not generate images.

The engine generates decisions.

---

# Philosophy

Knowledge alone is passive.

Execution alone is mechanical.

Reasoning connects the two.

The Creative Decision Engine exists to answer one question:

"What is the best creative decision given the current objective, context, constraints, memory, and evidence?"

---

# Responsibilities

The engine MUST

- interpret creative goals
- evaluate constraints
- retrieve relevant knowledge
- compare alternatives
- resolve conflicts
- justify decisions
- output structured decisions

The engine MUST NOT

- render images
- execute prompts
- own persistent memory
- modify Visual DNA directly

---

# Inputs

The engine receives

- User Intent
- Visual DNA
- Knowledge Graph
- Semantic Graph
- Memory
- Constraints
- Business Objectives
- Brand Objectives
- Evaluation History

---

# Outputs

The engine produces

- Creative Decisions
- Confidence Scores
- Decision Evidence
- Decision Trace
- Alternative Decisions
- Missing Information

These outputs become inputs to the DNA Framework.

---

# Internal Pipeline

The engine reasons in seven stages.

## Stage 1

Goal Interpretation

↓

Understand what success means.

---

## Stage 2

Context Retrieval

↓

Retrieve

- previous projects
- brand knowledge
- product knowledge
- audience knowledge

---

## Stage 3

Constraint Analysis

↓

Identify

- budget
- platform
- renderer
- campaign
- timing
- cultural constraints

---

## Stage 4

Alternative Generation

↓

Generate multiple creative approaches.

Example

Luxury Wedding Campaign

↓

Approach A

Royal Palace

↓

Approach B

Luxury Garden

↓

Approach C

Temple Courtyard

The engine should think in alternatives.

---

## Stage 5

Decision Evaluation

Every alternative is evaluated against

Business

Brand

Audience

Narrative

Product

Visual Consistency

Budget

Platform

Renderer Capability

---

## Stage 6

Decision Selection

Select the highest-scoring solution.

---

## Stage 7

Decision Explanation

Every selected decision should remain explainable.

Example

Chosen Environment

↓

Palace

Reason

Luxury positioning requires architectural grandeur.

---

# Reasoning Principles

The engine follows six reasoning principles.

## Goal First

Never optimize aesthetics before objectives.

---

## Brand Before Style

Brand identity overrides visual preference.

---

## Product Before Decoration

The product must remain the hero.

---

## Audience Before Trends

Audience relevance overrides novelty.

---

## Consistency Before Variety

Identity changes require explicit approval.

---

## Explainability Before Automation

Every important decision should remain inspectable.

---

# Decision Object

Every decision follows the same schema.

Decision

↓

Reason

↓

Evidence

↓

Confidence

↓

Alternatives

↓

Tradeoffs

↓

Owner

↓

Timestamp

This becomes the Decision Record.

---

# Decision Confidence

Every decision stores confidence.

Confidence derives from

Knowledge

Memory

Semantics

Evidence

Evaluation History

Low-confidence decisions may require

- user clarification
- additional reasoning
- experimentation

---

# Failure Handling

The engine must detect

- conflicting objectives
- missing evidence
- low confidence
- inconsistent semantics
- impossible constraints

Failures are surfaced before generation.

---

# Success Criteria

The engine succeeds when

- reasoning is explainable
- decisions are reusable
- alternatives are evaluated
- confidence is measurable
- user interaction is minimized

---

# Open Questions

- Should reasoning become probabilistic?
- Should reinforcement learning improve decisions?
- How should conflicting expert opinions be resolved?

---

# Research Dependencies

- Decision Theory
- Multi-Agent Planning
- Constraint Satisfaction
- Cognitive Science
- Creative Direction
- Human Expert Systems

---

# Engineering Notes

The Creative Decision Engine is implementation-independent.

Future implementations may use

- symbolic planning
- graph reasoning
- LLM planning
- hybrid reasoning
- reinforcement learning

The architecture remains unchanged.