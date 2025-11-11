🧱 Block 6 – Architecture v3 (Système, Données, Sécurité, Scaling)
1. Vision d’ensemble

L’application Planner v3 est une architecture modulaire et scalable, basée sur :

Frontend SPA (React + Vite)

Backend API REST (FastAPI + PostgreSQL + Redis)

Worker asynchrone (RQ)

Monitoring intégré (Prometheus + Grafana)

CI/CD (GitHub Actions + GHCR + Semantic Release)

Multi-tenancy + RBAC extensible

2. Schéma global (ASCII-only)
+--------------------+
|   Browser (React)  |
+--------------------+
          |
          | HTTPS / REST / JWT
          v
+----------------------------------+
|  Backend (FastAPI)               |
|  - Routers (v1)                  |
|  - Services (auth, people, etc.) |
|  - DB Layer (SQLAlchemy)         |
|  - Redis (cache & queue)         |
|  - /metrics (Prometheus)         |
+----------------------------------+
          | Async SQL
          v
+--------------------+
| PostgreSQL 16      |
| - data model v3    |
+--------------------+

          +----------------+
          | Redis Queue    |
          +----------------+
                 |
                 v
       +------------------+
       | RQ Worker        |
       | - notifications  |
       | - analytics job  |
       +------------------+

Monitoring side-channel:
   ├─ Prometheus (scrape metrics)
   └─ Grafana (dashboards)

3. Flux typique (Create Person)
Frontend → POST /api/v1/people
Backend Router → validate input (Pydantic)
↓
Service → DB Session
↓
SQLAlchemy → INSERT person(...)
↓
Commit → Response JSON
Frontend → Cache update (React Query)

4. Sécurité : Auth & RBAC
Authentification

JWT (HS256) signé avec clé secrète.

Durée par défaut : 60 min.

Refresh token optionnel (via /auth/refresh future).

Autorisation

RBAC (Role-Based Access Control) basé sur tables :

user

role

user_role

Décodage JWT → sub → récupération des rôles.

Dépendance FastAPI :

async def require_role(role: str):
    def wrapper(user: User = Depends(get_current_user)):
        if role not in user.roles:
            raise HTTPException(status_code=403)
        return user
    return wrapper

Sécurité API
Aspect	Mesure
Auth	JWT obligatoire
Transport	HTTPS
CORS	Whitelist frontend
Rate Limiting	via reverse proxy
Secrets	.env + GitHub Secrets
Password	Hashé bcrypt
Headers	Strict-Transport-Security, X-Frame-Options
5. Observabilité & Monitoring
Prometheus

Collecte /metrics toutes les 5s.

Exemples de métriques :

http_requests_total

http_request_duration_seconds

rq_jobs_total

process_memory_bytes

Grafana

Dashboards :

API latency (95th percentile)

Worker throughput

DB query time

Error rate

Alerte : seuil d’erreur >5% sur 5 minutes.

Logging structuré
{
  "timestamp": "2025-11-10T21:00:00Z",
  "level": "INFO",
  "service": "backend",
  "message": "POST /api/v1/people 201 Created",
  "duration_ms": 122
}

6. Data Model v3
[organization] 1---* [user] *---* [role]
       |
       *---* [project] 1---* [mission] *---* [assignment] *---1 [person]
                                           |
                                           *---1 [timesheet]

Tables principales
Table	Description	Relations
organization	Regroupe les entités multi-tenant	1→* user, project
user	Authentification et profil	→ role, 1→org
role	Définition des permissions	→ user
person	Intervenant ou technicien	→ mission via assignment
project	Projet de production	1→* mission
mission	Événement planifié	1→* assignment
assignment	Liaison mission-personne	1→1 timesheet
timesheet	Feuille de temps	-
notification	Log des envois (email/webhook)	-
7. Séquence : Notification Worker
Backend (POST /api/v1/notify)
  ↓ enqueue Redis
Redis Queue
  ↓
Worker RQ (consume)
  ↓ send_email()
  ↓ mark notification.status='sent'

8. Architecture physique (Docker Compose v3)
Service	Langage	Rôle	Ports
backend	Python 3.12 (FastAPI)	API principale	8000
frontend	TypeScript (Vite)	UI web	5173
worker	Python	Tâches async (RQ)	-
db	PostgreSQL 16	Stockage	5432
redis	Redis 7	Cache & queue	6379
prometheus	YAML config	Monitoring	9090
grafana	Go (Dashboards)	Visualisation	3000
9. Déploiement Kubernetes (exemple simplifié)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: planner-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: ghcr.io/org/planner/backend:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: planner-secrets
---
apiVersion: v1
kind: Service
metadata:
  name: planner-backend
