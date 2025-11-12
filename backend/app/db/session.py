"""Async SQLAlchemy session helpers."""
from __future__ import annotations

from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..core.config import get_settings

_async_engine: AsyncEngine | None = None
_async_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def _configure_engine() -> None:
    global _async_engine, _async_sessionmaker
    if _async_engine is None or _async_sessionmaker is None:
        settings = get_settings()
        _async_engine = create_async_engine(settings.database_url, future=True)
        _async_sessionmaker = async_sessionmaker(
            _async_engine, expire_on_commit=False, autoflush=False
        )


def get_engine() -> AsyncEngine:
    """Return the lazily configured async engine."""

    _configure_engine()
    assert _async_engine is not None  # for type checkers
    return _async_engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    """Return the lazily configured session factory."""

    _configure_engine()
    assert _async_sessionmaker is not None  # for type checkers
    return _async_sessionmaker


async def get_session() -> AsyncIterator[AsyncSession]:
    """Provide a FastAPI-compatible session dependency."""

    session_maker = get_session_maker()
    async with session_maker() as session:
        yield session


async def dispose_engine() -> None:
    """Dispose of the async engine (used by tests)."""

    global _async_engine
    if _async_engine is not None:
        await _async_engine.dispose()
        _async_engine = None


__all__ = [
    "dispose_engine",
    "get_engine",
    "get_session",
    "get_session_maker",
]
