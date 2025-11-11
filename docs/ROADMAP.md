# 🗺️ ROADMAP – Planner Blueprint

> **Version :** 3.x → 4.x Transition Plan  
> **Mise à jour :** Novembre 2025  
> **Responsable produit :** planner-core@planner.dev

---

## 🎯 Objectif
Cette roadmap décrit la trajectoire d’évolution du projet **Planner Blueprint** sur les 12 prochains mois.  
Elle vise à renforcer la **scalabilité**, la **sécurité**, et l’**observabilité**, tout en ajoutant des fonctionnalités orientées productivité.

---

## ✅ Étapes réalisées (v3.0 – 2025)
| Domaine | Réalisation | Statut |
|----------|--------------|--------|
| **Architecture** | Monorepo complet backend + frontend | ✅ |
| **CI/CD** | GitHub Actions unifié (lint, test, build, release) | ✅ |
| **Sécurité** | Bandit, Trivy, npm audit intégrés | ✅ |
| **Observabilité** | Prometheus + Grafana opérationnels | ✅ |
| **Docs** | Nouvelle structure `/docs/blueprint_v3` | ✅ |

---

## 🧭 Feuille de route v4 (2026)

### 🔹 Q1 2026 – Performance & API
- [ ] Migration vers **FastAPI 0.120+**.
- [ ] Adoption du **pattern Repository/Service** généralisé.
- [ ] Ajout d’une **API GraphQL Gateway** (Ariadne).
- [ ] Optimisation SQLAlchemy (bulk inserts, caching).

### 🔹 Q2 2026 – Temps réel & Observabilité avancée
- [ ] **WebSocket notifications** en direct (FastAPI WebSocket / Socket.IO).
- [ ] Intégration **OpenTelemetry** (trace complète backend + frontend).
- [ ] Centralisation des logs via **Grafana Loki**.
- [ ] Ajout dashboard "User Activity" + alertes Slack/Teams.

### 🔹 Q3 2026 – Scalabilité & Sécurité
- [ ] Migration vers **Kubernetes (Helm chart)**.
- [ ] Auto-scaling HPA + readiness probes.
- [ ] Ajout d’un **service d’audit trail** (traçabilité actions).
- [ ] Intégration **Keycloak** ou **Auth0** pour SSO.

### 🔹 Q4 2026 – UX & Gouvernance
- [ ] Mise en place d’un **Design System React** (Storybook + shadcn/ui).
- [ ] Publication du portail doc Docusaurus.
- [ ] Introduction des **Feature Flags** (config runtime).
- [ ] Mise à jour de la gouvernance : RFCs, conventions Git, release cadence.

---

## 🧩 Innovations futures (v5+)
| Piste | Description |
|--------|--------------|
| **Edge Computing** | Optimisation CDN & exécution front/server side. |
| **Machine Learning** | Suggestions planification via modèles légers. |
| **Multi-tenancy avancé** | Isolement data par organisation (schemas Postgres). |
| **Infrastructure as Code (IaC)** | Terraform + GitOps (ArgoCD). |
| **Zero Trust Security** | Renforcement RBAC + secrets dynamiques. |

---

## 📅 Milestones visuels

```
Q1 ───── API + GraphQL + Cache
Q2 ───── WebSocket + OpenTelemetry
Q3 ───── Kubernetes + Audit Trail
Q4 ───── UX + Docs + Feature Flags
```

---

## 🧠 Objectif final (v4.0)
> Un monorepo **100% observable**, **auto-scalable**, et **sécurisé**,  
> prêt pour le déploiement sur **Kubernetes** et **Cloud hybride**.

---

## 📘 Suivi de la roadmap
Les évolutions sont traquées via GitHub Projects :  
👉 [https://github.com/org/planner/projects/v4](https://github.com/org/planner/projects/v4)

---

