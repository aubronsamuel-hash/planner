# Codex Improvement Plan – Planner Blueprint v3

## 1. Target Monorepo Layout (v3.5 Baseline)
```
planner/
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
├── frontend/
│   ├── src/
│   ├── public/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── infra/
│   ├── docker/
│   │   ├── backend/Dockerfile
│   │   ├── frontend/Dockerfile
│   │   ├── worker/Dockerfile
│   │   └── prometheus/Dockerfile
│   ├── compose/
│   │   ├── docker-compose.dev.yml
│   │   ├── docker-compose.prod.yml
│   │   └── .env.compose.example
│   ├── helm/
│   │   ├── planner/Chart.yaml
│   │   └── planner/values.yaml
│   └── terraform/
├── observability/
│   ├── prometheus/
│   ├── grafana/
│   └── loki/
├── tests/
│   ├── api/
│   ├── e2e/
│   └── smoke/
├── scripts/
│   ├── sh/
│   └── ps/
├── docs/
│   ├── INDEX_v3.md
│   ├── Spec/
│   ├── blueprint/
│   ├── governance/
│   └── changelog/
├── .github/
│   └── workflows/
└── tools/
    ├── codegen/
    └── lint/
```

## 2. Prioritized Improvements
1. **Scaffold the documented components** (backend, frontend, infra, tests, `.github`) with minimal viable code or stubs to make the blueprint executable.
2. **Synchronize metadata sources** (manifest, docs, roadmap) via a shared `metadata.yaml` to avoid version drift and enable automated checks.
3. **Introduce quality specs**:
   - **QRS (Quality Requirements Specification):** consolidate non-functional goals (latency, availability, coverage) currently scattered across SRS/TRS.
   - **OPS Runbook:** operational procedures for incidents, backups, and on-call rotations complementing `SECURITY.md`.
   - **UX Guidelines:** document UI patterns and accessibility requirements for the React frontend.
4. **Extend testing strategy** by centralizing API smoke tests and Playwright e2e suites under `/tests`, driven from CI.
5. **Automate documentation upkeep** with a pipeline that fails on outdated anchors or missing files referenced from INDEX.

## 3. Architecture Evolution (v3.5 → v4.0)
- Formalize domain-driven modules in the backend (`app/domain`, `app/application`, `app/interfaces`) to prepare for GraphQL and WebSocket expansion.
- Add a `gateway` package or service to encapsulate future GraphQL endpoint(s) and rate limiting.
- Prepare infrastructure for multi-tenancy by splitting Terraform state per environment and defining per-tenant schemas in migrations.
- Establish observability exporters (OpenTelemetry collector, Loki stack) under the new `/observability` folder for staged rollout.

## 4. Automation & Tooling Enhancements
- Add **release-bot** (Semantic Release) with changelog + GitHub Releases automation.
- Provide **doc-gen** scripts that sync SRS/TRS/IRS highlights into README badges.
- Integrate **lint-bot** (e.g., Reviewdog) to enforce formatting on PRs.
- Create **bootstrap scripts** that detect missing services and suggest `scripts/sh/dev_up.sh` only after scaffolding is ready.

## 5. Security & Compliance Reinforcement
- Add policy-as-code checks (Open Policy Agent) for Terraform and Kubernetes manifests.
- Introduce dependency review workflow to block merges with known critical CVEs.
- Define a secrets rotation cadence table referencing GitHub/HashiCorp vault integrations.
- Document incident simulations and tabletop exercises aligned with `SECURITY.md` expectations.

## 6. Documentation & Knowledge Management
- Split `/docs` into topic-specific sub-folders (`architecture/`, `operations/`, `product/`).
- Provide templates for RFCs, postmortems, and design decisions.
- Publish onboarding playbooks linking to scripts and environment setup, with cross-checks against actual repository state.
