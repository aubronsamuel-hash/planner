"""Application factory for the Planner backend."""
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Planner Backend", version="0.1.0")

    @app.get("/api/v1/health", tags=["health"])  # pragma: no cover - simple wiring
    async def health() -> dict[str, str]:
        """Lightweight readiness probe used by smoke tests."""
        return {"status": "ok"}

    return app


app = create_app()
