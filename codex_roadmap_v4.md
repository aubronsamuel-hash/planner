# Codex Roadmap to Planner v4.0

## Overview
- **Time horizon:** 4 quarters (Q1–Q4 2026)
- **Cadence:** Iterative delivery with monthly checkpoints, automation-first.
- **Dependencies:** Completion of v3.5 scaffolding, resource allocation across backend, frontend, DevOps, and Docs squads.

## Step 1 – Audit & Refactor Structure (Q1 2026, Month 1)
- Bootstrap missing directories and placeholder services to match the documented monorepo layout.
- Align `manifest.json`, roadmap metadata, and doc references through a single metadata source.
- Deliverable: Repository tree mirrors Blueprint v3 expectations with CI dry-runs in place.

## Step 2 – Auto-generate Backend Modules (Q1 2026, Month 2)
- Use Codex codegen scripts under `tools/codegen/` to scaffold FastAPI modules (auth, people, missions, timesheets).
- Generate Alembic migrations, unit-test skeletons, and OpenAPI schemas.
- Deliverable: Passing backend lint/tests locally; API health endpoint live under Docker Compose.

## Step 3 – Auto-generate Frontend Pages (Q1 2026, Month 3)
- Produce React views (Auth, Dashboard, Missions, People) using shared UI kit and React Query bindings.
- Add MSW mocks and Vitest suites to cover critical flows.
- Deliverable: Frontend dev server integrates with backend mock API; smoke e2e test green.

## Step 4 – Implement Full CI/CD (Q2 2026, Months 4-5)
- Commit GitHub Actions workflows for lint, test, build, release, and security scans.
- Wire Codecov, Trivy, Bandit, npm audit, and dependency-review gates.
- Deliverable: CI required checks enforce code quality; semantic-release publishes prereleases to GHCR.

## Step 5 – Observability Rollout (Q2 2026, Month 6)
- Provision Prometheus, Grafana, and Loki assets under `/observability`.
- Instrument backend with Prometheus metrics and OpenTelemetry traces; configure alerts.
- Deliverable: Monitoring dashboards and alerting rules operating in staging.

## Step 6 – Living Documentation Platform (Q3 2026, Months 7-8)
- Migrate docs to MkDocs or Docusaurus pipeline with automated publishing on release.
- Sync SRS/TRS/IRS, QRS, OPS runbook, and UX guidelines into documentation site.
- Deliverable: Docs site deployed with auto-generated navigation and versioning.

## Step 7 – Test, QA, Release (Q3–Q4 2026, Months 9-12)
- Expand automated testing: load tests, contract tests, accessibility scans.
- Conduct release readiness reviews, incident response drills, and performance benchmarking.
- Ship Planner v4.0 GA with hardened security posture and observability SLIs tracked.

## Milestone Tracking
- Establish OKRs per step, tracked via GitHub Projects and automated status badges.
- Monthly retrospectives capture lessons learned and update subsequent iterations.
