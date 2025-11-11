# 📘 Spécification Fonctionnelle (SRS) – Planner Blueprint v3

**Codex Edition – 2025.11**

---

## 1. Objet du document

Ce document décrit l’ensemble des besoins fonctionnels, acteurs, exigences et règles de gestion du système **Planner Blueprint v3**.
Il est destiné à guider la conception, le développement et les tests automatisés de l’application.

**Nom du produit :** Planner Blueprint v3  
**Version :** 3.0  
**Auteur :** Planner Core Team  
**Statut :** Final  
**Public visé :** Équipes Dev, QA, Ops, et Codex (agent génératif).

---

## 2. Contexte général

Planner Blueprint v3 est une application web de **gestion opérationnelle** permettant de :

- Planifier des missions, personnes et ressources.  
- Gérer des utilisateurs et rôles (RBAC).  
- Suivre le temps et les activités (timesheets).  
- Centraliser la communication et les notifications.  
- Fournir un tableau de bord analytique.  

L’objectif est d’obtenir un **SaaS modulaire, performant, sécurisé et extensible**.

---

## 3. Description du système

### 3.1 Vue d’ensemble

Le système est composé de trois couches principales :

1. **Frontend** : application SPA (React + Vite + TypeScript).  
2. **Backend API** : FastAPI + PostgreSQL + Redis.  
3. **Worker asynchrone** : tâches (emails, analytics, notifications).  

Une surcouche DevOps (Docker + CI/CD + Monitoring) assure la cohérence et la reproductibilité.

---

## 4. Acteurs et rôles

| Acteur | Description | Permissions principales |
|---------|--------------|------------------------|
| **Administrateur** | Configure le système, crée les rôles, supervise les utilisateurs | CRUD complet, gestion des rôles |
| **Manager** | Gère les missions, affecte les personnes, valide les feuilles de temps | CRUD missions, validation, reporting |
| **Collaborateur** | Remplit ses missions et son temps de travail | Lecture missions, saisie temps |
| **Observateur** | Accès en lecture seule (audit, reporting) | Lecture globale |
| **System Worker** | Service interne (asynchrone, monitoring) | Tâches automatisées |

---

## 5. Fonctionnalités principales

### 5.1 Gestion des utilisateurs
- Création, édition, désactivation de comptes.  
- Attribution de rôles RBAC (admin, manager, user).  
- Réinitialisation de mot de passe.  
- Authentification JWT (HS256).  
- Audit log : connexion, modification, suppression.

### 5.2 Gestion des missions
- Création de missions avec titre, description, date, statut.  
- Affectation de personnes.  
- Gestion du cycle de vie : *draft → active → done*.  
- Export PDF ou CSV des missions.

### 5.3 Gestion des personnes
- Import / création d’intervenants.  
- Liaison à des missions.  
- Statut actif / inactif.  
- Contact, email, métier, disponibilité.

### 5.4 Timesheets
- Enregistrement du temps passé par mission.  
- Validation par manager.  
- Suivi de la charge hebdomadaire.  
- Rapport d’activité exportable.

### 5.5 Tableau de bord
- Vue synthétique : missions en cours, charge, ressources.  
- Graphiques : charge par personne / projet.  
- Widgets dynamiques (React + ChartJS).

### 5.6 Notifications
- Envoi automatique lors d’une affectation ou validation.  
- Canaux : email (SMTP) + webhook.  
- Historique et statut des envois.

### 5.7 Observabilité intégrée
- Endpoint `/metrics` Prometheus.  
- Statistiques API, workers, DB.  
- Logs JSON structurés.

---

## 6. Règles de gestion (Business Rules)

