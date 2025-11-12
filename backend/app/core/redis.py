"""Utilities to obtain a shared Redis connection."""
from __future__ import annotations

from typing import Optional

from redis.asyncio import Redis

from .config import get_settings

try:  # pragma: no cover - optional fallback for local tests
    from fakeredis.aioredis import FakeRedis  # type: ignore
except Exception:  # pragma: no cover - fakeredis is optional
    FakeRedis = None  # type: ignore

_redis: Optional[Redis] = None


def _build_client(url: str) -> Redis:
    if url.startswith("fakeredis://"):
        if FakeRedis is None:  # pragma: no cover - developer feedback
            raise RuntimeError(
                "fakeredis:// URL requested but fakeredis is not installed."
            )
        return FakeRedis()  # type: ignore[return-value]
    return Redis.from_url(url, decode_responses=False, encoding=None)


def get_redis() -> Redis:
    """Return a singleton Redis client instance."""

    global _redis
    if _redis is None:
        settings = get_settings()
        _redis = _build_client(settings.redis_url)
    return _redis


async def ensure_redis() -> Redis:
    """Verify the Redis connection is alive, recreating it if needed."""

    global _redis
    client = get_redis()
    try:
        await client.ping()
    except Exception:  # pragma: no cover - reinitialisation path
        settings = get_settings()
        _redis = _build_client(settings.redis_url)
        client = _redis
    return client


async def set_with_ttl(key: str, value: bytes | str, ttl_seconds: int) -> None:
    """Store ``value`` with a TTL and auto-expire semantics."""

    client = await ensure_redis()
    ttl = max(ttl_seconds, 1)
    await client.set(key, value, ex=ttl)


async def delete_key(key: str) -> None:
    """Remove ``key`` from Redis if it exists."""

    client = await ensure_redis()
    await client.delete(key)


async def close_redis() -> None:
    """Close the global Redis connection."""

    global _redis
    if _redis is not None:
        await _redis.close()
        _redis = None


__all__ = [
    "close_redis",
    "delete_key",
    "ensure_redis",
    "get_redis",
    "set_with_ttl",
]
