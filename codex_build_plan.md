# Codex Build Plan — Phase 2 "Build"

## 1. Architecture actuelle

### Backend (FastAPI)
- `backend/app/main.py` instancie une application FastAPI minimaliste avec un unique endpoint de santé (`/api/v1/health`) et ne charge aucun router métier ni configuration de sécurité.【F:backend/app/main.py†L1-L16】
- `backend/README.md` confirme que l'implémentation se limite au scaffolding initial et renvoie vers la blueprint backend pour les évolutions à venir.【F:backend/README.md†L1-L6】

### Frontend (React + Vite)
- `frontend/src/main.tsx` monte une page placeholder centrée avec React Query mais sans routing ni logique d'authentification ou de dashboard.【F:frontend/src/main.tsx†L1-L31】
- La blueprint Frontend V3 prévoit une SPA typée avec routing sécurisé, gestion JWT, composants UI structurés et tests Vitest/MSW qui sont absents du code actuel.【F:docs/blueprint/blocks/03_frontend_v3.md†L1-L106】

### Infrastructure
- `infra/README.md` décrit des compositions Docker et une arborescence Helm/Terraform encore vides en attendant la phase de provisioning, aucune ressource spécifique aux modules métier n'est présente.【F:infra/README.md†L1-L7】

### Tests
- `tests/README.md` ne fait état que des répertoires de suites (API, e2e, smoke) sans cas couvrant les domaines Auth, Missions ou Timesheets.【F:tests/README.md†L1-L5】

## 2. Modules métier manquants et plan de génération
Les blocs Auth, Missions, Timesheets et Dashboard n'ont encore aucun code. Les sections ci-dessous listent les fichiers à générer (par ordre de priorité) pour atteindre un socle fonctionnel cohérent avant implémentation.

### 2.1 Authentification & Gestion des utilisateurs
**Backend**
1. `backend/app/core/config.py` — charger la configuration (JWT secret, expirations, settings DB).
2. `backend/app/core/security.py` — helpers de hashing, génération/validation de tokens JWT, dépendances FastAPI.
3. `backend/app/models/user.py` — modèle ORM (SQLModel ou Pydantic selon choix) pour les utilisateurs et schémas associés.
4. `backend/app/api/dependencies/auth.py` — dépendances de récupération d'utilisateur courant et vérification des rôles.
5. `backend/app/api/routes/auth.py` — endpoints `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`.
6. `backend/app/services/user_service.py` — logique métier (création utilisateur, vérification credos, rotation refresh token).
7. Migration `backend/migrations/versions/<timestamp>_create_users_table.py` — création table `users` + index.

**Frontend**
1. `frontend/src/lib/api.ts` — client Axios mutualisé avec injection du token (suivant blueprint).【F:docs/blueprint/blocks/03_frontend_v3.md†L66-L90】
2. `frontend/src/lib/auth.ts` — helpers de persistance du JWT + décodage/expiration.【F:docs/blueprint/blocks/03_frontend_v3.md†L92-L105】
3. `frontend/src/hooks/useAuth.ts` — hook pour état d'authentification et rafraîchissement.
4. `frontend/src/routes/Login.tsx` — page de connexion (formulaire + mutations React Query).
5. `frontend/src/routes/ProtectedRoute.tsx` — garde de route vérifiant le token.
6. `frontend/src/components/ui/TextField.tsx` et `Button.tsx` — composants formulaires réutilisables.
7. `frontend/src/tests/auth/Login.test.tsx` — tests de la page de login (MSW pour simuler API).

**Infrastructure**
1. `infra/docker/backend/Dockerfile` — ajouter variables d'environnement JWT/DB et commande de migration.
2. `infra/compose/docker-compose.dev.yml` — monter volume pour secrets `.env`, exposer ports backend/frontend, ajouter service DB si absent.
3. `infra/terraform/auth_secrets.tf` — placeholder pour stocker secrets (ex: AWS SSM) en phase suivante.

**Tests centralisés**
1. `tests/api/auth/test_auth_flow.py` — scénarios happy path + cas d'erreur.
2. `tests/smoke/test_auth_health.py` — vérifie qu'un token peut être obtenu en environnement de smoke.
3. `tests/e2e/test_login_flow.py` — automatisation bout-en-bout (Playwright/Cypress placeholder).

### 2.2 Missions (gestion des affectations projets)
**Backend**
1. `backend/app/models/mission.py` — modèle `Mission` (projet, client, dates, statut).
2. `backend/app/models/assignment.py` — relation utilisateur ↔ mission (capacité, rôle).
3. `backend/app/schemas/mission.py` — schémas Pydantic de lecture/écriture.
4. `backend/app/api/routes/missions.py` — CRUD missions + endpoints d'affectation.
5. `backend/app/services/mission_service.py` — règles métier (capacités, chevauchements, archivage).
6. Migration `backend/migrations/versions/<timestamp>_create_missions_tables.py` — tables `missions` et `assignments`.

