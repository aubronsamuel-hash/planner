# Codex Action Plan – Planner Blueprint v3 ➜ v4

## Immediate (Week 1)
- Create scaffolding commits for `backend/`, `frontend/`, `infra/`, `tests/`, and `.github/workflows/` matching the documented blueprint skeleton.
- Update `manifest.json` to version 0.3.0 and align dependency metadata with SRS/TRS tables.
- Add placeholder `contributing.md`, `Makefile`, and Docker Compose files referenced across docs.
- Patch existing scripts to fail fast with actionable guidance when dependent directories or services are missing.

## Short Term (Weeks 2-6)
- Implement FastAPI health endpoint, Alembic base migration, and Redis integration tests.
- Generate React login/dashboard stubs with routing and React Query provider configuration.
- Commit CI workflows covering lint, tests, coverage upload, and container builds; enable dependency review and security scans.
- Stand up observability stack in development (Prometheus + Grafana + Loki) with sample dashboards and alerts.
- Draft new documentation artifacts: QRS, OPS Runbook, UX Guidelines, RFC template, postmortem template.

## Mid Term (Weeks 7-12)
- Implement feature-complete missions/people/timesheets modules with RBAC enforcement and audit logs.
- Integrate release automation (semantic-release) and changelog gating into CI.
- Harden infrastructure with Terraform environment baselines and Helm chart validation.
- Launch MkDocs/Docusaurus site with automated publishing from `docs/`.
- Conduct security tabletop exercise and update incident response playbooks accordingly.

## Continuous Activities
- Monitor dependency health weekly; patch high CVEs immediately.
- Keep roadmap and metadata in sync through automation; review quarterly.
- Enforce documentation drift checks via CI to ensure references remain valid.
- Track OKRs and KPIs (coverage, MTTR, deployment frequency) in GitHub Projects dashboards.
