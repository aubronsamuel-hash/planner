# Codex Deploy Plan – Phase 4

## 1. Environnements cibles et topologie
- **Développement (local / dev containers)** : Compose `docker-compose.dev.yml` pour itération rapide, secrets injectés via `secrets/.env.dev`, volumes bind-mount pour hot reload.
- **Pré-production (staging)** : Nouvel environnement Compose/Helm avec images taggées (`ghcr.io/org/planner-<svc>:staging`), base de données managée (supprimée en Phase 1) à réintroduire via services externes, surveillance rapprochée avant promotion.
- **Production** : Hébergement Kubernetes (cluster managé) orchestré par Helm chart `infra/helm/planner`, services exposés via Ingress contrôlé par traefik/nginx, observabilité complète (Prometheus/Grafana/Alertmanager), secrets fournis par gestionnaire (Secrets Manager/SealedSecrets).

## 2. Docker Compose (prod)
1. **Images & tags** : Mettre à jour `infra/compose/docker-compose.prod.yml` pour épingler des tags immuables (`${BACKEND_TAG}`, `${FRONTEND_TAG}`, `${WORKER_TAG}`) et activer le digest pinning.
2. **Réseau & reverse proxy** : Ajouter un service `nginx` ou `traefik` configuré avec TLS (certificats montés depuis `secrets/`), pointant vers `backend:8000` et `frontend:80`.
3. **Secrets & configuration** : Charger un fichier `.env.prod` (voir §5) via `env_file` pour backend/worker et ajouter `depends_on` healthcheck pour garantir l'ordre de démarrage.
4. **Base de données & cache** : Déclarer services `postgres` et `redis` gérés avec volumes `planner-db-data`, `planner-cache-data`, exposés uniquement sur le réseau interne.
5. **Observabilité** : Étendre la pile avec `prometheus`, `grafana` et `loki` (réutiliser `observability/`), monter les dashboards depuis `observability/grafana/dashboards`.
6. **Validation** : Ajouter une commande `docker compose -f infra/compose/docker-compose.prod.yml config` dans le pipeline pour vérifier la syntaxe.

## 3. Helm chart `infra/helm/planner`
1. **Values structurés** : Enrichir `values.yaml` pour inclure les blocs `image.tag`, `replicaCount`, `resources`, `envFromSecret`, `ingress`, `serviceAccount`, `autoscaling`.
2. **Templates à générer** : Créer des manifests `Deployment` (backend, frontend, worker), `Service`, `Ingress`, `HorizontalPodAutoscaler`, `ConfigMap` (configuration applicative), `Secret` référencé par `values`.
3. **ConfigMaps/Secrets** : Migrer les configurations Dashboard/Missions existantes vers des clés paramétrables, chiffrer les secrets via SealedSecrets (ou ExternalSecrets) et documenter le flux dans `observability/README.md`.
4. **Probes & ressources** : Définir `livenessProbe`/`readinessProbe` sur les conteneurs, limites CPU/mémoire, `podDisruptionBudget` pour backend.
5. **Monitoring** : Exposer `ServiceMonitor` Prometheus pour backend/worker, dashboards Helm hook pour Grafana.
6. **Packaging** : Ajouter `helm lint` et `helm template` dans CI; publier chart dans GitHub Pages ou OCI registry (`ghcr.io/org/charts/planner`).

## 4. Pipeline CI/CD (`.github/workflows/deploy.yml`)
1. **Déclencheurs** : `push` sur branche `main` + tags `v*`, déclenchement manuel `workflow_dispatch` avec sélection environnement.
2. **Jobs** :
   - `build_and_push`: build multi-stage Docker backend/frontend/worker avec caching (`actions/cache`, `docker/build-push-action`), push vers GHCR avec tag `sha` + `latest` ou environnement.
   - `scan`: analyser images avec `aquasecurity/trivy-action` et fail si CVE haute gravité.
   - `helm_lint`: installer Helm, exécuter `helm lint` et `helm template` sur chart.
   - `deploy`: conditionnel (`if: github.ref == 'refs/heads/main'` ou tag), récupérer secrets (OIDC → cloud provider), exécuter `helm upgrade --install` sur cluster cible ou `docker compose` sur VM selon environnement.
3. **Approvals** : Exiger approbation manuelle (Environment Protection) avant déploiement production.
4. **Notifications** : Publier status sur Slack/Teams via webhook secret.

## 5. Secrets & variables d'environnement (`.env.dev` → `.env.prod`)
1. **Inventaire variables** :
   - Backend : `PLANNER_JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`, `FEATURE_FLAG_DASHBOARD`, `LOG_LEVEL`.
   - Frontend : `VITE_API_BASE_URL`, `VITE_AUTH_AUDIENCE`, `VITE_SENTRY_DSN`.
   - Worker : `DATABASE_URL`, `REDIS_URL`, `SENTRY_DSN`.
2. **Fichier `.env.prod`** : créer `secrets/.env.prod` chiffré via `sops` ou `age`, versionné sous forme chiffrée, injecté en pipeline via GitHub Environments.
3. **Mapping GitHub Secrets** : `GHCR_TOKEN`, `KUBE_CONFIG`, `SLACK_WEBHOOK`, `POSTGRES_PASSWORD`, `REDIS_PASSWORD`.
4. **Rotation & audit** : Documenter procédure de rotation trimestrielle, logs d'accès (GitHub OIDC + cloud IAM).

## 6. Monitoring & Observabilité
1. **Prometheus** : Utiliser `observability/prometheus/README.md` comme base; ajouter `prometheus.yml` avec scrap targets backend (`/metrics`), worker, node exporter.
2. **Grafana** : Provisionner dashboards (`observability/grafana/dashboards/*.json`), configurer datasources via ConfigMap, sécuriser admin password via secret `GRAFANA_ADMIN_PASSWORD`.
3. **Alerting** : Déployer Alertmanager avec routes vers Slack/Email; définir règles d'alerte (latence API, taux d'erreur > 5%, jobs worker en échec, saturation CPU/mémoire).
4. **Logs** : Ajouter Loki + Promtail pour agrégation, exposer via Grafana Explore.
5. **Tracing** : Optionnel Phase 4.5 – envisager OpenTelemetry Collector connecté à backend et worker.

## 7. Points de vérification & dépendances
- **Pre-flight** :
  - `pytest` backend & API doivent rester verts (Phase 3).
  - Corriger clients frontend (`frontend/src/lib/api.ts`) avant freeze de release.
- **CI Validation** :
  - `docker compose config` (prod) sans erreur.
  - `helm lint`, `helm template`, `helm unittest` si disponibles.
  - Scans Trivy et ESLint/Vitest (une fois dépendances installées).
- **Post-déploiement** :
  - Checks HTTP (`/healthz`, `/metrics`).
  - Dashboard Grafana accessible, alertes tests déclenchées (silencées).
  - Restauration base de données à partir de snapshot testée.
- **Dépendances externes** : Cluster Kubernetes (1.27+), registre GHCR, stockage objet pour backups, service email/SMS pour notifications.

## 8. RACI & calendrier
- **SRE Lead** : responsable pipeline et Helm.
- **Backend Lead** : owner migrations DB et instrumentation Prometheus.
- **Frontend Lead** : corrige API base URL et configure build prod.
- **Security** : valide secrets, gère scans.
- **Timeline** :
  - Semaine 1 : corrections frontend + freeze applicatif.
  - Semaine 2 : mise à jour Compose & Helm, tests en staging.
  - Semaine 3 : rehearsal déploiement, ajustements observabilité.
  - Semaine 4 : go-live + monitoring renforcé.
