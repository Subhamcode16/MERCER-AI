# PHASE-21 — Architecture & Control Plane Specification

**Project:** ILYREN Creative Workforce / ILYREN Creative Studio  
**Phase:** 21 — Real Model, MCP & Visual Intelligence Integration  
**Status:** RATIFIED & INTEGRATION READY  

---

## 1. System Architecture Overview

Phase 21 connects the Phase 14–20 control plane abstractions to real-world LLM providers, vision models, image generation endpoints, and controlled Model Context Protocol (MCP) transport servers while preserving every security and execution authority invariant:

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$

```text
Human / Client
      ↓
Phase 16 Command Center
      ↓
Phase 15 / 17 Operations & Fabric
      ↓
Phase 14 Creative Workforce Bridge
      ↓
Phase 20 / 21 Model Workforce & Routing Policy
      ├───────────────┐
      ↓               ↓
LLM Gateway      Visual Gateway
(Gemini 2.5/     (Imagen 3 HD /
 Universal LLM)  Gemini Multimodal)
      │               │
      └───────┬───────┘
              ↓
          MCP Gateway
     (Controlled Transport)
              ↓
Visual Knowledge Benchmark v2 + Intelligence Evaluation
              ↓
Phase 18 / 19 Learning & Institutional Intelligence
```

---

## 2. Core Gateways & Routing Specifications

1. **LLM Model Gateway (`src/model_gateway/`):**
   - Universal OpenAI-compatible API adapter supporting Gemini 2.5 Flash/1.5 Pro, OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, DeepSeek V3/R1, Qwen 2.5, Meta Llama 3.3, and local Ollama endpoints.
   - Provider health detection, rate-limit handling, waterfall fallback, token budget manager, prompt redaction, and cryptographic audit ledgers.

2. **Visual Model Gateway (`src/visual_model_gateway/`):**
   - Multimodal vision analysis (`gemini-2.5-flash`) and image generation (`imagen-3-hd`) with fallback to local visual sandbox.
   - Cryptographic lineage tracking (`request_id`, `provider`, `model`, `timestamp`, `parent_artifact_id`, `content_hash`, `evaluation_record`).

3. **MCP Capability Transport Gateway (`src/mcp_gateway/`):**
   - Transport layer for external tools (`mcp_fashion_trends`, `mcp_inventory_core`).
   - Risk classification (`READ_ONLY`, `ANALYSIS`, `DRAFTING`, `TRANSFORMATION`, `MUTATION`, `DESTRUCTIVE`).
   - Toggle switch management, circuit breaker isolation, and sanitization of tool outputs as `UNTRUSTED_EXTERNAL_OBSERVATION`.

4. **Evidence-Based Model Routing (`src/model_gateway/routing.py`):**
   - Role-to-model mapping: `TREND_ANALYST` (Gemini 2.5 Flash), `STRATEGIST` (Gemini 1.5 Pro), `DESIGNER` (Gemini 2.5 Flash), `CONTENT_SPECIALIST` (Claude 3.5 Sonnet), `CRITIC` (Gemini 2.5 Flash), `REVIEWER` (Gemini 1.5 Pro).
