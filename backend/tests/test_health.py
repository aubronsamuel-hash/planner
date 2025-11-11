"""Smoke tests for the FastAPI application without relying on httpx."""
import anyio

from backend.app.main import create_app


def test_health_endpoint_returns_ok() -> None:
    app = create_app()
    route = next(route for route in app.router.routes if getattr(route, "path", None) == "/api/v1/health")
    result = anyio.run(route.endpoint)
    assert result == {"status": "ok"}
