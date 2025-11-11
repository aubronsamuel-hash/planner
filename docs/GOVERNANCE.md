# 🧭 GOVERNANCE – Planner Blueprint

> **Version :** 3.x  
> **Mise à jour :** Novembre 2025  
> **Mainteneur principal :** @you  
> **Statut :** Actif  

---

## 🎯 1. Objectif
Ce document définit la gouvernance technique, les processus décisionnels et les standards organisationnels du projet **Planner Blueprint**.  
Il assure une gestion collaborative, transparente et durable du code source, des versions et des contributions.

---

## 🧑‍💻 2. Rôles et responsabilités

| Rôle | Description | Responsabilités principales |
|------|--------------|-----------------------------|
| **Mainteneur principal** | Garant technique du blueprint | Revue des PR, validation releases |
| **Dev Backend** | API, DB, Auth, CI | Code FastAPI + tests |
| **Dev Frontend** | UI, UX, React, State | Composants, tests, intégration |
| **DevOps** | Infra, Docker, Observabilité | Pipelines, sécurité, scaling |
| **QA / Testeur** | Validation, couverture, non-régressions | CI tests + rapports |
| **Product Owner** | Vision & roadmap | Priorisation et release notes |

---

## ⚙️ 3. Structure organisationnelle

```
planner/
├── backend/
├── frontend/
├── infra/
├── scripts/
└── docs/
```

Chaque module est **indépendant** mais synchronisé via le monorepo et la CI/CD.

---

## 📋 4. Processus de contribution

1. **Créer une issue** (bug, feature, documentation).  
2. **Créer une branche** à partir de `develop` :
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
3. **Coder & tester** localement (`make test`, `make lint`).  
4. **Créer une Pull Request** vers `develop`.  
5. **Reviewer obligatoire** (au moins 1 membre du core team).  
6. **Merge** → déclencheur automatique de pipeline CI/CD.  

---

## 📦 5. Branches & Releases

| Branche | Rôle | Description |
|----------|------|-------------|
| `main` | Production | Stable, publiée |
| `develop` | Pré-production | Dernières features validées |
| `feature/*` | Dev fonctionnel | Nouvelles fonctionnalités |
| `fix/*` | Correctifs | Bugs urgents |
| `release/*` | Préparation release | Versions figées pour tests |
| `hotfix/*` | Patches rapides | Correctifs urgents sur `main` |

Releases générées automatiquement par **Semantic Release**.

---

## 🧩 6. Versioning
- **Standard SemVer** : MAJOR.MINOR.PATCH  
- Exemple : `0.3.0`  
- Version mise à jour via :
  ```bash
  npx semantic-release
  ```

---

## 🔍 7. Revue de code

Critères d’acceptation d’une Pull Request :
- ✅ Tests unitaires passent (CI verte).
- ✅ Lint sans erreur.
- ✅ Code documenté (docstring / JSDoc).
- ✅ Nom de commit conforme (conventional commits).
- ✅ Aucune variable sensible ni code mort.

---

## 🧱 8. Gouvernance technique

| Domaine | Outil | Règle |
|----------|--------|-------|
| **Langage backend** | Python 3.12 | Typage strict, async |
| **Langage frontend** | TypeScript | Hooks + components typed |
| **Tests** | Pytest / Vitest | Coverage > 70% |
| **CI/CD** | GitHub Actions | Validation automatique |
| **Sécurité** | Bandit / Trivy | Aucun “High” accepté |
| **Docs** | Markdown / Docusaurus | À jour sur chaque merge |

---

## 🧠 9. Prise de décision
Les décisions techniques se prennent via le modèle RFC :

1. Création d’un **RFC** (Request For Comments) dans `/docs/rfcs/`.  
2. Discussion (pull request + review).  
3. Vote de l’équipe core : majorité simple.  
4. Validation → intégration roadmap.

---

## 🧩 10. Gouvernance communautaire
- Respect de la charte de conduite (basée sur Contributor Covenant).  
- Aucune discrimination ni harcèlement tolérés.  
- Discussions via Slack #planner-dev ou GitHub Discussions.  
- Mentorat encouragé pour les nouveaux contributeurs.  

---

## 🧾 11. Transparence & Reporting
- Releases publiques (CHANGELOG.md).  
- Rapports sécurité (`SECURITY.md`).  
- Roadmap ouverte (`ROADMAP.md`).  
- Historique complet des PRs et Issues GitHub.  

---

## 🏁 12. Révocation et transfert
Le mainteneur principal peut déléguer son rôle après vote du core team.  
En cas d’inactivité prolongée (>3 mois), un transfert de gouvernance est initié.

---

## 📚 13. Références
- [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/)  
- [Semantic Versioning](https://semver.org/lang/fr/)  
- [Contributor Covenant](https://www.contributor-covenant.org/)  
- [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)  