| Règle | Description |
|--------|-------------|
| RG-001 | Un utilisateur doit avoir au moins un rôle. |
| RG-002 | Une mission doit comporter au moins une personne affectée. |
| RG-003 | Le temps total enregistré par semaine ne peut excéder 60h. |
| RG-004 | Les utilisateurs inactifs ne peuvent pas se connecter. |
| RG-005 | Les rôles “admin” ne peuvent pas être supprimés. |
| RG-006 | Toute modification de mission génère un log d’audit. |
| RG-007 | Les exports ne contiennent pas de données sensibles (ex: tokens). |

---

## 7. Contraintes non fonctionnelles

| Domaine | Exigence |
|----------|-----------|
| Performance | Temps de réponse API < 200ms (95e percentile) |
| Disponibilité | 99.5% uptime |
| Sécurité | OWASP Top 10 conforme |
| Compatibilité | Navigateurs modernes (Chrome, Edge, Firefox) |
| Scalabilité | 1000 requêtes/s soutenues |
| Monitoring | Metrics + logs + traces disponibles |
| Internationalisation | Interface FR/EN (future v4) |

---

## 8. Données et modèles

Les principales entités :

- **User(id, username, email, roles, is_active)**  
- **Role(id, name, permissions)**  
- **Mission(id, title, start_date, end_date, status)**  
- **Person(id, full_name, email, job_title)**  
- **Assignment(id, mission_id, person_id)**  
- **Timesheet(id, person_id, mission_id, hours, week)**  
- **Notification(id, type, status, created_at)**  

Relations principales :

```
User *---* Role
Mission *---* Person (via Assignment)
Person 1---* Timesheet
```

---

## 9. Cas d’usage principaux (UML simplifié)

### UC1 – Authentification
```
Utilisateur → [Login Page]
→ API /auth/login
→ JWT reçu
→ Accès au tableau de bord
```

### UC2 – Création d’une mission
```
Manager → UI "Nouvelle mission"
→ API /missions POST
→ Notification envoyée aux personnes affectées
→ Mission visible dans tableau de bord
```

### UC3 – Validation du temps
```
Collaborateur → Saisie temps (timesheet)
→ Manager valide
→ Rapport hebdo mis à jour
```

---

## 10. Scénarios utilisateurs

### Scénario 1 : Création d’un projet
1. L’administrateur crée un projet.  
2. Il y associe des missions.  
3. Des collaborateurs sont affectés.  
4. Les temps sont saisis et validés.  
5. Un rapport est généré automatiquement.

### Scénario 2 : Monitoring
1. Le worker agrège les logs et métriques.  
2. Prometheus récupère les données `/metrics`.  
3. Grafana les visualise en temps réel.

---

## 11. Interfaces
- **Frontend ↔ API REST (JSON)**  
- **Backend ↔ PostgreSQL (async)**  
- **Backend ↔ Redis (cache + queue)**  
- **Worker ↔ Backend (Redis RQ)**  
- **Monitoring ↔ Prometheus**  

---

## 12. Sécurité fonctionnelle
- Authentification obligatoire (JWT).  
- RBAC appliqué sur chaque endpoint.  
- Logs d’audit pour toute action critique.  
- Politique stricte CORS et headers HTTP.

---

## 13. Conditions de succès
- L’application est **intégralement fonctionnelle via Docker Compose**.  
- Toutes les fonctionnalités métier sont testées.  
- La documentation est complète et à jour.  
- Le pipeline CI/CD déploie automatiquement une image stable.

---

## 14. Évolutions prévues
- Ajout de WebSocket (notifications live).  
- Intégration OpenTelemetry (traçabilité distribuée).  
- Dashboard de productivité par rôle.  
- API GraphQL (lecture seule).

---

## 15. Glossaire

| Terme | Définition |
|--------|-------------|
| Mission | Action planifiée dans un projet |
| Personne | Intervenant interne ou externe |
| Timesheet | Feuille d’heures hebdomadaire |
| Worker | Process asynchrone |
| RBAC | Role-Based Access Control |
| CI/CD | Intégration et déploiement continu |
| Codex | Agent génératif de développement |
