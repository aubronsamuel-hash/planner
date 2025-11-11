🧩 Block 1 – Core Blueprint v3 (Production-Ready Monorepo)
0. Guiding Principles

Code-first, infra-aware — tout code source est auto-descriptif et déployable.

Reproducible builds via Docker Compose et versions figées.

Cross-platform : compatibilité Windows (PowerShell) / Linux / macOS (Bash).

Observabilité intégrée : Prometheus + logs structurés par défaut.

DX maximale : scripts simples, cohérence CLI, onboarding express.

Infra-as-code ready : basculable vers Kubernetes sans refonte.

1. Objectives

Un monorepo unique : backend, frontend, infra, docs, tests, CI/CD.

Environnement local unifié (Docker Compose multi-profil).

Scripts DevOps pour init, build, test, lint, format, deploy.

CI déterministe (GitHub Actions + caches).

Security-first : scan SCA + linting + type-check obligatoire.

Observabilité out-of-the-box : /metrics exposé + stack Prometheus/Grafana.

2. Repository Layout (v3)
repo/
  ├── .editorconfig
  ├── .gitignore
  ├── .gitattributes
  ├── .env.example
  ├── .env.local
  ├── README.md
  ├── Makefile
  ├── docker-compose.yml
  ├── manifest.json
  ├── scripts/
  │   ├── ps/
  │   │   ├── init_repo.ps1
  │   │   ├── dev_up.ps1
  │   │   ├── dev_down.ps1
  │   │   ├── run_tests.ps1
  │   │   ├── smoke.ps1
  │   │   ├── fmt.ps1
  │   │   ├── lint.ps1
  │   │   ├── logs.ps1
  │   │   ├── db_migrate.ps1
  │   │   ├── reseed.ps1
  │   │   ├── rebuild.ps1
  │   │   └── coverage.ps1
  │   └── sh/
  │       ├── init_repo.sh
  │       ├── dev_up.sh
  │       ├── dev_down.sh
  │       ├── run_tests.sh
  │       ├── lint.sh
  │       ├── fmt.sh
  │       └── logs.sh
  │
  ├── backend/
  │   ├── app/
  │   ├── pyproject.toml
  │   ├── uv.lock
  │   ├── alembic.ini
  │   └── tests/
  │
  ├── frontend/
  │   ├── src/
  │   ├── vite.config.ts
  │   ├── tsconfig.json
  │   ├── package.json
  │   └── tests/
  │
  ├── infra/
  │   ├── docker/
  │   │   ├── backend/Dockerfile
  │   │   ├── frontend/Dockerfile
  │   │   ├── worker/Dockerfile
  │   │   └── prometheus/Dockerfile
  │   └── k8s/
  │       ├── base/
  │       │   ├── backend.yaml
  │       │   ├── frontend.yaml
  │       │   ├── redis.yaml
  │       │   ├── postgres.yaml
  │       │   ├── prometheus.yaml
  │       │   ├── grafana.yaml
  │       │   └── namespace.yaml
  │
  ├── tests/
  │   ├── e2e/
  │   │   ├── playwright.config.ts
  │   │   └── test_smoke.spec.ts
  │   └── api/
  │       └── test_health.py
  │
  ├── docs/
  │   ├── INDEX.md
  │   ├── architecture.md
  │   ├── contributing.md
  │   ├── roadmap/
  │   └── blueprint/
  │       ├── 01_blueprint_v3.md
  │       ├── 02_backend_v3.md
  │       ├── 03_frontend_v3.md
  │       ├── 04_ci_cd_security_v3.md
  │       ├── 05_docs_devops_v3.md
  │       └── 06_architecture_v3.md
  │
  └── .github/
      └── workflows/
          ├── ci.yml
          ├── security.yml
          ├── release.yml
          └── deploy.yml

