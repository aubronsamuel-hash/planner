🔒 Block 4 – CI/CD v3 (Pipelines, Sécurité, Qualité, Release)
1. Objectifs

CI/CD unifiée pour backend + frontend.

Cache intelligent pour pip et npm.

Intégration de sécurité continue (SCA, SAST).

Build et publication automatique d’images Docker.

Tests unitaires, linting et couverture dans le pipeline.

Gestion sémantique des releases (semantic-versioning).

2. Structure GitHub Actions
.github/
└── workflows/
    ├── ci.yml
    ├── security.yml
    ├── release.yml
    └── deploy.yml

3. CI Principale – ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend:
    name: Backend (Python)
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: app
          POSTGRES_PASSWORD: app
          POSTGRES_DB: app
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U app"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}

      - name: Install backend deps
        run: |
          cd backend
          pip install uv
          uv pip install .[dev]

      - name: Lint backend
        run: cd backend && ruff check . && mypy .

      - name: Test backend
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql+asyncpg://app:app@localhost:5432/app

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./backend/coverage.xml
          token: ${{ secrets.CODECOV_TOKEN }}

  frontend:
    name: Frontend (Node)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Cache npm
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

      - name: Install deps
        run: cd frontend && npm ci

      - name: Lint frontend
        run: cd frontend && npm run lint

      - name: Test frontend
        run: cd frontend && npm run test -- --coverage --run
        env:
          CI: true

4. Sécurité – security.yml
name: Security Scan

on:
  schedule:
    - cron: "0 3 * * 1" # chaque lundi
  workflow_dispatch:

jobs:
  sast_sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan Python (Bandit)
        run: |
          pip install bandit
          bandit -r backend -ll -q

      - name: Scan Node (npm audit)
        run: |
          cd frontend
          npm audit --omit dev

      - name: Docker Image Scan
        uses: aquasecurity/trivy-action@0.24.0
        with:
          scan-type: fs
          format: table
          ignore-unfixed: true
          exit-code: 0

5. Build & Publication Docker – deploy.yml
name: Build & Push Docker

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & Push Backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./infra/docker/backend/Dockerfile
          push: true
          tags: ghcr.io/${{ github.repository }}/backend:latest

      - name: Build & Push Frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./infra/docker/frontend/Dockerfile
          push: true
          tags: ghcr.io/${{ github.repository }}/frontend:latest

6. Versioning Automatique – release.yml
name: Semantic Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install Semantic Release
        run: npm install -g semantic-release @semantic-release/git @semantic-release/changelog @semantic-release/github

      - name: Run Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npx semantic-release

7. Badges README
[![CI](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)]()
[![Security](https://github.com/org/repo/actions/workflows/security.yml/badge.svg)]()
[![Coverage](https://codecov.io/gh/org/repo/branch/main/graph/badge.svg)]()
[![Docker](https://github.com/org/repo/actions/workflows/deploy.yml/badge.svg)]()

8. Qualité & Garde-fous
Contrôle	Description	Objectif
Linting	ruff, eslint, mypy	0 erreurs, code propre
Testing	pytest, vitest	70%+ coverage
Security	bandit, trivy, npm audit	Aucun High/Critical
CI speed	Caches pip/npm	< 5 min
Release	semantic-release	Versioning automatisé
Observabilité	Prometheus + Grafana	métriques /metrics en CI
9. Exemple de logs CI réussie
✅ Lint backend → OK
✅ Tests backend (19 passed)
✅ Lint frontend → OK
✅ Vitest frontend → OK (coverage: 82%)
✅ Bandit → No issues
✅ Trivy → 0 vulnerabilities
✅ Docker build → pushed ghcr.io/org/planner
✅ Semantic release → 0.3.0 → changelog updated

10. Conseils de déploiement

Utiliser GitHub Environments (staging, production) avec approbation manuelle.

Configurer des secrets (JWT_SECRET, DATABASE_URL, REDIS_URL, GRAFANA_ADMIN_PASS).

Relier GHCR à ton hébergeur (Railway, Fly.io, Render, K8s).

Activer la rétention des artefacts (coverage, reports, build logs).

Ajouter des notifications Slack via actions/slack@v3.

11. Quickstart CI locale (optionnel)

Tester la CI localement avec act
 :

act -j backend --artifact-server-path ./artifacts