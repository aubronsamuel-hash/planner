# Planner Blueprint v3.2 – Worker + Monitoring

Phase 3.2 activates the asynchronous worker stack and observability pipeline
required by the TRS/IRS specifications. The repository now packages a Redis RQ
worker, Prometheus metrics for both backend and worker services, and a
Grafana/Loki monitoring toolkit.

## Quickstart
1. `make bootstrap`
2. `make up`
3. `make monitoring` to launch Prometheus, Grafana, Loki, and the worker.
4. Visit `http://localhost:5173` for the frontend placeholder.
5. Query `http://localhost:8000/api/v1/health` for the backend health check.
6. Scrape metrics via `http://localhost:8000/metrics` and
   `http://localhost:9000/metrics`.

> ℹ️ Grafana is exposed on `http://localhost:3000` with default credentials
> `admin` / `admin`. Import `infra/docker/grafana/dashboards/planner-overview.json`
> to display backend throughput, worker activity, and Loki log streams.

Refer to `docs/INDEX_v3.md` and `codex_roadmap_v4.md` for the full delivery
context.

## Observability Highlights
- Prometheus counters, gauges, and histograms provide visibility into HTTP
  traffic and worker job throughput.
- Grafana is pre-provisioned with Prometheus and Loki datasources plus a
  dashboard template that correlates worker performance with API load.
- Loki ingestion is wired through an optional HTTP handler activated via the
  `PLANNER_LOKI_URL` environment variable. Both backend and worker containers
  automatically push logs when the variable is set.

## Authentication Highlights
- Passwords are normalized with SHA-256 before bcrypt hashing, satisfying the
  security constraints from the SRS and preventing bcrypt truncation issues.
- Access tokens include a unique JTI stored in Redis with a TTL that matches
  the token lifetime, ensuring automatic cleanup of revoked tokens and
  alignment with the Redis cache requirements.
