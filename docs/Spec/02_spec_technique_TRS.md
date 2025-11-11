# 📗 Spécification Technique (TRS) – Planner Blueprint v3
**Codex Edition – 2025.11**

---

## 1️⃣ Objet du document
Ce document présente la conception technique détaillée du système **Planner Blueprint v3**, en décrivant ses composants, technologies, interfaces, contraintes, et exigences techniques.  
Il s’adresse aux développeurs, architectes, DevOps, et systèmes automatisés (Codex).

**Nom du produit :** Planner Blueprint v3  
**Version :** 3.0  
**Auteur :** Planner Core Team  
**Statut :** Final – Stable  
**Langues de référence :** Python / TypeScript / YAML  

---

## 2️⃣ Architecture technique générale

### 2.1 Vue globale

```
        ┌─────────────────────┐
        │     Frontend SPA    │
        │ React + Vite + TS   │
        └────────┬────────────┘
                 │ (HTTP/JSON)
                 ▼
        ┌─────────────────────┐
        │   Backend API       │
        │ FastAPI + SQLA + RQ │
        └────────┬────────────┘
                 │ (Async IO)
        ┌────────┴────────┐
        │ PostgreSQL DB   │
        │ Redis (Cache/Q) │
        └─────────────────┘
                 │
        ┌────────▼────────┐
        │ Monitoring Stack│
        │ Prometheus/Graf │
        └─────────────────┘
```

L’infrastructure est **conteneurisée via Docker Compose** et déployable sur **Kubernetes (Helm)**.

---

## 3️⃣ Technologies utilisées

| Domaine | Outil / Framework | Rôle |
|----------|------------------|------|
| Backend | **FastAPI 0.115+** | API REST & async services |
| ORM | **SQLAlchemy 2.x** + Alembic | ORM et migrations |
| DB | **PostgreSQL 16** | Stockage principal |
| Cache / Queue | **Redis 7.x** | Cache + file RQ |
| Frontend | **React 18 + Vite + TypeScript** | Interface utilisateur |
| UI Kit | **Shadcn/UI + TailwindCSS** | Design system |
| Tests | **Pytest / Vitest / MSW** | Tests unitaires et mocks |
| CI/CD | **GitHub Actions + GHCR + Codecov** | Pipelines et déploiement |
| Sécurité | **Bandit / Trivy / npm audit** | Analyse et durcissement |
| Observabilité | **Prometheus + Grafana + Loki** | Monitoring & logs |
| Infrastructure | **Docker Compose / Helm** | Orchestration et déploiement |

---

## 4️⃣ Structure du dépôt

```
planner/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── worker/
│   │   └── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── tests/
│   ├── vite.config.ts
│   └── package.json
├── infra/
│   ├── docker-compose.yml
│   ├── helm/
│   ├── prometheus.yml
│   └── grafana/
├── docs/
└── scripts/
```

---

## 5️⃣ Composants backend (FastAPI)

### 5.1 Structure logique
| Module | Description |
|---------|--------------|
| `api/` | Routes REST (auth, missions, users, timesheets) |
| `core/` | Config, dépendances, sécurité |
| `models/` | ORM SQLAlchemy |
| `schemas/` | Modèles Pydantic |
| `services/` | Logique métier |
| `worker/` | Jobs asynchrones RQ |
| `tests/` | Tests unitaires et d’intégration |

### 5.2 Exemple de route
```python
@router.post("/missions", response_model=MissionOut)
async def create_mission(mission: MissionIn, user: User = Depends(current_user)):
    return await MissionService.create(mission, user)
```

---

## 6️⃣ Base de données

### 6.1 Schéma SQL principal
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE missions (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  start_date DATE,
  end_date DATE,
  status VARCHAR(20)
);

