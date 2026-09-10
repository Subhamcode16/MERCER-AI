# EXTERNAL-INTELLIGENCE-TRUST-MODEL.md
## Phase 29 Architecture Specification: External Intelligence Trust Model & Injection Defense

---

### 1. Overview

External intelligence (scraped trend blogs, industry reports, platform documentation) is treated as **untrusted data** and strictly segregated from internal execution contexts.

Under the invariants:
$$\mathbf{External\ Observation \neq Trusted\ Fact} \quad \mathbf{Model\ Output \neq Trusted\ Input}$$

---

### 2. Source Reliability Classification

- `HIGH_ACADEMIC_INDUSTRY`: Vetted analyst research (McKinsey, Gartner, academic papers).
- `MEDIUM_PLATFORM_DOCS`: Official Meta, TikTok, and Google developer documentation.
- `LOW_UNVERIFIED_WEB`: Public blogs, forums, uncorroborated social media threads.
- `UNTRUSTED_ADVERSARIAL`: Synthetic or malicious inputs carrying prompt injection directives.

---

### 3. Prompt Injection Defense Pipeline

The `ExternalIntelligenceIngest` pipeline scans incoming content for prompt injection signatures:
- Direct command directives (`"ignore previous instructions"`, `"system prompt:"`)
- Privilege escalation attempts (`"grant admin"`, `"elevate permission"`)
- Database mutation instructions (`"override governance"`, `"set is_admin = true"`)

All matching patterns are stripped, neutralized to `[STRIPPED_DIRECTIVE]`, and flagged with `is_safe_for_synthesis = False`.
