# Phase 20: Model Gateway & Provider Capability Report

## Executive Overview

This report details the integration of real LLM model providers behind the provider-neutral **LLM Model Gateway** (`src/model_gateway/`).

---

## Supported Providers & Fallback Strategy

1. **Google Gemini Live Adapter (`GeminiLiveProvider`):**
   - Connects to Google AI Studio Gemini API (`gemini-2.5-flash`, `gemini-1.5-pro`) when `GEMINI_API_KEY` is present.
   - Leverages `google-genai` SDK.
   - Automatic waterfall fallback to Sandbox provider upon quota or network error.

2. **Sandbox LLM Adapter (`SandboxLLMProvider`):**
   - Deterministic local testing and benchmark execution engine.
   - Guarantees 100% test reproducibility and offline operational continuity.

---

## Model Provenance & Redaction Matrix

- **Credential Redaction:** The `CredentialRedactor` systematically removes API keys (`AIzaSy...`, `sk-...`, Bearer tokens) prior to prompt dispatch and response logging.
- **Response Provenance:** Every model generation retains an immutable `ResponseProvenance` block:
  ```json
  {
    "provider": "google_or_sandbox",
    "model": "gemini-2.5-flash",
    "model_version": "2026.1",
    "request_id": "req_847a9f",
    "timestamp": 1788739200.0,
    "policy_version": "20.0",
    "structured_output_validated": true
  }
  ```

---

## Audit Verification

Tested and validated in `tests/phase20/test_model_gateway.py`. Zero credential leakage detected.