**Frontend**
1. `frontend/src/routes/Missions.tsx` — page liste (table filtrable, actions CRUD).
2. `frontend/src/components/missions/MissionForm.tsx` — formulaire création/édition.
3. `frontend/src/components/missions/AssignmentList.tsx` — sous-composant des affectations.
4. `frontend/src/lib/types/missions.ts` — types TypeScript partagés.
5. `frontend/src/tests/missions/MissionsPage.test.tsx` — tests UI avec MSW pour missions.

**Infrastructure**
1. `infra/compose/docker-compose.dev.yml` — ajouter service worker (ex: Celery/RQ) si planifie notifications.
2. `infra/helm/planner/templates/missions-configmap.yaml` — configuration front/back (feature flags, quotas).

**Tests centralisés**
1. `tests/api/missions/test_mission_crud.py` — couverture API (list/create/update/delete).
2. `tests/api/missions/test_assignment_rules.py` — vérifie règles de disponibilité.
3. `tests/e2e/test_missions_dashboard.py` — test bout-en-bout sur interactions principales.

### 2.3 Timesheets (suivi du temps)
**Backend**
1. `backend/app/models/timesheet.py` — modèle pour feuilles de temps (utilisateur, mission, date, heures, statut).
2. `backend/app/schemas/timesheet.py` — schémas lecture/écriture, validations (heures max/jour).
3. `backend/app/api/routes/timesheets.py` — endpoints pour soumettre, approuver, exporter.
4. `backend/app/services/timesheet_service.py` — règles de validation, calcul d'heures.
5. Migration `backend/migrations/versions/<timestamp>_create_timesheets_table.py`.

**Frontend**
1. `frontend/src/routes/Timesheets.tsx` — vue hebdomadaire avec saisie inline.
2. `frontend/src/components/timesheets/TimesheetTable.tsx` — table responsive.
3. `frontend/src/components/timesheets/TimesheetApprovalModal.tsx` — modale manager.
4. `frontend/src/lib/types/timesheets.ts` — types partagés.
5. `frontend/src/tests/timesheets/TimesheetEntry.test.tsx` — tests de saisie.

**Infrastructure**
1. `infra/docker/backend/Dockerfile` — ajouter dépendances (par ex. `pandas` pour export CSV) si requises.
2. `infra/terraform/timesheet_storage.tf` — bucket/object storage placeholder pour exports.

**Tests centralisés**
1. `tests/api/timesheets/test_submission_flow.py` — soumission, édition, approbation.
2. `tests/api/timesheets/test_validation.py` — limites d'heures, chevauchements.
3. `tests/e2e/test_timesheet_weekly_flow.py` — scénario complet utilisateur.

### 2.4 Dashboard (vue consolidée management)
**Frontend**
1. `frontend/src/App.tsx` — configurer layout global, routes protégées, navigation.
2. `frontend/src/routes/Dashboard.tsx` — page overview (widgets KPIs missions/timesheets).
3. `frontend/src/components/layout/Shell.tsx` — shell avec header/sidebar et contenu.【F:docs/blueprint/blocks/03_frontend_v3.md†L44-L64】
4. `frontend/src/components/dashboard/KpiCards.tsx` — composant cartes KPI.
5. `frontend/src/components/dashboard/UpcomingMissions.tsx` — liste condensée des prochaines missions.
6. `frontend/src/components/dashboard/TeamAvailability.tsx` — visuel dispo (heatmap ou table).
7. `frontend/src/tests/dashboard/DashboardRouting.test.tsx` — tests de navigation protégée.

**Backend**
1. `backend/app/api/routes/dashboard.py` — endpoint agrégé fournissant KPIs (missions actives, heures soumises, etc.).
2. `backend/app/services/dashboard_service.py` — agrégation cross-modules.
3. `backend/app/schemas/dashboard.py` — schémas de réponse pour KPIs.

**Infrastructure**
1. `infra/compose/docker-compose.prod.yml` — exposer variables FEATURE_FLAG_DASHBOARD pour activer widgets.
2. `infra/helm/planner/templates/dashboard-configmap.yaml` — configuration front (polling interval, cards visibles).

**Tests centralisés**
1. `tests/api/dashboard/test_kpi_summary.py` — vérifie calculs agrégés.
2. `tests/e2e/test_dashboard_entrypoint.py` — scénarios d'accès au dashboard après login.
3. `tests/smoke/test_dashboard_ping.py` — vérifie endpoint agrégé répond en production.

## 3. Prochaines étapes
1. Prioriser l'implémentation du module Auth pour débloquer les autres routes sécurisées.
2. Générer les fichiers listés pour Auth en premier, puis Missions et Timesheets en parallèle une fois le socle commun en place.
3. Terminer par le Dashboard qui consommera les API précédentes.
4. Après génération des fichiers, renseigner les TODO techniques restants et préparer les stories d'implémentation détaillées.

