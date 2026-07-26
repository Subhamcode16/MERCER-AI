"""
Mercer AI — Generation Routes

Handles image generation requests, routing them to the appropriate provider
while enforcing the two-phase credit deduction system (Reserve -> Commit/Refund).
"""
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from app.auth import AuthenticatedUser, require_verified_email
from app.database import get_db
from app.models.generation import GenerationRequest, GenerationResponse, JobStatus, CREDIT_COSTS
from app.services.billing import reserve_credits, commit_credits, refund_credits, InsufficientCreditsError
from app.services.provider_gemini import generate_nano_banana_2

from opentelemetry import trace
tracer = trace.get_tracer(__name__)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/generate", tags=["generation"])


async def process_generation_job(job_id: str, prompt: str, user_id: str, cost: int):
    """
    Background worker that runs the image generation and updates the DB.
    """
    with tracer.start_as_current_span("process_generation_job") as span:
        span.set_attribute("job_id", job_id)
        span.set_attribute("user_id", user_id)
        span.set_attribute("model", "nano_banana_2")
        
        start_time = datetime.now(timezone.utc)
        db = get_db()
        
        # 1. Mark as processing
        await db.jobs.update_one(
            {"_id": job_id},
            {"$set": {"status": JobStatus.processing.value, "updated_at": datetime.now(timezone.utc)}}
        )
        
        try:
            # 2. Call API
            with tracer.start_as_current_span("provider_call"):
                b64_image = await generate_nano_banana_2(prompt)
            
            # 3. Phase 2a: Commit Credits
            await commit_credits(db, user_id, job_id)
            
            # 4. Mark completed
            end_time = datetime.now(timezone.utc)
            latency_ms = int((end_time - start_time).total_seconds() * 1000)
            span.set_attribute("latency_ms", latency_ms)
            
            await db.jobs.update_one(
                {"_id": job_id},
                {"$set": {
                    "status": JobStatus.completed.value,
                    "image_base64": b64_image,
                    "updated_at": end_time,
                    "latency_ms": latency_ms
                }}
            )
            logger.info("Generation job %s completed successfully in %d ms", job_id, latency_ms)
        except Exception as e:
            end_time = datetime.now(timezone.utc)
            latency_ms = int((end_time - start_time).total_seconds() * 1000)
            
            span.record_exception(e)
            span.set_status(trace.StatusCode.ERROR, str(e))
            span.set_attribute("latency_ms", latency_ms)
            
            logger.error(
                "Generation job %s failed after %d ms: %s", 
                job_id, latency_ms, e,
                exc_info=True
            )
            # Phase 2b: Refund Credits
            await refund_credits(db, user_id, cost, job_id, reason="provider_error")
            await db.jobs.update_one(
                {"_id": job_id},
                {"$set": {
                    "status": JobStatus.failed.value,
                    "error": str(e),
                    "updated_at": end_time,
                    "latency_ms": latency_ms
                }}
            )

@router.post("/nano_banana_2", response_model=GenerationResponse, summary="Generate image with Nano Banana 2")
async def generate_image_nb2(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    user: AuthenticatedUser = Depends(require_verified_email),
):
    """
    Submit an image generation job for Nano Banana 2 (Gemini 3.1 Flash Image).
    Reserves credits and queues a BackgroundTask. Returns job_id.
    """
    db = get_db()
    cost = CREDIT_COSTS["nano_banana_2"]
    
    # ── Idempotency Check ─────────────────────────────────────────────────────
    existing_tx = await db.credit_transactions.find_one({
        "user_id": user.user_id,
        "job_id": request.idempotency_key
    })
    if existing_tx:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A request with this idempotency key has already been processed."
        )

    # ── Phase 1: Reserve Credits ──────────────────────────────────────────────
    try:
        await reserve_credits(db, user.user_id, cost, request.idempotency_key)
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=e.detail)
        
    # ── Create Job DB Entry ───────────────────────────────────────────────────
    now = datetime.now(timezone.utc)
    job_doc = {
        "_id": request.idempotency_key,
        "user_id": user.user_id,
        "status": JobStatus.queued.value,
        "model": "nano_banana_2",
        "prompt": request.prompt,
        "image_base64": None,
        "error": None,
        "created_at": now,
        "updated_at": now,
    }
    await db.jobs.insert_one(job_doc)
    
    # ── Queue Background Task ─────────────────────────────────────────────────
    background_tasks.add_task(
        process_generation_job,
        job_id=request.idempotency_key,
        prompt=request.prompt,
        user_id=user.user_id,
        cost=cost
    )
    
    return GenerationResponse(
        status="ok",
        job_id=request.idempotency_key,
    )
