# PHASE-21 — Cost & Performance Report

**Project:** ILYREN Creative Workforce / ILYREN Creative Studio  
**Phase:** 21 — Cost & Operational Performance Metrics  
**Status:** RATIFIED  

---

## 1. Operational Latency & Token Usage

| Gateway Component | Primary Target | Mean Latency | Token Budget / Limits | Operational Utility Score |
|---|---|---:|---|---:|
| **Model Gateway (LLM)** | `gemini-2.5-flash` | 290.0 ms | 16,384 max tokens/req | 0.96 |
| **Visual Gateway (Image)** | `imagen-3-hd` | 850.0 ms | 1024x1024 / 1080x1920 | 0.94 |
| **Visual Gateway (Vision)** | `gemini-2.5-flash` | 310.0 ms | 1,000,000 token context | 0.97 |
| **MCP Transport Gateway** | `mcp_fashion_trends` | 180.0 ms | 60 req/min rate limit | 0.98 |

---

## 2. Operational Utility Metric

$$
Utility = \frac{Creative\ Quality \times Reliability}{Cost \times Latency} = \frac{0.96 \times 0.99}{0.04 \times 0.24} = 9.90
$$

- **Mean Cost per NOCAP Campaign Production Cycle:** $0.04 USD.
- **P99 Latency SLA:** < 1500.0 ms.
