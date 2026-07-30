# Batch Processing Architecture

Covers how generation requests get queued, batched, submitted, and resolved — primarily for Studio-tier Nano Banana Pro calls (per `pricing-tier.md`), but the same pipeline works for any non-urgent request across all three models.

## Why a rolling window, not nightly

Provider batch APIs promise up to 24h turnaround, but you don't need to wait that long — and users won't tolerate a next-day delivery for "generate an image" UX. Submit accumulated non-urgent jobs on a **rolling window (every 15-30 min)** instead of once a day. You still get the ~50% discount; you just collect a smaller batch more often. Trade-off: smaller batches = slightly more per-job overhead, but the UX difference (minutes vs a day) is worth it.

## Infra choice

Your stack is Python/FastAPI/MongoDB/Docker/Supervisor — no need to add Redis/Celery just for this:

- **Queue**: a MongoDB collection (`generation_jobs`) acting as the job store. Status field drives state transitions.
- **Worker**: a separate Supervisor-managed process (`batch_worker.py`) running a loop — poll every N seconds for `status: "queued"` jobs, group by provider, submit as batch.
- **Scale-up path**: if job volume grows past what a single polling worker can handle, move to Celery + Redis or SQS. Don't build that until you actually need it.

## Job lifecycle

```
submitted → queued → batched → sent_to_provider → polling → completed | failed → credited | refunded → delivered
```

```python
# MongoDB document shape
{
    "_id": ObjectId(...),
    "user_id": "...",
    "model": "nano_banana_pro",
    "prompt": "...",
    "resolution": "2048",
    "urgent": False,
    "status": "queued",
    "credit_cost": 4,
    "provider_batch_id": None,     # set once submitted
    "created_at": datetime,
    "updated_at": datetime,
    "result_url": None,
    "error": None,
}
```

## Worker loop (simplified)

```python
async def batch_worker_loop():
    while True:
        pending = await db.generation_jobs.find(
            {"status": "queued", "urgent": False}
        ).to_list(length=500)

        by_provider = group_by(pending, key=lambda j: PROVIDER_MAP[j["model"]])

        for provider, jobs in by_provider.items():
            if jobs:
                batch_id = await submit_batch(provider, jobs)
                await db.generation_jobs.update_many(
                    {"_id": {"$in": [j["_id"] for j in jobs]}},
                    {"$set": {"status": "sent_to_provider", "provider_batch_id": batch_id}}
                )

        await poll_open_batches()
        await asyncio.sleep(60)   # tune to your rolling window
```

## OpenAI Batch API

```python
# 1. Build JSONL — one line per job
lines = [
    {
        "custom_id": str(job["_id"]),
        "method": "POST",
        "url": "/v1/images/generations",
        "body": {"model": "gpt-image-2", "prompt": job["prompt"], "quality": job["quality"], "size": job["size"]},
    }
    for job in jobs
]
file = client.files.create(file=jsonl_bytes(lines), purpose="batch")

# 2. Create batch
batch = client.batches.create(
    input_file_id=file.id,
    endpoint="/v1/images/generations",
    completion_window="24h",
)

# 3. Poll (worker loop, not blocking a request)
status = client.batches.retrieve(batch.id)
if status.status == "completed":
    output = client.files.content(status.output_file_id)
    # parse JSONL, match custom_id back to job _id
```

## Gemini Batch API

```python
# Submit
batch_job = client.batches.create(
    model="gemini-3-pro-image-preview",
    requests=[
        {"custom_id": str(job["_id"]), "contents": [job["prompt"]], "config": {"response_modalities": ["IMAGE"]}}
        for job in jobs
    ],
)

# Poll
result = client.batches.get(name=batch_job.name)
if result.state == "SUCCEEDED":
    for r in result.responses:
        # match r.custom_id back to job _id, extract inline_data
```

## Partial failures within a batch

Both providers return per-item results — one job in a batch failing doesn't fail the whole batch. Handle this explicitly:

```python
for item_result in output:
    job = jobs_by_id[item_result["custom_id"]]
    if item_result["status"] == "success":
        await deliver_and_credit(job, item_result["output"])
    else:
        await refund_credits(job)   # see credit-system.md
        await notify_user_of_failure(job)
```

## Urgent (real-time) path

Requests flagged `urgent=True` skip the queue entirely and hit the standard (non-batch) endpoint synchronously inside the request handler, same credit cost either way — batching is a cost-optimization on your side, not a user-facing pricing lever. See `api-calling.md` for the standard-call shape.

## Delivery

Once a batch job resolves, push a websocket/SSE event or poll-friendly status endpoint to the client — don't make the frontend guess. Store `result_url` (uploaded to S3/object storage) rather than the raw bytes in MongoDB.