3. Manifest (v3)
{
  "version": "0.3.0",
  "backend": {
    "lang": "Python 3.12",
    "framework": "FastAPI",
    "database": "PostgreSQL 16",
    "cache": "Redis 7"
  },
  "frontend": {
    "lang": "TypeScript 5.6",
    "framework": "React + Vite",
    "ui": "ShadCN + Tailwind"
  },
  "infra": {
    "compose": "3.9",
    "monitoring": ["Prometheus", "Grafana"],
    "queue": "RQ Worker"
  },
  "ci": ["GitHub Actions", "Codecov", "Trivy"],
  "scripts": ["PowerShell", "Bash"]
}

4. Docker Compose (v3, multi-profiles)
version: "3.9"

services:
  db:
    image: postgres:16
    container_name: planner-db
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    volumes:
      - db_data:/var/lib/postgresql/data
    ports: ["5432:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    container_name: planner-redis
    ports: ["6379:6379"]

  backend:
    build: ./infra/docker/backend
    container_name: planner-backend
    env_file:
      - ./.env.local
      - ./backend/.env.example
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports: ["8000:8000"]
    depends_on: [db, redis]
    profiles: ["dev", "test"]

  frontend:
    build: ./infra/docker/frontend
    container_name: planner-frontend
    env_file:
      - ./.env.local
      - ./frontend/.env.example
    volumes:
      - ./frontend:/usr/src/app
    command: npm run dev -- --host 0.0.0.0 --port 5173
    ports: ["5173:5173"]
    depends_on: [backend]
    profiles: ["dev"]

  worker:
    build: ./infra/docker/worker
    env_file:
      - ./.env.local
    volumes:
      - ./backend:/app
    depends_on: [backend, redis]
    profiles: ["dev", "prod"]

  prometheus:
    build: ./infra/docker/prometheus
    container_name: planner-prometheus
    volumes:
      - ./infra/docker/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports: ["9090:9090"]
    profiles: ["monitoring"]

  grafana:
    image: grafana/grafana:10.3.0
    container_name: planner-grafana
    ports: ["3000:3000"]
    profiles: ["monitoring"]
    depends_on: [prometheus]

volumes:
  db_data:

5. Root .env.example
COMPOSE_PROJECT_NAME=planner
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=app
REDIS_URL=redis://redis:6379/0
BACKEND_URL=http://backend:8000
FRONTEND_URL=http://frontend:5173
JWT_SECRET=change_me
JWT_ALG=HS256
ENV=dev
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000

6. Makefile (v3)
.PHONY: up down logs fmt lint test migrate rebuild coverage

up: 
	docker compose --profile dev up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

fmt:
	docker compose exec -T backend ruff check --fix || true
	docker compose exec -T backend black .
	cd frontend && npx eslint . --fix

lint:
	docker compose exec -T backend ruff check
	cd frontend && npx eslint .

test:
	docker compose exec -T backend pytest -q
	cd frontend && npm test --silent

migrate:
	docker compose exec -T backend alembic upgrade head

coverage:
	docker compose exec -T backend pytest --cov=app --cov-report=term-missing

rebuild:
	docker compose down -v && docker compose up -d --build

7. Profiles Résumés
Profil	Description	Services lancés
dev	Développement local complet	db, redis, backend, frontend, worker
test	CI ou intégration	db, backend, redis
prod	Production (sans dev tools)	backend, worker, db, redis
monitoring	Observabilité optionnelle	prometheus, grafana
8. Quality Gates v3

✅ Lint : ruff, eslint obligatoires avant merge.

✅ Tests : couverture ≥ 70% initiale (objectif 85%).

✅ Security : scan SCA via trivy + bandit.

✅ Builds reproductibles : images Docker taggées par SHA.

✅ Docs synchronisées : CI vérifie la mise à jour de /docs/api.

9. Quickstart (v3)
# 1️⃣ Cloner le projet
git clone https://github.com/org/planner.git && cd planner

# 2️⃣ Créer les fichiers d'env
scripts/ps/init_repo.ps1   # ou ./scripts/sh/init_repo.sh

# 3️⃣ Lancer l'environnement complet
make up

# 4️⃣ Vérifier la santé
curl http://localhost:8000/api/v1/health
curl http://localhost:5173

# 5️⃣ Ouvrir Grafana (monitoring)
http://localhost:3000