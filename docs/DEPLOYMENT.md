# 🚀 DEPLOYMENT GUIDE – Planner Blueprint v3

> **Version :** 3.0  
> **Dernière mise à jour :** Novembre 2025  
> **Auteur :** Planner DevOps Team  
> **Statut :** Stable

---

## 🎯 Objectif
Ce guide décrit les étapes nécessaires pour déployer **Planner Blueprint v3** dans différents environnements :  
- **Local (Docker Compose)**  
- **Staging (GitHub Actions + Compose)**  
- **Production (Kubernetes via Helm)**

---

## 🧱 1. Prérequis
| Outil | Version minimale | Rôle |
|--------|------------------|------|
| Docker | 24.x | Conteneurisation |
| Docker Compose | 3.9 | Orchestration locale |
| Python | 3.12 | Backend |
| Node.js | 20.x | Frontend |
| GitHub CLI | 2.0+ | Déploiement CI/CD |
| kubectl | 1.30+ | Gestion Kubernetes |
| Helm | 3.14+ | Déploiement chart |

---

## 🧩 2. Déploiement local (Docker Compose)

### Étapes
```bash
git clone https://github.com/org/planner.git
cd planner
scripts/sh/init_repo.sh
make up
```

### Vérification
- Backend : [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)  
- Frontend : [http://localhost:5173](http://localhost:5173)  
- Prometheus : [http://localhost:9090](http://localhost:9090)  
- Grafana : [http://localhost:3000](http://localhost:3000)

### Commandes utiles
| Commande | Description |
|-----------|--------------|
| `make down` | Arrête tous les services |
| `make logs` | Suivi des logs en temps réel |
| `make rebuild` | Rebuild complet du stack |
| `make seed` | Données d’exemple en DB |
| `make smoke` | Test de santé rapide |

---

## ⚙️ 3. Déploiement staging (CI/CD)

### Configuration GitHub
Créer les secrets suivants :
| Nom | Exemple | Utilisation |
|------|----------|-------------|
| `JWT_SECRET` | `supersecretkey` | Auth backend |
| `DATABASE_URL` | `postgresql+asyncpg://user:pass@db:5432/app` | Connexion DB |
| `REDIS_URL` | `redis://redis:6379/0` | Cache & queue |
| `GRAFANA_PASS` | `admin` | Monitoring |

### Workflow concerné
`.github/workflows/deploy.yml`  
→ Build & push images Docker vers **GHCR**.

### Déploiement staging
```bash
gh workflow run deploy.yml -f environment=staging
```

Images disponibles sur :  
`ghcr.io/org/planner/backend:staging`  
`ghcr.io/org/planner/frontend:staging`

---

## ☁️ 4. Déploiement production (Kubernetes)

### 4.1 Structure Helm Chart
```
helm/planner/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── postgres.yaml
│   ├── redis.yaml
│   └── ingress.yaml
```

### 4.2 Installation
```bash
helm install planner helm/planner -n planner --create-namespace
```

### 4.3 Mise à jour
```bash
helm upgrade planner helm/planner -n planner
```

### 4.4 Suppression
```bash
helm uninstall planner -n planner
```

---

## 🔐 5. Sécurité production

- **HTTPS obligatoire** via ingress (cert-manager ou Traefik).  
- Secrets Kubernetes stockés sous forme d’objets `Secret`.  
- JWT signés côté backend.  
- Liveness/readiness probes sur tous les pods.  
- Backups PostgreSQL automatiques (`pg_dump` + `cronjob`).  
- Scans Trivy intégrés à la pipeline avant déploiement.  

---

## 📊 6. Monitoring et Observabilité

| Service | Port | Description |
|----------|------|--------------|
| **Prometheus** | 9090 | Collecte métriques backend |
| **Grafana** | 3000 | Dashboards (API, worker, DB) |
| **Loki** | 3100 | Centralisation des logs |
| **Alertmanager** | 9093 | Alertes système |

Dashboards recommandés :  
- Latence API (p95, p99)  
- Erreurs HTTP 4xx/5xx  
- Charge CPU par pod  
- Jobs RQ en attente  

---

## 🧩 7. Stratégie de rollback
En cas d’échec :
```bash
helm rollback planner <num_release>
```
ou pour Docker Compose :
```bash
make down && make up
```

---

## 🧠 8. Bonnes pratiques DevOps
- Toujours déployer depuis une release taguée (`vX.Y.Z`).  
- Jamais de `latest` en production.  
- Séparer les environnements (staging/prod).  
- Conserver 5 releases Helm maximum.  
- Monitorer les erreurs dans Grafana + logs Loki.

---

## 📦 9. Déploiement manuel simplifié
```bash
docker compose --profile prod up -d --build
```
> Utilisé pour environnements restreints sans CI/CD.

---

## 📘 10. Ressources externes
- [Helm Documentation](https://helm.sh/docs/)  
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)  
- [Grafana Loki](https://grafana.com/oss/loki/)  
- [Kubernetes Best Practices](https://kubernetes.io/docs/setup/best-practices/)

---

## ✅ 11. Validation post-déploiement
Vérification automatisée via :
```bash
scripts/sh/smoke.sh
```
Critères :
- API `/health` → 200 OK  
- Frontend répond sur port 5173  
- Worker RQ opérationnel  
- DB connectée (migration OK)

---

## 🏁 12. Fin de déploiement
Si toutes les vérifications sont vertes →  
✅ Déploiement validé et version marquée comme **Release Stable**.

---
