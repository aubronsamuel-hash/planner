"""Unit tests for the RQ task layer."""
from __future__ import annotations

import pytest

from backend.app.worker import tasks


def _metric(name: str, labels: dict[str, str]) -> float:
    value = tasks.registry().get_sample_value(name, labels)  # type: ignore[arg-type]
    return float(value or 0.0)


@pytest.fixture(autouse=True)
def _fast_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tasks.time, "sleep", lambda *_: None)


@pytest.mark.parametrize("uniform_value", [0.123])
def test_send_email_increments_counters(monkeypatch: pytest.MonkeyPatch, uniform_value: float) -> None:
    monkeypatch.setattr(tasks.random, "uniform", lambda *_: uniform_value)
    baseline = _metric("rq_jobs_total", {"task": "send_email"})
    response = tasks.send_email("ops@example.com", "Subject", "Body")
    assert response["status"] == "sent"
    assert _metric("rq_jobs_total", {"task": "send_email"}) == pytest.approx(baseline + 1)
    assert _metric("rq_failures_total", {"task": "send_email"}) == pytest.approx(0.0)


def test_instrument_task_records_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tasks.random, "uniform", lambda *_: 0.1)

    @tasks.instrument_task
    def failing_task() -> None:
        raise RuntimeError("boom")

    baseline = _metric("rq_failures_total", {"task": "failing_task"})
    with pytest.raises(RuntimeError):
        failing_task()
    assert _metric("rq_failures_total", {"task": "failing_task"}) == pytest.approx(baseline + 1)
