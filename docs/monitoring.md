# Monitoring Stack – Planner Blueprint v3.2

## Overview
Phase 3.2 introduces a full observability loop covering:

- **Prometheus** scraping backend (`:8000/metrics`) and worker (`:9000/metrics`).
- **Grafana** with pre-provisioned dashboards and datasources.
- **Loki** log aggregation through the optional `PLANNER_LOKI_URL` sink.

The stack is deployed via Docker Compose (`make monitoring`). Prometheus uses
`infra/docker/prometheus/prometheus.yml` and Grafana automatically loads
`infra/docker/grafana/dashboards/planner-overview.json`.

## Local Execution
```bash
make up
make monitoring
```

Services:

| Component   | URL                         | Notes                                   |
|-------------|-----------------------------|-----------------------------------------|
| Backend     | http://localhost:8000       | `/metrics` includes request counters    |
| Worker      | http://localhost:9000       | `/metrics` exposes RQ job metrics       |
| Prometheus  | http://localhost:9090       | Targets `planner-backend` & `planner-worker` |
| Grafana     | http://localhost:3000       | Credentials `admin` / `admin`           |
| Loki API    | http://localhost:3100       | Receives JSON log batches               |

## Metrics Reference

### Backend
- `planner_http_requests_total{method, path}` – request counter.
- `planner_http_request_duration_seconds{method, path}` – response latency histogram.
- `planner_http_requests_in_progress` – gauge of concurrent requests.

### Worker
- `rq_jobs_total{task}` – total RQ jobs (success & failure).
- `rq_failures_total{task}` – failed jobs.
- `rq_job_duration_seconds{task}` – duration histogram.

## Loki Integration
Set `PLANNER_LOKI_URL` (e.g. `http://loki:3100/loki/api/v1/push`) to enable the
Loki handler for both backend and worker. Logs are tagged with `service` to
match the Grafana dashboard queries.

## Troubleshooting
- Metrics return 404 → ensure worker command publishes metrics (`python -m backend.app.worker.main`).
- Grafana dashboards empty → check Prometheus targets under Status → Targets.
- Logs missing in Loki → confirm `PLANNER_LOKI_URL` is configured and that the
  Grafana Loki datasource reports “Data source is working”.

## CI/CD Hooks
The `deploy.yml` workflow uploads a sample Prometheus scrape via `curl`.
`ci/test_worker.yml` executes the `send_email` job against a fakeredis queue to
ensure RQ wiring remains functional.
