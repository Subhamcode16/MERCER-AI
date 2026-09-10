# PHASE-21 — Model Routing Report

**Project:** ILYREN Creative Workforce / ILYREN Creative Studio  
**Phase:** 21 — Evidence-Based Model Routing  
**Status:** RATIFIED  

---

## 1. Executive Summary

`ModelRoutingPolicy` in `src/model_gateway/routing.py` enforces role-to-model routing based on benchmark metrics, visual capabilities, and context requirements.

---

## 2. Role-to-Model Mapping Matrix

| Workforce Role | Primary Model | Fallback Model | Rationale |
|---|---|---|---|
| **TREND_ANALYST** | `gemini-2.5-flash` | `sandbox-llm` | High speed, strong structured data extraction |
| **STRATEGIST** | `gemini-1.5-pro` | `sandbox-llm` | 2M token context for multi-doc synthesis |
| **DESIGNER** | `gemini-2.5-flash` / `imagen-3-hd` | `sandbox-llm` | High visual understanding & prompt expansion |
| **CONTENT_SPECIALIST** | `claude-3-5-sonnet` | `sandbox-llm` | Superior editorial tone and copy precision |
| **CRITIC** | `gemini-2.5-flash` | `sandbox-llm` | High-precision visual defect detection |
| **REVIEWER** | `gemini-1.5-pro` | `sandbox-llm` | Independent governance & compliance checking |

---

## 3. Critic Independence Verification

```text
Generation Role (DESIGNER) ≠ Critic Role (CRITIC)
```
- Verified by `routing.validate_critic_independence()`.
- Prevents models from evaluating their own outputs directly without independent reviewer gates.
