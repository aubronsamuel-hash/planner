"""Application factory for the Planner backend."""
from __future__ import annotations

from fastapi import FastAPI, Response

from .api.routes import auth, dashboard, missions, timesheets
from .core.logging import configure_logging
from .core.metrics import metrics_middleware, metrics_response


def create_app() -> FastAPI:
    configure_logging("planner-backend")
    app = FastAPI(title="Planner Backend", version="0.3.0")

    app.middleware("http")(metrics_middleware)

    @app.get("/api/v1/health", tags=["health"])  # pragma: no cover - simple wiring
    async def health() -> dict[str, str]:
        """Lightweight readiness probe used by smoke tests."""

        return {"status": "ok"}

    @app.get("/metrics", include_in_schema=False, tags=["monitoring"])
    async def metrics() -> Response:  # pragma: no cover - exercised in tests
        return metrics_response()

    app.include_router(auth.router)
    app.include_router(missions.router)
    app.include_router(timesheets.router)
    app.include_router(dashboard.router)

    return app


app = create_app()
