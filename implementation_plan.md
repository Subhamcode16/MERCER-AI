# Phase 3: Image Generation Layer

This phase implements the core generation engine of Atelier OS. We will build the robust credit reservation system and integrate the Google GenAI SDK to call Nano Banana 2 (`gemini-3.1-flash-image`).

## User Review Required

> [!IMPORTANT]  
> Please review this plan. Upon your approval, I will execute these steps. Ensure that `GEMINI_API_KEY` is present in your `.env` file before we proceed.

## Open Questions

> [!WARNING]
> How would you like the generated images returned? 
> 1. Return the raw base64 string directly in the API response.
> 2. Upload to Supabase Storage and return a public URL. 
> 
> *Recommendation: Base64 is faster to implement right now for MVP testing, but Supabase Storage is better for production.*

## Proposed Changes

### `app/models/generation.py`
#### [NEW] [generation.py](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/backend/app/models/generation.py)
- Define Pydantic models for the generation request (`GenerationRequest`) requiring `prompt` and `idempotency_key`.
- Define a mapping of model names to credit costs (e.g., `nano_banana_2` costs 2 credits).

### `app/services/billing.py`
#### [NEW] [billing.py](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/backend/app/services/billing.py)
Implement the robust two-phase commit system described in the intelligence docs:
- **`reserve_credits(user_id, amount, job_id)`**: Uses atomic `$gte` MongoDB update to deduct credits and writes a `reserve` ledger entry.
- **`commit_credits(user_id, job_id)`**: Writes a `commit` ledger entry.
- **`refund_credits(user_id, amount, job_id)`**: Re-adds credits and writes a `refund` ledger entry (called in case of provider failure).

### `app/services/provider_gemini.py`
#### [NEW] [provider_gemini.py](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/backend/app/services/provider_gemini.py)
- Integrates `google-genai` SDK.
- Function `generate_nano_banana_2(prompt: str)` that calls the `gemini-3.1-flash-image` model and returns the resulting image data.
- Wraps API calls in robust `try/except` blocks to handle network timeouts and provider errors gracefully.

### `routers/generate.py`
#### [MODIFY] [generate.py](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/backend/app/routers/generate.py)
- Apply the `require_verified_email` dependency to gate unverified Free tier users.
- Implement the `POST /generate/nano_banana_2` endpoint.
- Stitch together the flow: 
  1. Check idempotency.
  2. Reserve credits.
  3. Call `generate_nano_banana_2`.
  4. Commit credits on success (or refund on failure).
  5. Return result.

## Verification Plan

### Automated Tests
1. Call endpoint without credits -> verify `402 Payment Required`.
2. Call endpoint with invalid prompt -> verify credits are refunded.
3. Call endpoint successfully -> verify 2 credits are deducted from MongoDB and image is returned.
