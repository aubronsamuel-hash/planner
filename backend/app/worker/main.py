"""Entrypoint for running the Planner RQ worker."""
from __future__ import annotations

import argparse
import logging
import os
import signal
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Iterable

import redis
from rq import Connection, Queue, Worker

from backend.app.core.config import get_settings
from backend.app.core.logging import configure_logging

from .tasks import registry

LOGGER = logging.getLogger("planner.worker")


class _MetricsRequestHandler(BaseHTTPRequestHandler):
    """Serve the Prometheus metrics collected by worker tasks."""

    def do_GET(self) -> None:  # noqa: N802  # pragma: no cover - exercised via integration tests
        from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return
        payload = generate_latest(registry())
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPE_LATEST)
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003 - BaseHTTPRequestHandler API
        LOGGER.debug("metrics: " + format, *args)


def _serve_metrics(port: int) -> HTTPServer:
    server = HTTPServer(("0.0.0.0", port), _MetricsRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    LOGGER.info("Metrics server started", extra={"port": port})
    return server


def _build_connection(url: str) -> redis.Redis:
    if url.startswith("fakeredis://"):
        from fakeredis import FakeStrictRedis

        return FakeStrictRedis()
    return redis.from_url(url)


def _parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Planner RQ worker")
    parser.add_argument("--burst", action="store_true", help="Run worker in burst mode")
    parser.add_argument("--queue", action="append", dest="queues", default=["planner"], help="Queue name")
    parser.add_argument(
        "--metrics-port",
        type=int,
        default=int(os.getenv("PLANNER_WORKER_METRICS_PORT", "9000")),
        help="Port exposed for Prometheus metrics",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    configure_logging("planner-worker")
    args = _parse_args(argv)
    settings = get_settings()
    redis_url = settings.redis_url
    connection = _build_connection(redis_url)
    metrics_server = _serve_metrics(args.metrics_port)

    def _signal_handler(signum: int, frame: object | None) -> None:  # pragma: no cover - signal wiring
        LOGGER.info("Received shutdown signal", extra={"signal": signum})
        metrics_server.shutdown()

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    with Connection(connection):
        queues = [Queue(name, connection=connection) for name in args.queues]
        worker = Worker(queues, name="planner-worker")
        LOGGER.info(
            "Worker starting",
            extra={"queues": args.queues, "redis_url": redis_url, "burst": args.burst},
        )
        worker.work(burst=args.burst)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
