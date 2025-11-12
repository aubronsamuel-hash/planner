# 🧭 Codex Context Sync – Planner Blueprint v3
**Version : 1.0 – Novembre 2025**  
**Auteur : Planner Core Team / Codex Assist**

---

## 1️⃣ Objet du document
Ce document fournit à **Codex** un état global et à jour du projet **Planner Blueprint v3** :
- Contexte fonctionnel (SRS)
- Architecture technique (TRS)
- Intégrations et flux (IRS)
- Étapes de développement à poursuivre
- Règles et politiques de documentation à respecter

Objectif : garantir la **continuité du développement** et la **traçabilité complète** de toutes les actions automatisées ou manuelles.

---

## 2️⃣ État du projet

| Élément | Détail |
|----------|--------|
| Nom du produit | Planner Blueprint v3 |
| Statut | Phase de mise en œuvre |
| Spécifications disponibles | ✅ SRS – ✅ TRS – ✅ IRS |
| Technologies principales | FastAPI, React, PostgreSQL, Redis, RQ, Docker, GitHub Actions |
| Objectif immédiat | Démarrage du développement et documentation automatisée |

---

## 3️⃣ Modules définis dans les spécifications

| Domaine | Composant | État | Description |
|----------|------------|------|-------------|
| **Backend** | Auth, Users, Missions, Timesheets | 🧩 À implémenter | FastAPI + Pydantic + SQLAlchemy |
| **Frontend** | Login, Dashboard, Missions | 🧩 À implémenter | React + Vite + Tailwind |
| **Worker** | Notifications, Exports | 🧩 À implémenter | Redis RQ |
| **DB** | PostgreSQL + Alembic | ⚙️ Schéma validé | Index, contraintes FK |
| **Cache** | Redis | ⚙️ Configurée | Sessions + cache missions |
| **CI/CD** | GitHub Actions + GHCR | 🧩 À activer | Lint / test / build / deploy |
| **Monitoring** | Prometheus + Grafana | 🧩 À brancher | `/metrics` exposé |

---

## 4️⃣ Étapes de développement Codex

1. Générer la base du **backend FastAPI** conforme au TRS.  
2. Créer le **frontend React/Vite/TS** avec Auth et Dashboard.  
3. Construire le **docker-compose.yml** complet (backend, frontend, DB, Redis, Prometheus, Grafana).  
4. Mettre en place la **CI/CD GitHub Actions**.  
5. Connecter le **monitoring** (Prometheus scrape `/metrics`).  
6. Lancer les **tests d’intégration IRS (`pytest -m integration`)**.  
7. Documenter chaque étape (README, docs/).

---

## 5️⃣ Directives Codex

| Domaine | Directive |
|----------|------------|
| Structure | Suivre exactement l’arborescence du TRS |
| Sécurité | JWT obligatoire sur tous les endpoints |
| Tests | `pytest` et `vitest` obligatoires avant merge |
| CI/CD | Workflows `lint.yml`, `test.yml`, `deploy.yml` |
| Monitoring | Endpoint `/metrics` et `/health` obligatoires |
| Documentation | Générer `README.md` + docs/ pour chaque module |
| Versions | Tag semver obligatoire (`v3.x.y`) |

---

## 6️⃣ Politique de Documentation Codex

> Codex doit produire et maintenir une **documentation vivante** à chaque itération du projet.

### 📘 README.md
- Objectif du module  
- Prérequis et dépendances  
- Commandes de build / test / lint  
- Points de vigilance (sécurité, performance)  

### 📂 docs/
| Fichier | Contenu attendu |
|----------|----------------|
| `architecture.md` | Schéma global + composants |
| `api_reference.md` | Endpoints REST `/api/v1` + exemples |
| `deployment.md` | Docker / CI/CD / Environnements |
| `monitoring.md` | Prometheus / Grafana / Alertes |
| `changelog.md` | Journal des versions et commits |

### 🧱 Commentaires de code
- Docstrings PEP257 / JSDoc  
- Référence aux règles SRS (ex: RG-002)  
- Description claire des dépendances et des entrées/sorties  

---

## 7️⃣ Points de contrôle Codex ✅  

### 🔹 Techniques
- [ ] **Docker Compose fonctionnel** (backend, frontend, db, redis, monitoring)  
- [ ] **API `/health` opérationnelle**  
- [ ] **Authentification JWT testée et validée**  
- [ ] **Prometheus détecte `/metrics`**  
- [ ] **Worker RQ opérationnel et supervisé**  
- [ ] **Lint / Tests OK dans la CI/CD**

### 🔹 Documentaires
- [ ] README à jour à la racine et dans chaque module  
- [ ] Dossier `/docs` complet  
- [ ] API documentée (`/docs` FastAPI auto)  
- [ ] Changelog mis à jour  
- [ ] Rapport de couverture visible dans CI  

---

## 8️⃣ Environnement de travail

| Composant | Version |
|------------|----------|
| Python | 3.11+ |
| Node.js | 20+ |
| PostgreSQL | 16 |
| Redis | 7.x |
| Docker | 24+ |
| OS | Ubuntu 22.04 LTS |

---

## 9️⃣ Suivi et maintenance
- Codex doit consigner chaque génération dans le changelog (`/docs/changelog.md`).  
- Les modifications de schémas DB doivent être accompagnées d’un fichier Alembic.  
- Tout ajout de dépendance doit être validé dans CI avant merge.  

---

**Fin du document — Codex Context Sync**