spec:
  selector:
    app: backend
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP

10. Scalabilité
Cible	Méthode
API	autoscaling horizontal (HPA Kubernetes)
DB	read replicas PostgreSQL
Cache	Redis cluster mode
Worker	RQ multi-pod avec TTL
Frontend	CDN + cache HTTP
Monitoring	Prometheus + long-term storage
CI/CD	Parallel matrix jobs
11. Sécurité Infrastructure
Domaine	Mesure
Réseau	Segmentation Docker / Namespace K8s
Secrets	GitHub Secrets / Vault
Base de données	Chiffrement en transit (SSL)
Backup	pg_dump automatisé quotidien
Logs	Centralisation Loki ou ELK
Auth CI/CD	OIDC + Permissions minimales
Firewall	Cloud provider (deny-all par défaut)
12. Performance & Résilience

Temps moyen de réponse : <200 ms sur requêtes CRUD.

Support charge 1k req/s (3 pods backend).

Failover Redis/DB prévu via restart policy.

Retry automatique des tâches RQ.

Observabilité intégrée aux tests CI (pytest --metrics futur).

13. Diagramme Séquence Auth (simplifié)
Browser ─── POST /auth/login ───▶ Backend
Backend ─── SQL query (user) ───▶ DB
DB ─── result ───▶ Backend
Backend ─── JWT ───▶ Browser
Browser ─── Authorization: Bearer <token> ───▶ Backend (protected route)
Backend ─── validate token ───▶ OK ✅

14. Scalabilité future

Passage de Docker Compose → Helm charts K8s.

Intégration OpenTelemetry pour tracing distribué.

Ajout WebSocket pour live updates (notifications).

Load balancing via Traefik ou NGINX ingress.

Intégration CI/CD → staging automatique + review apps.

15. Exemple Monitoring (metrics clés)
Type	Nom	Description
HTTP	http_requests_total	Total de requêtes API
Latence	http_request_duration_seconds	Durée moyenne des requêtes
RQ	rq_jobs_enqueued_total	Jobs ajoutés
DB	db_query_duration_seconds	Temps moyen de requête
Worker	rq_jobs_failed_total	Jobs échoués
System	process_cpu_seconds_total	CPU du conteneur
16. Maintenance & Audit

alembic upgrade head avant chaque déploiement.

Backups PostgreSQL (pg_dump -Fc app > backup.dump).

Scan sécurité automatique via security.yml.

Vérification dépendances tous les 30 jours.

Audit trimestriel : test de charge + failover test.

17. Schéma global complet (ASCII résumé)
+--------------------------------------------------------------+
|                      FRONTEND (React)                        |
|  Auth / UI / Routing / Cache / Query                         |
+--------------------------------------------------------------+
                | REST (JWT)
                v
+---------------------------+   Queue  +------------------------+
| BACKEND (FastAPI)         | <------> | REDIS (Cache + Queue)  |
| Auth / API / DB / Metrics |          +------------------------+
| Observabilité Prometheus  |                     |
+-------------+-------------+                     v
              |                                +--------+
              v                                | WORKER |
       +--------------+                       +--------+
       | PostgreSQL   |
       | Data layer   |
       +--------------+
                |
                | Metrics scrape
                v
+--------------------------+       +--------------------------+
|   Prometheus (metrics)   | <---- | Grafana (dashboards)     |
+--------------------------+       +--------------------------+

18. Résumé
Domaine	Stack	Statut
Backend	FastAPI + SQLAlchemy + Alembic	✅
Frontend	React + Vite + Tailwind + Query	✅
CI/CD	GitHub Actions + GHCR + Semantic Release	✅
Sécurité	JWT, RBAC, Bandit, Trivy	✅
Monitoring	Prometheus + Grafana	✅
Scaling	Docker → Kubernetes ready	✅
19. Conclusion

Planner v3 atteint le niveau d’une architecture Enterprise Ready :

CI/CD reproductible

Infra observable

Code typé et modulaire

Sécurité par défaut

Scalabilité native

Prochaine version (v4) envisagera :

API GraphQL optionnelle

WebSocket live sync

Feature flags & audit trail

Intégration OpenTelemetry complète