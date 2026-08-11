import json
import logging
from functools import wraps
from typing import Any, Callable, Optional
import redis.asyncio as redis
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class InMemoryPubSub:
    """Lightweight in-memory Pub/Sub system for when Redis is unavailable."""
    def __init__(self):
        import asyncio
        self._subscribers = {}
        self._lock = asyncio.Lock()

    def subscribe(self, channel: str):
        import asyncio
        queue = asyncio.Queue()
        if channel not in self._subscribers:
            self._subscribers[channel] = set()
        self._subscribers[channel].add(queue)
        return queue

    def unsubscribe(self, channel: str, queue):
        if channel in self._subscribers:
            self._subscribers[channel].discard(queue)
            if not self._subscribers[channel]:
                del self._subscribers[channel]

    async def publish(self, channel: str, message: str):
        if channel in self._subscribers:
            for queue in list(self._subscribers[channel]):
                await queue.put(message)

in_memory_pubsub = InMemoryPubSub()
redis_client: Optional[redis.Redis] = None

async def init_redis():
    """Initializes the Redis connection pool."""
    global redis_client
    try:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        # Test connection
        await redis_client.ping()
        logger.info(f"Connected to Redis at {settings.redis_url}")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        redis_client = None

async def close_redis():
    """Closes the Redis connection pool."""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Closed Redis connection.")
        redis_client = None

def get_redis() -> Optional[redis.Redis]:
    """Returns the current Redis client instance."""
    return redis_client

def cache_response(ttl: int = 3600):
    """
    A decorator that caches the result of an async function in Redis.
    The cache key is generated from the function name and its arguments.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not redis_client:
                # If Redis is unavailable, bypass the cache and run the function
                return await func(*args, **kwargs)

            # Generate a simple cache key (can be improved for complex objects)
            key_parts = [func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
            cache_key = "cache:" + ":".join(key_parts)

            try:
                cached_val = await redis_client.get(cache_key)
                if cached_val:
                    return json.loads(cached_val)
            except Exception as e:
                logger.warning(f"Redis get error for {cache_key}: {e}")

            # Execute the actual function
            result = await func(*args, **kwargs)

            try:
                # Cache the result
                await redis_client.set(cache_key, json.dumps(result), ex=ttl)
            except Exception as e:
                logger.warning(f"Redis set error for {cache_key}: {e}")

            return result
        return wrapper
    return decorator
