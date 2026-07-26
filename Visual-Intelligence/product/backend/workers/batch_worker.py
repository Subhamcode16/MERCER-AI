"""
Mercer AI — Batch Worker (Phase 5 stub)

Supervisor-managed process running alongside the FastAPI app.
Polls MongoDB every 15-30 minutes for non-urgent queued jobs,
groups by provider, submits to OpenAI or Gemini Batch APIs,
polls for results, delivers to Cloudflare R2, and pushes
completion notifications to clients.

Status: STUB — Full implementation in Phase 5.
"""
import asyncio
import logging
import os
import sys

# Allow imports from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.logging import setup_logging

setup_logging()
logger = logging.getLogger("batch_worker")


async def batch_worker_loop() -> None:
    """
    Main loop — runs continuously, wakes on the rolling window interval.
    Phase 5 implementation will:
      1. Query generation_jobs where status="queued" and urgent=False
      2. Group by provider (openai | gemini)
      3. Submit each group as a batch job
      4. Poll open batches for completion
      5. Deliver results to R2 and notify clients
    """
    logger.info("Batch worker started. Awaiting Phase 5 implementation.")
    interval = int(os.getenv("BATCH_WORKER_INTERVAL_SECONDS", "900"))  # 15 min default

    while True:
        logger.info("Batch worker tick — interval=%ds", interval)
        # Phase 5: replace this with actual batch logic
        await asyncio.sleep(interval)


if __name__ == "__main__":
    asyncio.run(batch_worker_loop())
