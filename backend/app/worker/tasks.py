"""Business tasks executed by the Planner RQ worker."""
from __future__ import annotations

import logging
import random
import time
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

from prometheus_client import CollectorRegistry, Counter, Histogram

LOGGER = logging.getLogger("planner.worker")

_REGISTRY = CollectorRegistry()
RQ_JOBS_TOTAL = Counter(
    "rq_jobs_total",
    "Total number of RQ jobs executed by the worker",
    labelnames=("task",),
    registry=_REGISTRY,
)
RQ_FAILURES_TOTAL = Counter(
    "rq_failures_total",
    "Total number of failed RQ jobs",
    labelnames=("task",),
    registry=_REGISTRY,
)
RQ_JOB_DURATION_SECONDS = Histogram(
    "rq_job_duration_seconds",
    "Execution duration of RQ jobs",
    labelnames=("task",),
    registry=_REGISTRY,
)

P = ParamSpec("P")
R = TypeVar("R")


def instrument_task(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator registering Prometheus counters for a given task."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        task_name = func.__name__
        start = time.perf_counter()
        LOGGER.info("Starting task", extra={"task": task_name})
        try:
            result = func(*args, **kwargs)
        except Exception:
            elapsed = time.perf_counter() - start
            RQ_JOBS_TOTAL.labels(task=task_name).inc()
            RQ_JOB_DURATION_SECONDS.labels(task=task_name).observe(elapsed)
            RQ_FAILURES_TOTAL.labels(task=task_name).inc()
            LOGGER.exception("Task failed", extra={"task": task_name})
            raise
        else:
            RQ_JOBS_TOTAL.labels(task=task_name).inc()
            elapsed = time.perf_counter() - start
            RQ_JOB_DURATION_SECONDS.labels(task=task_name).observe(elapsed)
            LOGGER.info(
                "Completed task",
                extra={"task": task_name, "duration_seconds": round(elapsed, 4)},
            )
            return result

    return wrapper


@instrument_task
def send_email(to: str, subject: str, content: str) -> dict[str, Any]:
    """Simulate sending an email notification."""

    # The implementation is mocked for blueprint purposes.
    simulated_latency = random.uniform(0.05, 0.2)
    time.sleep(simulated_latency)
    payload = {"to": to, "subject": subject, "content": content}
    LOGGER.debug("Email payload", extra={"payload": payload})
    return {"status": "sent", "latency": simulated_latency, "payload": payload}


@instrument_task
def generate_timesheet_report(user_id: int) -> dict[str, Any]:
    """Simulate report generation for a user's weekly timesheet."""

    simulated_latency = random.uniform(0.1, 0.35)
    time.sleep(simulated_latency)
    report_path = f"/tmp/timesheet-{user_id}.pdf"
    LOGGER.debug(
        "Generated timesheet report",
        extra={"user_id": user_id, "path": report_path},
    )
    return {"status": "generated", "path": report_path, "latency": simulated_latency}


@instrument_task
def aggregate_metrics() -> dict[str, Any]:
    """Aggregate system metrics, returning the outcome."""

    simulated_latency = random.uniform(0.05, 0.15)
    time.sleep(simulated_latency)
    statistics = {
        "active_users": random.randint(5, 50),
        "missions_in_progress": random.randint(1, 20),
        "alerts_open": random.randint(0, 3),
    }
    LOGGER.debug("Aggregated metrics", extra={"statistics": statistics})
    return {"status": "aggregated", "latency": simulated_latency, "statistics": statistics}


def registry() -> CollectorRegistry:
    """Expose the registry used by worker metrics for reuse by servers/tests."""

    return _REGISTRY


__all__ = [
    "RQ_FAILURES_TOTAL",
    "RQ_JOB_DURATION_SECONDS",
    "RQ_JOBS_TOTAL",
    "aggregate_metrics",
    "generate_timesheet_report",
    "instrument_task",
    "registry",
    "send_email",
]
