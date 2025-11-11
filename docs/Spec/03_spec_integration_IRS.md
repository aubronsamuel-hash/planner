# 📘 Spécification d’Intégration (IRS) – Planner Blueprint v3
**Codex Edition – 2025.11**

---

## 1️⃣ Objet du document
Ce document décrit les flux d’intégration et les interactions entre les composants de l’application **Planner Blueprint v3**, ainsi que les systèmes externes auxquels elle peut être connectée.  
Il complète les documents SRS et TRS en précisant les **interfaces, protocoles, formats et sécurités d’échange**.

**Nom du produit :** Planner Blueprint v3  
**Version :** 3.0  
**Auteur :** Planner DevOps / Codex  
**Statut :** Final  
**Portée :** Backend ↔ Frontend ↔ Services ↔ Monitoring ↔ CI/CD  

---

## 2️⃣ Périmètre d’intégration
| Domaine | Intégration | Description |
|----------|--------------|-------------|
| **Backend ↔ Frontend** | REST JSON | Échanges API sécurisés JWT |
| **Backend ↔ DB (PostgreSQL)** | Async ORM | Lecture/écriture, migrations Alembic |
| **Backend ↔ Redis** | Cache + Queue | RQ Worker, cache missions et sessions |
| **Worker ↔ Backend** | Redis Queue | Jobs async (emails, rapport, sync) |
| **Monitoring** | Prometheus / Grafana / Loki | Métriques et logs centralisés |
| **CI/CD ↔ Infra** | GitHub Actions + GHCR | Build, tests, déploiement Docker |
| **API externes (optionnelles)** | Webhooks REST | Connecteurs SaaS (Slack, Notion...) |

---

## 3️⃣ Diagramme de flux global

```
             ┌──────────────┐
             │   Frontend   │
             │ React + Vite │
             └──────┬───────┘
                    │ REST / JSON
                    ▼
          ┌─────────────────────┐
          │     Backend API     │
          │ FastAPI + SQLA + RQ │
          └────────┬────────────┘
                   │ Async Queue
     ┌─────────────┼──────────────┐
     │             │              │
     ▼             ▼              ▼
PostgreSQL       Redis          Worker (RQ)
(DB)             (Cache/Queue)  (Emails, Metrics)
     │                             │
     └───────────────┬─────────────┘
                     ▼
             Monitoring Stack
     (Prometheus + Grafana + Loki)
```

---

## 4️⃣ Frontend ↔ Backend

### 4.1 Protocoles
- **HTTP/1.1 ou HTTP/2**  
- **Format JSON UTF-8**  
- **Authentification JWT (header Authorization: Bearer)**  
- **Compression gzip** activée côté backend  

### 4.2 Exemples de requêtes

**GET /missions**
```http
GET /api/v1/missions
Authorization: Bearer eyJhbGciOi...
```
**Response**
```json
[
  { "id": 1, "title": "Mission Alpha", "status": "active" }
]
```

**POST /timesheets**
```http
POST /api/v1/timesheets
Content-Type: application/json
Authorization: Bearer eyJhbGciOi...
```
```json
{ "mission_id": 3, "hours": 8, "week": "2025-W45" }
```

---

## 5️⃣ Backend ↔ PostgreSQL

### 5.1 Connexion
- Driver : `asyncpg`  
- Pool : 10 connexions par worker  
- Timeout : 30 secondes  
- Schéma : `public` (extensible multi-tenant v4)  

### 5.2 Stratégies
- Lecture / écriture async via SQLAlchemy.  
- Transactions automatiques.  
- FK cascade et rollback transactionnel.  
- Journalisation via middleware SQLAlchemy logger.  

### 5.3 Intégrité
- Contraintes `NOT NULL`, `CHECK` et `UNIQUE`.  
- Index sur `status`, `email`, `mission_id`.  
- Audits automatiques (`updated_at`, `modified_by`).  

---

## 6️⃣ Backend ↔ Redis

### 6.1 Usage
- **Cache** : sessions utilisateur, tokens, requêtes fréquentes.  
- **Queue** : jobs RQ pour envoi d’emails, notifications, exports.  
- **Pub/Sub** : mécanisme temps réel interne (v4).  

### 6.2 Configuration
- URI : `redis://redis:6379/0`  
- TTL sessions : 3600s  
- Format de stockage : JSON sérialisé  

### 6.3 Exemple de tâche RQ
```python
@rq.job
def send_email(to, subject, content):
    smtp.send(to=to, subject=subject, body=content)
```

---

## 7️⃣ Backend ↔ Worker

### 7.1 Flux
1. API crée un job asynchrone  
2. Job ajouté à la file Redis  
3. Worker RQ exécute le job  
4. Résultat stocké / logué  

### 7.2 Types de jobs
| Type | Description |
|-------|--------------|
| Email | Notification utilisateur |
| Report | Génération rapport PDF |
| Metrics | Agrégation données monitoring |
| Export | Génération CSV mission/timesheet |

---

## 8️⃣ Monitoring stack

