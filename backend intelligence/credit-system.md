# Credit System

How credits get allocated, held, deducted, and refunded — designed to survive concurrent requests, provider failures, and retries without double-charging or leaking free generations.

## Data model

Two collections, not one balance field you mutate directly:

```python
# users collection — cached balance for fast reads
{
    "_id": "user_123",
    "tier": "pro",
    "credit_balance": 640,          # cached, derived from ledger — never the source of truth
    "renewal_date": datetime,
}

# credit_transactions collection — append-only ledger, source of truth
{
    "_id": ObjectId(...),
    "user_id": "user_123",
    "type": "reserve" | "commit" | "release" | "grant" | "refund" | "expire",
    "amount": -4,                   # negative for spend, positive for grant/refund
    "job_id": "...",                # links to generation_jobs
    "created_at": datetime,
}
```

`credit_balance` on the user doc is a cache, recomputed from summing the ledger. If they ever disagree, the ledger wins — this is what makes disputes and audits possible.

## Reserve → commit → release pattern

The core problem: a user's request goes to a slow provider call, and in that window the same user (or a race from a retry) could fire a second request past their real balance. Fix with a two-phase deduction:

```python
async def generate_with_billing(user_id: str, job_spec: dict):
    cost = CREDIT_COSTS[(job_spec["model"], job_spec["resolution"])]

    # Phase 1: reserve — atomic, fails if insufficient balance
    reserved = await db.users.find_one_and_update(
        {"_id": user_id, "credit_balance": {"$gte": cost}},
        {"$inc": {"credit_balance": -cost}},
    )
    if not reserved:
        raise InsufficientCreditsError(required=cost)

    await db.credit_transactions.insert_one({
        "user_id": user_id, "type": "reserve", "amount": -cost,
        "job_id": job_spec["job_id"], "created_at": now(),
    })

    try:
        result = await call_model(job_spec)   # api-calling.md
    except Exception:
        # Phase 2a: release — refund the reservation, no charge
        await db.users.update_one({"_id": user_id}, {"$inc": {"credit_balance": cost}})
        await db.credit_transactions.insert_one({
            "user_id": user_id, "type": "release", "amount": cost,
            "job_id": job_spec["job_id"], "created_at": now(),
        })
        raise

    # Phase 2b: commit — reservation becomes a real charge, nothing more to do
    await db.credit_transactions.insert_one({
        "user_id": user_id, "type": "commit", "amount": 0,   # already deducted at reserve
        "job_id": job_spec["job_id"], "created_at": now(),
    })
    return result
```

The `$gte` filter on the reserve step makes it atomic at the database level — two concurrent requests can't both succeed past the balance, MongoDB's single-document atomicity handles the race.

## Idempotency on retries

Every generation request from the client must carry a client-generated `idempotency_key`. Before reserving credits, check if a job with that key already exists and is in-flight or completed — if so, return the existing job instead of creating a new reservation. This is what stops a flaky network retry from double-charging.

```python
existing = await db.generation_jobs.find_one({"idempotency_key": key})
if existing:
    return existing   # don't re-reserve
```

## Refunds

Automatic refund (credit back to `credit_balance`, `type: "refund"` ledger entry) on:
- Provider returns an error / batch job item fails
- Content policy rejection (prompt blocked before generation happens — never even reserve in this case, reject at validation)
- Timeout past your own SLA (e.g. batch job stuck >48h)

Never auto-refund on: user simply dislikes the output. That's a support/discretionary path, not an automatic system rule.

## Grants and renewal

- Monthly renewal: `type: "grant"`, amount = tier's credit allotment, on the subscription's billing anniversary (drive this off your payment processor's webhook, not a cron guess). Since you're running Razorpay for domestic (UPI/cards/netbanking) and possibly Stripe for international cards, tag every grant with `source: "razorpay"` or `source: "stripe"` — the ledger stays a single unified currency either way, but the tag is what lets you reconcile "credits granted" against "payments received" per provider when the two webhook payloads don't line up.
- **No rollover** by default — simplest to reason about and matches the Higgsfield-style breakage assumption in `pricing-tier.md`. If you want rollover later, cap it (e.g. max 1 month's worth) so it doesn't become unlimited banking.
- Top-up / pay-as-you-go credits (optional): separate `type: "grant"` with a `source: "purchase"` tag so you can distinguish subscription credits from purchased ones if you ever want different expiry rules between them.

## Low-balance handling

- Soft warning at 20% remaining (in-app banner, not blocking)
- Hard block at 0 — the `$gte` check above already enforces this at the data layer, so there's no code path where a request can succeed without sufficient balance
- Never let client-side code decide whether a user "has enough credits" — that check has to happen server-side at reservation time, every time

## Audit requirements

- Ledger entries are immutable — never update or delete a `credit_transactions` row, only insert new offsetting entries
- Sum of ledger for any user should always equal their cached `credit_balance` — run a periodic reconciliation job (nightly) that flags drift
- Retain the ledger indefinitely (or per your data retention policy) — this is your source of truth if a billing dispute ever comes up