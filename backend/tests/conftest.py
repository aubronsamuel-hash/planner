"""Shared fixtures for backend tests."""
from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path
from typing import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient

from backend.app.core.config import get_settings
from backend.app.core.redis import close_redis, ensure_redis
from backend.app.db.session import dispose_engine
from backend.app.main import create_app

_TEST_DIR = Path(tempfile.mkdtemp(prefix="planner-tests-"))
_DB_URL = f"sqlite+aiosqlite:///{_TEST_DIR / 'planner.db'}"

os.environ.setdefault("PLANNER_DATABASE_URL", _DB_URL)
os.environ.setdefault("PLANNER_REDIS_URL", "fakeredis://")
os.environ.setdefault("PLANNER_JWT_SECRET", "test-secret")
os.environ.setdefault("PLANNER_ACCESS_TOKEN_MINUTES", "2")
os.environ.setdefault("PLANNER_REFRESH_TOKEN_MINUTES", "5")
get_settings.cache_clear()

_ALEMBIC_CFG = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
_ALEMBIC_CFG.set_main_option(
    "script_location", str(Path(__file__).resolve().parents[1] / "migrations")
)
_ALEMBIC_CFG.set_main_option("sqlalchemy.url", _DB_URL)
command.upgrade(_ALEMBIC_CFG, "head")


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _settings_guard() -> AsyncIterator[None]:
    try:
        yield
    finally:
        get_settings.cache_clear()
        await dispose_engine()
        await close_redis()


@pytest_asyncio.fixture(autouse=True)
async def _clear_redis() -> AsyncIterator[None]:
    client = await ensure_redis()
    await client.flushdb()
    yield


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
