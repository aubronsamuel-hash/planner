"""Tests for Prometheus instrumentation on the backend."""
import pytest


@pytest.mark.asyncio
async def test_metrics_endpoint_exposes_counters(client) -> None:
    await client.get("/api/v1/health")
    response = await client.get("/metrics")
    assert response.status_code == 200
    body = response.text
    assert "planner_http_requests_total" in body
    assert "planner_http_request_duration_seconds" in body
    assert "planner_http_requests_in_progress" in body
