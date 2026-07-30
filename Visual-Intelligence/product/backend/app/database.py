"""
Mercer AI — MongoDB Connection + Index Management

Uses Motor (async driver). All database access goes through get_db().
Indexes are created at startup via _ensure_indexes() — idempotent, safe to re-run.
"""
import logging
from typing import Optional

import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
_db: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None


async def connect_db() -> None:
    global _client, _db
    _client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=5000,
    )
    _db = _client[settings.mongodb_db_name]
    await _client.admin.command("ping")   # fail fast if unreachable
    await _ensure_indexes()
    logger.info("MongoDB indexes verified.")


async def close_db() -> None:
    global _client
    if _client:
        _client.close()
        _client = None


def get_db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    """
    Return the database handle.
    Call this inside route handlers — no async needed for the getter itself.
    """
    if _db is None:
        raise RuntimeError("Database not initialised. Call connect_db() first.")
    return _db


async def _ensure_indexes() -> None:
    """
    Idempotent index creation.
    All indexes are documented here — this is the single source of truth
    for MongoDB index strategy.
    """
    db = get_db()

    # ── users ─────────────────────────────────────────────────────────────────
    # Primary key is _id (Supabase UUID string) — already indexed by MongoDB.
    await db.users.create_index([("email", ASCENDING)], unique=True)
    await db.users.create_index([("tier", ASCENDING)])

    # ── credit_transactions (append-only ledger) ──────────────────────────────
    # Audit queries: all transactions for a user, newest first
    await db.credit_transactions.create_index(
        [("user_id", ASCENDING), ("created_at", DESCENDING)]
    )
    # Link transactions to jobs
    await db.credit_transactions.create_index([("job_id", ASCENDING)], sparse=True)
    # Webhook idempotency: no duplicate provider event grants
    await db.credit_transactions.create_index(
        [("provider_event_id", ASCENDING)],
        unique=True,
        sparse=True,
        name="idx_provider_event_id_unique",
    )

    # ── generation_jobs ───────────────────────────────────────────────────────
    # User's job history
    await db.generation_jobs.create_index(
        [("user_id", ASCENDING), ("created_at", DESCENDING)]
    )
    # Batch worker: find queued non-urgent jobs quickly
    await db.generation_jobs.create_index(
        [("status", ASCENDING), ("urgent", ASCENDING)]
    )
    # Poll open batches by provider_batch_id
    await db.generation_jobs.create_index(
        [("provider_batch_id", ASCENDING)], sparse=True
    )
    # Client idempotency: one job per idempotency_key
    await db.generation_jobs.create_index(
        [("idempotency_key", ASCENDING)],
        unique=True,
        sparse=True,
        name="idx_idempotency_key_unique",
    )

    # ── workspaces ────────────────────────────────────────────────────────────
    await db.workspaces.create_index([("owner_id", ASCENDING)])

    # ── brands ────────────────────────────────────────────────────────────────
    await db.brands.create_index([("workspace_id", ASCENDING)])

    # ── products ──────────────────────────────────────────────────────────────
    await db.products.create_index([("brand_id", ASCENDING)])
    await db.products.create_index([("domain", ASCENDING)])

    # ── knowledge_claims (LAW-001) ────────────────────────────────────────────
    await db.knowledge_claims.create_index([("subject", ASCENDING)])
    await db.knowledge_claims.create_index([("predicate", ASCENDING)])
    await db.knowledge_claims.create_index([("status", ASCENDING)])

    # ── graph_edges (ARC-001) ─────────────────────────────────────────────────
    await db.graph_edges.create_index([("source_id", ASCENDING)])
    await db.graph_edges.create_index([("target_id", ASCENDING)])
    await db.graph_edges.create_index([("edge_type", ASCENDING)])
