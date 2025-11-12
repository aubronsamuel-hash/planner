"""Integration test ensuring the worker can execute jobs using fakeredis."""
from __future__ import annotations

from fakeredis import FakeStrictRedis
from rq import Queue
from rq.worker import SimpleWorker
import pytest

from backend.app.worker import tasks


def test_worker_executes_send_email(monkeypatch) -> None:
    monkeypatch.setattr(tasks.time, "sleep", lambda *_: None)
    monkeypatch.setattr(tasks.random, "uniform", lambda *_: 0.2)
    before = tasks.registry().get_sample_value("rq_jobs_total", {"task": "send_email"}) or 0.0
    connection = FakeStrictRedis()
    queue = Queue("planner", connection=connection)
    job = queue.enqueue(tasks.send_email, "alice@example.com", "Greetings", "Payload")
    worker = SimpleWorker([queue], connection=connection)
    worker.work(burst=True)
    assert queue.count == 0
    after = tasks.registry().get_sample_value("rq_jobs_total", {"task": "send_email"}) or 0.0
    assert after == pytest.approx(before + 1)
