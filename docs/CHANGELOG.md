# 🧾 CHANGELOG – Planner Blueprint

> **Convention :** basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
> **Version actuelle : 0.3.2 (Blueprint v3)**
> **Format :** SemVer (Semantic Versioning)

---

## [0.3.2] – 2025-11-15
### 🚀 Added
- Worker Redis RQ (`backend/app/worker/`) avec métriques Prometheus (`rq_jobs_total`,
  `rq_failures_total`, `rq_job_duration_seconds`).
- Endpoint `/metrics` FastAPI (compteurs, histogrammes et jauges HTTP).
- Stack monitoring Docker Compose : Prometheus, Grafana (datasources provisionnées),
  Loki + dashboard `planner-overview`.
- Workflows GitHub Actions `test_worker.yml` et `deploy.yml` (push image GHCR,
  vérification `curl /metrics`).
- Documentation `docs/monitoring.md` et `docs/worker_reference.md`.

### 🧰 Changed
- Dockerfiles backend/worker installent le package Python pour exposer les
  métriques et la configuration Loki.
- `Makefile` expose `make monitoring` pour démarrer l’observabilité locale.

### 🧪 Tests
- Nouveaux tests Pytest sur l’instrumentation (`test_metrics.py`,
  `test_worker_tasks.py`, `test_worker_queue.py`).

---

## [0.3.0] – 2025-11-11
### 🚀 Added
- Nouvelle architecture **Blueprint v3** complète :
  - Backend FastAPI + PostgreSQL + Redis (auth sécurisée, observabilité).
  - Frontend React + Vite + Tailwind + JWT.
  - CI/CD GitHub Actions + GHCR + Codecov + Semantic Release.
  - Observabilité Prometheus + Grafana intégrée.
- Refonte totale du dossier `/docs/` :
  - 6 blocs principaux (Blueprint → Architecture).
  - Nouvel INDEX_v3 avec compatibilité versions.
  - Scripts DevOps PowerShell et Bash.
- Qualité et sécurité :
  - Scans **Trivy**, **Bandit**, **npm audit**.
  - Tests avec couverture ≥ 70%.

### 🧰 Changed
- Docker Compose multi-profils (`dev`, `test`, `prod`, `monitoring`).
- CI unifiée (backend + frontend dans un même workflow).
- Passage à Python 3.12 et Node 20.
- Documentation entièrement réécrite (Markdown v3).

### 🧩 Deprecated
- Ancien blueprint v2 (2024) remplacé.
- CI séparée backend/frontend supprimée.
- Ancien dossier `/docs/blueprint/v2` archivé.

### 🐛 Fixed
- Résolution du problème de compatibilité `asyncpg`.
- Amélioration du cache GitHub Actions pour pip et npm.
- Correction des tests asynchrones avec `pytest-asyncio`.
- **bcrypt+SQLAlchemy fix** : implémentation complète de l’authentification
  asynchrone (JWT HS256, JTI Redis, migrations Alembic) pour la phase
  Blueprint v3.1-Recovery.

---

## [0.2.0] – 2024-07-10
### Added
- Support initial Docker Compose.
- Documentation FastAPI + React.
- Tests CI de base sur backend.

### Changed
- Passage de Flask à FastAPI.
- Début intégration Alembic.

---

## [0.1.0] – 2023-12-02
### Added
- Première version prototype.
- Backend Flask + SQLite.
- Frontend React sans Auth.

---

## 📈 Version à venir
> **[0.4.0] (prévue pour 2026)**
> - Ajout WebSocket + GraphQL Gateway
> - Observabilité OpenTelemetry complète
> - K8s Helm Charts
