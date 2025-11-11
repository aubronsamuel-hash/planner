🛠️ Block 5 – Documentation, DevOps & Gouvernance (v3)
1. Objectifs

Créer un environnement DevOps intégré : init, build, test, deploy.

Fournir des scripts cohérents PowerShell et Bash.

Mettre en place un Makefile universel.

Documenter les conventions d’équipe : Git, branches, PR, release.

Ajouter l’observabilité (Prometheus + Grafana).

Créer un onboarding clair avec un CONTRIBUTING.md.

2. Arborescence DevOps
scripts/
├── ps/
│   ├── init_repo.ps1
│   ├── dev_up.ps1
│   ├── dev_down.ps1
│   ├── run_tests.ps1
│   ├── smoke.ps1
│   ├── fmt.ps1
│   ├── lint.ps1
│   ├── logs.ps1
│   ├── db_migrate.ps1
│   ├── reseed.ps1
│   ├── rebuild.ps1
│   └── coverage.ps1
└── sh/
    ├── init_repo.sh
    ├── dev_up.sh
    ├── dev_down.sh
    ├── run_tests.sh
    ├── lint.sh
    ├── fmt.sh
    ├── logs.sh
    └── reseed.sh

3. Scripts PowerShell
scripts/ps/init_repo.ps1
Write-Host "== init_repo =="
if (-Not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Push-Location backend
if (-Not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Pop-Location
Push-Location frontend
if (-Not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Pop-Location
Write-Host "Repository initialized ✅"

scripts/ps/dev_up.ps1
Write-Host "== dev up =="
docker compose --profile dev up -d --build

scripts/ps/dev_down.ps1
Write-Host "== dev down =="
docker compose down -v

scripts/ps/run_tests.ps1
Write-Host "== tests =="
docker compose exec -T backend pytest -q
Push-Location frontend
npm test --silent
Pop-Location

scripts/ps/smoke.ps1
Write-Host "== smoke test =="
try {
  $r = Invoke-WebRequest -Uri http://localhost:8000/api/v1/health -UseBasicParsing
  Write-Host "Backend Health: " $r.Content
} catch { Write-Host "Backend not responding ❌" }

scripts/ps/logs.ps1
Write-Host "== logs =="
docker compose logs -f

scripts/ps/reseed.ps1
Write-Host "== reseed =="
docker compose exec -T backend python -m app.db.seed

scripts/ps/coverage.ps1
Write-Host "== coverage =="
docker compose exec -T backend pytest --cov=app --cov-report=term-missing

4. Scripts Bash
scripts/sh/init_repo.sh
#!/usr/bin/env bash
set -e
echo "== init_repo =="
cp -n .env.example .env || true
cp -n backend/.env.example backend/.env || true
cp -n frontend/.env.example frontend/.env || true
echo "Repository initialized ✅"

scripts/sh/dev_up.sh
#!/usr/bin/env bash
docker compose --profile dev up -d --build

scripts/sh/run_tests.sh
#!/usr/bin/env bash
docker compose exec -T backend pytest -q
(cd frontend && npm test --silent)

scripts/sh/logs.sh
#!/usr/bin/env bash
docker compose logs -f

scripts/sh/reseed.sh
#!/usr/bin/env bash
docker compose exec -T backend python -m app.db.seed

5. Makefile complet
.PHONY: up down logs test lint fmt migrate coverage rebuild smoke seed

up: ; docker compose --profile dev up -d --build
down: ; docker compose down -v
logs: ; docker compose logs -f
fmt: ; docker compose exec -T backend ruff check --fix || true
lint: ; docker compose exec -T backend ruff check && cd frontend && npx eslint .
test: ; docker compose exec -T backend pytest -q && cd frontend && npm test --silent
migrate: ; docker compose exec -T backend alembic upgrade head
coverage: ; docker compose exec -T backend pytest --cov=app --cov-report=term-missing
smoke: ; ./scripts/sh/smoke.sh
seed: ; ./scripts/sh/reseed.sh
rebuild: ; docker compose down -v && docker compose up -d --build

6. Observabilité
Stack Prometheus + Grafana
Docker Compose profile "monitoring"

Prometheus : collecte /metrics du backend.

Grafana : dashboards interactifs.

infra/docker/prometheus/prometheus.yml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "backend"
    static_configs:
      - targets: ["backend:8000"]

Accès :

Prometheus → http://localhost:9090

Grafana → http://localhost:3000
 (login: admin / pass: admin)

7. Conventions Git & Workflow
Élément	Règle
Branches	main (prod), develop (préprod), feature/*, fix/*, release/*
Commits	feat:, fix:, docs:, ci:, chore:
PRs	1 feature = 1 PR = 1 review obligatoire
Rebase	avant merge sur main
Tags	générés via semantic-release
Lint commits	validés via commitlint
8. CONTRIBUTING.md (extrait)
# Contribuer à Planner

## 🧭 Installation rapide
```bash
git clone https://github.com/org/planner.git
cd planner
scripts/sh/init_repo.sh
make up

🧩 Commandes utiles
Commande	Description
make up	Lance l’environnement complet
make down	Arrête et supprime les conteneurs
make test	Exécute tous les tests
make lint	Vérifie la qualité du code
make coverage	Génère la couverture de test
make seed	Remplit la base avec des données d’exemple
🧱 Règles de contribution

Fork → commit → PR vers develop

Style de commit : type(scope): message

Inclure tests unitaires pour chaque nouvelle fonctionnalité.

Ajouter la doc correspondante dans /docs.

🔐 Sécurité

Ne pas pousser de secrets (.env, JWT_SECRET, etc.).
Les variables sensibles doivent être configurées via GitHub Secrets.

📘 Docs

/docs/architecture_v3.md

/docs/blueprint/

/docs/api/openapi.json


---

## 9. Gouvernance & Qualité
| Domaine | Outil | Objectif |
|----------|--------|----------|
| **Code Style** | Ruff, ESLint, Mypy | Standard Python/TS |
| **Tests** | Pytest, Vitest | ≥70% coverage |
| **Sécurité** | Bandit, Trivy, npm audit | Aucun High/Critical |
| **CI/CD** | GitHub Actions | Automatisation totale |
| **Docs** | Markdown + Docusaurus (optionnel) | Maintenabilité |
| **Monitoring** | Prometheus, Grafana | Visibilité du runtime |

---

## 10. Roadmap DevOps


✅ Step 01 : Monorepo Docker + CI
✅ Step 02 : Tests automatiques backend/frontend
✅ Step 03 : JWT + Auth sécurisée
✅ Step 04 : Observabilité Prometheus
✅ Step 05 : Scans sécurité automatisés
🧩 Step 06 : Déploiement K8s (Helm)
🧩 Step 07 : Auto-scaling + logs centralisés (ELK)
🧩 Step 08 : E2E Playwright
🧩 Step 09 : Alertes Grafana + Slack
🧩 Step 10 : Audit et conformité ISO27001


---

## 11. Exemple Onboarding Dev
### En 5 minutes 👇
```bash
git clone https://github.com/org/planner.git
cd planner
scripts/sh/init_repo.sh
make up
curl http://localhost:8000/api/v1/health
curl http://localhost:5173


💡 Pour tester le monitoring :

make up PROFILE=monitoring
open http://localhost:3000

12. Résumé global
Module	Description	Statut
Backend	FastAPI, PostgreSQL, Redis, RQ	✅
Frontend	React + Vite + Auth	✅
CI/CD	Lint, Test, Build, Security, Release	✅
DevOps	Scripts, Makefile, Observabilité	✅
Docs	Architecture, Roadmap, Contrib, API	✅