| Composant | Rôle | Port | Description |
|------------|------|------|--------------|
| **Prometheus** | Scrape `/metrics` | 9090 | Collecte métriques backend/worker |
| **Grafana** | Dashboards | 3000 | Visualisation (temps, erreurs) |
| **Loki** | Centralisation logs | 3100 | JSON logs unifiés |
| **Alertmanager** | Notifications | 9093 | Alertes > Slack / Email |

### 8.1 Exposition métriques
Backend expose :
```
/metrics
  http_requests_total
  http_request_duration_seconds
  rq_jobs_total
```

---

## 9️⃣ CI/CD ↔ Environnements

### 9.1 Workflows GitHub Actions
```
.github/workflows/
├── lint.yml
├── test.yml
├── deploy.yml
```

### 9.2 Variables GitHub
| Nom | Description | Environnement |
|------|--------------|---------------|
| `JWT_SECRET` | Clé JWT | staging/prod |
| `DATABASE_URL` | Connexion DB | tous |
| `REDIS_URL` | Cache et queue | tous |
| `GHCR_TOKEN` | Auth Docker Registry | prod |
| `GRAFANA_PASS` | Accès monitoring | prod |

### 9.3 Étapes CI
1. Lint → tests → build → push GHCR  
2. Release semantic → déploiement staging  
3. Vérification automatisée `/health`  

---

## 🔟 API externes (optionnelles)

| Intégration | Type | Endpoint | Usage |
|--------------|------|-----------|-------|
| **Slack** | Webhook POST | `/webhook/slack` | Notifications activité |
| **Notion / ClickUp** | REST API | `/sync/tasks` | Synchronisation tâches |
| **SMTP / SendGrid** | Email | `/notify/email` | Communication utilisateurs |

### Exemple webhook Slack
```json
{
  "text": "Nouvelle mission assignée à Alice - Mission Alpha"
}
```

---

## 11️⃣ Format des échanges

| Format | Utilisation |
|---------|--------------|
| **JSON** | API standard |
| **CSV** | Exports mission/timesheet |
| **PDF** | Rapports managers |
| **YAML** | Config CI/CD |
| **PromQL** | Monitoring Prometheus |

---

## 12️⃣ Sécurité d’intégration

| Domaine | Politique |
|----------|-----------|
| Auth API | JWT + HTTPS obligatoire |
| CORS | Restreint au domaine frontend |
| Logs | Aucun secret dans logs |
| CI/CD | Secrets GitHub uniquement |
| Monitoring | Accès restreint via Basic Auth |
| Webhooks | Signature HMAC obligatoire |

---

## 13️⃣ Synchronisation des environnements

| Environnement | Description | Services |
|----------------|--------------|-----------|
| **Local (dev)** | Docker Compose complet | backend, frontend, db, redis |
| **Staging** | GitHub Actions CI/CD | build & test auto |
| **Production** | Helm + Kubernetes | scalable, monitoring |
| **Monitoring** | Prometheus + Grafana | global metrics |

---

## 14️⃣ Résilience et reprise

| Scénario | Mécanisme |
|-----------|------------|
| DB down | Retry avec backoff (FastAPI middleware) |
| Worker fail | Retry RQ avec logs |
| API crash | Auto-restart Docker / K8s |
| File Redis saturée | Purge TTL auto |
| CI/CD fail | Rerun auto via GitHub API |

---

## 15️⃣ Diagramme d’interaction (séquence simplifiée)

```
Frontend → Backend → Redis → Worker → PostgreSQL
       ↘──────────── Prometheus ←────────────↙
```

---

## 16️⃣ Règles d’intégration

| ID | Règle | Type |
|----|--------|------|
| INT-001 | Toute API doit exposer `/health` | Système |
| INT-002 | Les jobs RQ doivent être idempotents | Worker |
| INT-003 | Les exports ne doivent pas contenir d’identifiants sensibles | Sécurité |
| INT-004 | Les workflows CI ne pushent que sur tag semver | CI/CD |
| INT-005 | Les endpoints REST doivent être versionnés `/api/v1/...` | API |

---

## 17️⃣ Tests d’intégration

### Objectif :
Valider le bon fonctionnement inter-systèmes :
- API ↔ DB  
- API ↔ Redis  
- Worker ↔ Queue  
- Monitoring ↔ Prometheus  

### Exécution :
```bash
pytest -m integration
```

---

## 18️⃣ Métriques clés à suivre

| Nom | Type | Objectif |
|------|------|-----------|
| `http_request_duration_seconds` | Histogramme | Latence API |
| `rq_jobs_failed_total` | Counter | Fiabilité jobs |
| `db_query_time_seconds` | Histogramme | Performance SQL |
| `cache_hits_total` | Counter | Efficacité cache |

---

## 19️⃣ Annexes
- Diagrammes détaillés dans `architecture_v3.md`  
- Liste des endpoints : `openapi.json` auto-généré  
- CI/CD logs : GitHub Actions → Tab “Runs”  
