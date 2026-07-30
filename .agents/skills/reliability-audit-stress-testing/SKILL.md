---
name: "reliability-audit-stress-testing"
description: "A specialized skill for stress-testing API endpoints, validating rate limiters, benchmarking MongoDB under load, analyzing async task queue concurrency, checking database connection pool exhaustion, and identifying race conditions in financial ledgers."
---

# Reliability Audit & Stress-Testing Skill Instructions

When this skill is triggered, you must act as a Senior SDE / Staff Reliability Engineer to test the backend services of Mercer AI under heavy simulated load (e.g., up to 100k simulated users or high concurrent spikes).

## 🛠️ CORE TESTING OBJECTIVES

### 1. Concurrency & Race Conditions (Double-Spend Protection)
- **What to test**: Multiple concurrent threads or requests targeting the same user account's credit balance (e.g., trying to generate 10 images at once when only having 2 credits).
- **Goal**: Ensure the transaction ledger (`credit_transactions`) correctly serializes allocations, prevents a negative balance, and does not allow double-spending.
- **Methods**: Use `asyncio.gather` with `httpx.AsyncClient` sending requests in parallel within milliseconds.

### 2. Rate Limiting Validation
- **What to test**: Rate-limiting policies (e.g., `SlowAPI` limits on `/generate` or `/auth` endpoints).
- **Goal**: Verify requests exceeding limits receive a `429 Too Many Requests` status, and that rate limits are enforced per IP/user.
- **Methods**: Script requests in a loop exceeding the limit threshold and assert `response.status_code == 429`.

### 3. Async Job Queues & Polling Overhead
- **What to test**: Backlog of multiple long-running async generator jobs (`BackgroundTasks` queue).
- **Goal**: Ensure the server does not freeze when the task pool is full, and status polling (`GET /jobs/{job_id}`) remains highly responsive under load.
- **Methods**: Trigger multiple mock generation tasks simultaneously and repeatedly poll statuses concurrently.

### 4. Database Connection Pool & Indexing Checks
- **What to test**: MongoDB operations under concurrent query pressure.
- **Goal**: Verify connection pools do not exhaust and that query times do not degrade exponentially under large virtual user loads. Ensure all queried fields (`user_id`, `job_id`, etc.) have MongoDB indexes.
- **Methods**: Perform stress queries against the `users` and `credit_transactions` collections.

---

## 📋 AUTOMATED STRESS-TEST TEMPLATE

Write a dedicated stress-testing script (e.g., `tests/stress_test.py` or `scratch/stress_test.py`) that implements:
1. **Mock Endpoints/Services**: Intercept or mock out heavy external resources (like the actual Gemini API call) so we can stress test the local server architecture without rate-limiting external APIs.
2. **Dynamic Concurrent Requests**: Uses python `asyncio` to swarm endpoints concurrently.
3. **Structured Reporting**: Prints a final breakdown including:
   - Total Requests Sent
   - Success Rate (%)
   - Failure Rate (%) & HTTP Status Codes (e.g., 429, 402, 401, 500)
   - Min / Average / Max Latency (ms)
   - Race condition anomalies detected (e.g., credit ledger discrepancies)
