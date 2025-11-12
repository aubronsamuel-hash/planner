"""Application settings used by Planner services."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    jwt_secret: str = "insecure-secret"
    jwt_algorithm: str = "HS256"
    access_token_expiry_minutes: int = 15
    refresh_token_expiry_minutes: int = 60 * 24
    database_url: str = "postgresql+asyncpg://planner:planner@localhost:5432/planner"
    redis_url: str = "redis://localhost:6379/0"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            jwt_secret=os.getenv("PLANNER_JWT_SECRET", cls.jwt_secret),
            jwt_algorithm=os.getenv("PLANNER_JWT_ALGORITHM", cls.jwt_algorithm),
            access_token_expiry_minutes=int(os.getenv("PLANNER_ACCESS_TOKEN_MINUTES", cls.access_token_expiry_minutes)),
            refresh_token_expiry_minutes=int(os.getenv("PLANNER_REFRESH_TOKEN_MINUTES", cls.refresh_token_expiry_minutes)),
            database_url=os.getenv("PLANNER_DATABASE_URL", cls.database_url),
            redis_url=os.getenv("PLANNER_REDIS_URL", cls.redis_url),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings.from_env()


__all__ = ["Settings", "get_settings"]
