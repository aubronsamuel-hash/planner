# Worker Reference – Planner Blueprint v3.2

## Task Catalogue

| Function | Description | Metrics | Notes |
|----------|-------------|---------|-------|
| `send_email(to, subject, content)` | Simulated transactional email dispatch. | `rq_jobs_total`, `rq_job_duration_seconds` | Returns payload echo for audit trails. |
| `generate_timesheet_report(user_id)` | Produces an offline PDF path for the given user. | `rq_jobs_total`, `rq_job_duration_seconds` | Future versions will render actual reports. |
| `aggregate_metrics()` | Aggregates analytical counters for dashboards. | `rq_jobs_total`, `rq_job_duration_seconds` | Used by Prometheus export to cross-check. |

All tasks are decorated by `instrument_task`, which increments
`rq_jobs_total{task}` and `rq_failures_total{task}` and records job durations.
Failures raise their original exception for upstream retry policies.

## Running the Worker

### Python Module
```bash
python -m backend.app.worker.main --queue planner
```

### Docker Compose
The worker service is defined in `infra/compose/docker-compose.dev.yml` and is
started automatically by `make monitoring`. Environment variables:

- `PLANNER_REDIS_URL` – Redis connection string (supports `fakeredis://`).
- `PLANNER_WORKER_METRICS_PORT` – defaults to `9000`.
- `PLANNER_LOKI_URL` – optional Loki push endpoint.

## Metrics Endpoint
An embedded HTTP server (port 9000) serves `/metrics`. The response includes the
three counters required by Phase 3.2 plus duration histograms.

## Testing Guidance
- `pytest backend/tests/test_worker_tasks.py` exercises instrumentation logic.
- `pytest backend/tests/test_worker_queue.py` spins a fakeredis queue and runs the
  worker in burst mode to assert job execution.
- GitHub Actions workflow `ci/test_worker.yml` gates pull requests on worker
  health.

## Future Extensions
- Add SMTP integration (per IRS §7.2) for `send_email`.
- Introduce PDF rendering for `generate_timesheet_report` using WeasyPrint.
- Push Prometheus counters to Alertmanager for proactive failure alerts.
