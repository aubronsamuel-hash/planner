"""Prometheus metrics utilities shared across the backend stack."""
from __future__ import annotations

import time
from typing import Awaitable, Callable

from fastapi import Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

REGISTRY = CollectorRegistry()

REQUEST_COUNT = Counter(
    "planner_http_requests_total",
    "Total number of HTTP requests processed by the backend",
    labelnames=("method", "path"),
    registry=REGISTRY,
)
REQUEST_DURATION = Histogram(
    "planner_http_request_duration_seconds",
    "Histogram of HTTP request durations",
    labelnames=("method", "path"),
    registry=REGISTRY,
)
ACTIVE_REQUESTS = Gauge(
    "planner_http_requests_in_progress",
    "Number of HTTP requests currently being served",
    registry=REGISTRY,
)

EXCLUDED_PATHS = {"/metrics"}


async def metrics_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Collect Prometheus metrics for each handled request."""

    path = request.url.path
    if path in EXCLUDED_PATHS:
        return await call_next(request)

    method = request.method
    start_time = time.perf_counter()
    ACTIVE_REQUESTS.inc()
    try:
        response = await call_next(request)
    finally:
        ACTIVE_REQUESTS.dec()
    duration = time.perf_counter() - start_time
    REQUEST_COUNT.labels(method=method, path=path).inc()
    REQUEST_DURATION.labels(method=method, path=path).observe(duration)
    return response


def metrics_response() -> Response:
    """Return the aggregated Prometheus metrics response."""

    payload = generate_latest(REGISTRY)
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)


__all__ = [
    "REGISTRY",
    "ACTIVE_REQUESTS",
    "REQUEST_COUNT",
    "REQUEST_DURATION",
    "metrics_middleware",
    "metrics_response",
]
