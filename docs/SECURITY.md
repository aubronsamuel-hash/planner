# 🔒 SECURITY POLICY – Planner Blueprint

> **Version :** v3.0 (2025-11-11)
> **Responsable sécurité :** planner-security@planner.dev
> **Statut :** Actif

---

## 🧩 1. Objectif
Cette politique définit les règles de sécurité applicables au projet **Planner Blueprint v3**.  
Elle vise à garantir la confidentialité, l’intégrité et la disponibilité du code, des données et des environnements de développement.

---

## 🧱 2. Versions supportées

| Version | Support | Statut |
|----------|----------|--------|
| 0.3.x | ✅ | Active |
| 0.2.x | ⚠️ | En phase de migration |
| 0.1.x | ❌ | Obsolète |

Les correctifs de sécurité sont appliqués uniquement aux branches `main` et `release/*` de la version active.

---

## 🛡️ 3. Standards de sécurité

### Authentification & Autorisation
- JWT (HS256) avec clé secrète stockée dans les **GitHub Secrets**.
- Durée d’expiration des tokens : 60 min.
- Hachage des mots de passe via **bcrypt** (`passlib`).
- RBAC (Role-Based Access Control) pour les endpoints sensibles.

### Réseau & Communication
- Toutes les communications passent par **HTTPS**.
- CORS restreint au domaine frontend officiel.
- Reverse proxy recommandé (Traefik ou NGINX).

### Stockage & Données
- PostgreSQL : chiffrement en transit (SSL activé).
- Aucune donnée sensible ne doit être en clair dans les dumps SQL.
- Backups encryptés via `pg_dump -Fc`.

### CI/CD
- Scans automatisés à chaque push :
  - **Trivy** : analyse de vulnérabilités Docker/images.
  - **Bandit** : analyse statique Python.
  - **npm audit** : vérification des dépendances JS.
- Caches `pip` et `npm` isolés par build runner.

### Secrets Management
- Fichiers `.env` ignorés par Git.
- Secrets stockés dans GitHub → `Settings > Secrets and Variables`.
- Accès restreint par repository et environnement (staging/prod).

### Observabilité & Logs
- Logs structurés JSON (niveau INFO/ERROR).
- Pas de données personnelles dans les logs.
- Accès monitoring limité (Prometheus + Grafana en mode privé).

---

## ⚠️ 4. Signalement de vulnérabilités

Merci de **ne pas publier publiquement** de vulnérabilité avant correctif.  
Signalez toute faille à :
```
📧  security@planner.dev
```
ou via issue privée GitHub (`Security Advisory`).

**Délai de réponse :** 72 heures ouvrées maximum.

---

## 🧰 5. Bonnes pratiques pour les contributeurs
- Ne jamais commit de secrets (API key, password, token).
- Toujours utiliser `.env.local` pour le développement.
- Vérifier les dépendances avec :
  ```bash
  pip list --outdated
  npm audit
  ```
- Lancer les scans avant push :
  ```bash
  make lint && make test
  ```

---

## 🧾 6. Réponse aux incidents
- Étape 1 : Identification du problème (logs, métriques).
- Étape 2 : Contention (rollback, isolation du conteneur).
- Étape 3 : Correction et patch.
- Étape 4 : Publication d’un **Security Advisory**.
- Étape 5 : Post-mortem documenté.

---

## 🧩 7. Références
- [OWASP Top 10 – 2025](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks Docker & Kubernetes](https://www.cisecurity.org/benchmark/docker)
- [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)