CREATE TABLE assignments (
  id SERIAL PRIMARY KEY,
  mission_id INT REFERENCES missions(id),
  person_id INT REFERENCES persons(id)
);
```

### 6.2 Contraintes techniques
- Index sur `mission_id`, `person_id`  
- FK ON DELETE CASCADE  
- UUID supporté (PostgreSQL `uuid-ossp`)  
- Timezone UTC+0 par défaut  

---

## 7️⃣ API REST

### 7.1 Endpoints principaux

| Ressource | Méthode | Endpoint | Auth | Description |
|------------|----------|-----------|------|-------------|
| Auth | POST | `/auth/login` | ❌ | Connexion |
| Users | GET | `/users/me` | ✅ | Profil courant |
| Missions | GET | `/missions` | ✅ | Liste missions |
| Missions | POST | `/missions` | ✅ | Création |
| Timesheets | POST | `/timesheets` | ✅ | Enregistrement temps |
| Notifications | GET | `/notifications` | ✅ | Historique |

### 7.2 Format de réponse
```json
{
  "id": 12,
  "title": "Mission Alpha",
  "status": "active",
  "assignees": ["user1", "user2"]
}
```

---

## 8️⃣ Sécurité technique

| Domaine | Mesure |
|----------|--------|
| Authentification | JWT (HS256) |
| Autorisation | RBAC via dépendance `Depends(current_user)` |
| Hashage | bcrypt (passlib) |
| Validation | Pydantic (niveau modèle) |
| Sécurité réseau | HTTPS, CORS restrictif |
| CI/CD | Scans Bandit + Trivy |
| DB | Connexion SSL obligatoire |
| Secrets | GitHub Secrets + .env |

---

## 9️⃣ Frontend

### 9.1 Arborescence
```
src/
├── components/
├── pages/
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── Missions.tsx
│   └── Timesheets.tsx
├── services/
├── hooks/
└── store/
```

### 9.2 Gestion d’état
- `React Query` pour la synchronisation API  
- `Context API` pour l’état global utilisateur  
- `Zustand` (optionnel) pour stores légers  

### 9.3 Sécurité côté front
- Intercepteur Axios pour token JWT  
- Redirection automatique sur 401  
- Token stocké dans `sessionStorage`  

---

## 🔟 Tests et qualité

| Domaine | Outil | Commande |
|----------|--------|----------|
| Backend tests | Pytest | `pytest` |
| Frontend tests | Vitest + React Testing Library | `npm run test` |
| Lint Python | Ruff | `ruff check .` |
| Lint JS | ESLint | `npm run lint` |
| Coverage | Codecov | CI automatique |

---

## 11️⃣ Performance & optimisation

- Caching Redis sur endpoints fréquents `/missions` et `/users/me`.  
- Index DB sur champs critiques (`status`, `email`).  
- Compression gzip activée.  
- Lazy loading côté React.  
- Build Vite optimisé (`esbuild`).  

---

## 12️⃣ Monitoring et logs

| Composant | Description |
|------------|--------------|
| **Prometheus** | Scrape `/metrics` backend |
| **Grafana** | Dashboards API, DB, Worker |
| **Loki** | Logs JSON centralisés |
| **RQ Dashboard** | Monitoring des jobs asynchrones |

---

## 13️⃣ CI/CD Pipeline

```
.github/workflows/
├── lint.yml
├── test.yml
├── deploy.yml
```

### Étapes typiques :
1. Lint Python/JS  
2. Tests unitaires + coverage  
3. Build Docker images  
4. Push vers GHCR  
5. Release via Semantic Release  

---

## 14️⃣ Exigences système

| Domaine | Exigence |
|----------|-----------|
| Serveur API | 2 vCPU / 2Go RAM minimum |
| DB | 10Go stockage min |
| Worker | 1 CPU / 512Mo RAM |
| Monitoring | Prometheus + Grafana |
| OS recommandé | Ubuntu 22.04 LTS |

---

## 15️⃣ Sécurité avancée
- CSP headers (`default-src 'self'`)  
- Séparation front/back en domaines distincts  
- HTTPS obligatoire  
- `helmet` sur Node proxy  
- Validation stricte des entrées (XSS / SQLi)  

---

## 16️⃣ Maintenabilité
- Code modulaire, typé (MyPy + TS strict).  
- Documentation générée via `mkdocs` ou `pdoc`.  
- Conventions PEP8 et ESLint Airbnb.  
- Tests CI obligatoires avant merge.  

---

## 17️⃣ Annexes
- **Schéma d’architecture complet** : voir `architecture_v3.md`.  
- **Modèles OpenAPI** : `/docs` (FastAPI auto).  
- **Ports exposés :**
  - API : 8000  
  - Front : 5173  
  - Prometheus : 9090  
  - Grafana : 3000  
