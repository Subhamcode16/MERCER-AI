# API Calling Guide

Covers request shape per model, standard vs batch routing, and how calls tie back to the credit ledger in `pricing-tier.md`.

## Routing logic (tier → model → mode)

```python
def resolve_call_params(tier: str, model: str, urgent: bool = False):
    """
    Returns (mode, resolution) given the user's tier and requested model.
    mode: "standard" | "batch"
    """
    if model == "nano_banana_pro":
        if tier == "starter":
            return "standard", "1024"          # preview-only, no batch, no 4K
        if tier == "pro":
            return "standard", "2048"
        if tier == "studio":
            return ("standard" if urgent else "batch"), "2048"

    if model == "nano_banana_2":
        return "standard", "1024" if tier == "starter" else "2048"

    if model == "gpt_image_2":
        quality = "low" if tier == "starter" else "medium"
        return "standard", quality

    raise ValueError(f"unknown model: {model}")
```

## GPT Image 2

```python
response = client.images.generate(
    model="gpt-image-2",
    prompt=prompt,
    size="1024x1024",          # or 1024x1536 / 1536x1024 — slightly cheaper at medium/high
    quality="low" | "medium" | "high",
)
image_b64 = response.data[0].b64_json
```

- No separate batch endpoint call shape — use OpenAI's Batch API (JSONL file upload + `client.batches.create()`) for non-real-time jobs; 50% off input/output tokens.
- Edits (reference images) always bill high-fidelity input tokens regardless of `quality` — don't offer edit flows on Starter tier without a separate, higher credit cost.

## Nano Banana Pro / Nano Banana 2

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",   # or "gemini-3.1-flash-image" for NB2
    contents=[prompt],
    config={"response_modalities": ["IMAGE"]},   # image-only saves output tokens vs default ["TEXT","IMAGE"]
)
image_bytes = response.candidates[0].content.parts[0].inline_data.data
```

- Set `response_modalities: ["IMAGE"]` explicitly — the default also returns text tokens you don't need, and pay for.
- For Batch mode, use the Gemini Batch API (async job submission) — same request shape, submitted via batch endpoint, ~50% discount on both routes.
- Reference images: up to 14 for Pro. Each adds ~$0.0011 (negligible) — don't gate this on credits separately, it's inside the flat per-gen cost already used in the tier table.

## Credit deduction — wrap every call

```python
CREDIT_COSTS = {
    ("nano_banana_2", "1024"): 2,
    ("nano_banana_2", "2048"): 2,
    ("gpt_image_2", "low"): 1,
    ("gpt_image_2", "medium"): 2,
    ("nano_banana_pro", "1024"): 3,
    ("nano_banana_pro", "2048"): 4,
}

async def generate_with_billing(user_id: str, tier: str, model: str, prompt: str, urgent: bool = False):
    mode, resolution = resolve_call_params(tier, model, urgent)
    cost = CREDIT_COSTS[(model, resolution)]

    if not await has_sufficient_credits(user_id, cost):
        raise InsufficientCreditsError(required=cost)

    result = await call_model(model, mode, resolution, prompt)   # dispatch to the two functions above
    await deduct_credits(user_id, cost)                          # only deduct on success
    return result
```

**Key rule: deduct only on a successful, billable generation.** Both OpenAI and Gemini only charge for completed generations — mirror that in your ledger so failed calls don't cost the user credits.

## Batch job lifecycle (Studio tier default for Nano Banana Pro)

1. Queue eligible requests (non-`urgent`) into a nightly batch instead of calling standard endpoint per-request
2. Submit as one batch job per provider per run
3. Poll or webhook for completion
4. Deduct credits and deliver results once the batch resolves — surface an in-app "generating" state rather than blocking the user's session

## Monitoring

- Log cost-per-call (provider's actual billed tokens, not your credit price) separately from credit deductions — this is how you'll catch margin drift if Google/OpenAI change rates
- Alert if any tier's actual-cost-to-credit ratio drifts more than ~15% from the targets in `pricing-tier.md`
