# 📚 API Reference – Planner Backend Authentication

This document summarises the key authentication endpoints now powered by the
async SQLAlchemy + Redis stack delivered in Planner Blueprint v3.1-Recovery.

## 🔐 Authentication Workflow

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | `POST` | Create a new user and persist the record in PostgreSQL via the async session factory. |
| `/api/v1/auth/login` | `POST` | Validate credentials, issue a JWT access token (HS256) with a Redis-backed JTI, and persist a refresh token hash. |
| `/api/v1/auth/refresh` | `POST` | Rotate refresh + access tokens. Revokes the previous access token’s JTI and ensures Redis TTL alignment with SQL expiry. |
| `/api/v1/auth/logout` | `POST` | Requires a bearer token and refresh token. Revokes both the refresh token hash and the active access token JTI. |
| `/api/v1/auth/me` | `GET` | Returns the authenticated user profile using an async database session dependency. |

### Token Management
- Access tokens are signed with `HS256` and include a `jti` claim stored in
  Redis with a TTL equal to the access token lifetime.
- Refresh tokens are stored hashed (SHA-256) in PostgreSQL with matching Redis
  cache entries for fast revocation checks.
- Logout and refresh flows revoke associated JTIs, preventing replay attacks.

## ⚙️ Dependencies
- **Database:** `postgresql+asyncpg` (configurable; tests use SQLite for speed).
- **Cache:** Redis (supports `fakeredis://` for local development and tests).
- **Migrations:** Alembic asynchronous environment (`alembic upgrade head`).

Refer to the backend README for bootstrap instructions and to `docs/CHANGELOG.md`
for the release notes of the recovery build.
