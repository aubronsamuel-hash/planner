"""Application factory for the Planner backend."""
from __future__ import annotations

from fastapi import FastAPI

from .api.routes import auth, dashboard, missions, timesheets


def create_app() -> FastAPI:
    app = FastAPI(title="Planner Backend", version="0.2.0")

    @app.get("/api/v1/health", tags=["health"])  # pragma: no cover - simple wiring
    async def health() -> dict[str, str]:
        """Lightweight readiness probe used by smoke tests."""

        return {"status": "ok"}

    app.include_router(auth.router)
    app.include_router(missions.router)
    app.include_router(timesheets.router)
    app.include_router(dashboard.router)

    return app


app = create_app()
