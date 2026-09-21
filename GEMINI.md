# Agent Engineering Rules & Operating Memory (GEMINI.md)

This document defines the persistent engineering discipline, cognitive protocol, and decision framework that Antigravity must follow across all tasks.

---

## 1. Mandatory Planning & Self-Review Protocol

1. **Root Cause & Dependency Trace**:
   - Before proposing any solution, inspect and trace all related code paths, dependencies, styling hierarchies, and component interactions. Never guess or act solely on superficial symptoms.
2. **Draft & Self-Review Before Presentation**:
   - Always create a draft plan and critically self-review it against potential side effects, layout shifts, dark/light theme boundaries, and component coupling *before* presenting it to the user.

---

## 2. Multi-Option Scoring & Top-Route Selection

Before modifying or writing code, formulate multiple technical approaches and score each systematically. **Always select and execute the highest-scoring route.**

### Scoring Criteria:
1. **Conflict & Cascade Prevention (Highest Priority)**:
   - Does this approach ensure zero new conflicts or secondary errors?
   - Modifying one page or component must **never** affect, degrade, or introduce regressions into any other page, component, or route.
2. **Scope Isolation & Blast Radius**:
   - Is the change strictly confined to the target module/file?
   - Any solution risking global side effects, unwanted styling leaks, or cross-component coupling is heavily penalized.
3. **Architectural & Token Cleanliness**:
   - Does the fix use standard design tokens and clean architectural patterns rather than hardcoded overrides, static `!important` flags, or brute-force hacks?
4. **Deterministic Verification**:
   - Can the change be cleanly verified with zero type errors (`cmd /c npx tsc --noEmit` exiting with code `0`)?

---

## 3. Strict Anti-Regression & Quality Rules

1. **Zero Blind Trial-and-Error**:
   - Shotgun debugging, speculative edits, and guess-and-check cycles are strictly forbidden. Every edit must be intentional, scoped, and justified.
2. **Fix 1 Without Creating 10**:
   - Resolving one defect must never spawn secondary issues. If an approach causes cascading breakages across unrelated files, halt immediately and pivot to a more isolated route.
3. **Component & Page Independence**:
   - Workspaces and applications must preserve modularity. Page-level changes must remain self-contained.

---

## 4. Environment & Execution Standards

1. **Windows Command Standard**:
   - Always execute terminal tools and build scripts via `cmd /c <command>` (e.g., `cmd /c npx tsc --noEmit`) to bypass PowerShell script execution policy restrictions.
2. **Mandatory Type Verification**:
   - Always verify TypeScript type integrity before concluding any task.
