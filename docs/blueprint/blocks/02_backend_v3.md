⚙️ Block 2 – Backend v3 (FastAPI + PostgreSQL + Redis + Observabilité)
1. Objectifs

API robuste et asynchrone (FastAPI + SQLAlchemy 2.0).

Sécurité JWT complète via python-jose et passlib.

Migrations automatiques via Alembic.

Observabilité : /metrics exposé à Prometheus.

Code clair, modulaire, testable et typé.

Services découplés (domaine + persistance + validation).

2. pyproject.toml (mise à jour)
[project]
name = "planner-backend"
version = "0.3.0"
description = "Planner backend (FastAPI + PostgreSQL + Redis + RQ)"
requires-python = ">=3.12"

dependencies = [
  "fastapi[all]==0.115.4",
  "uvicorn[standard]==0.30.6",
  "pydantic==2.9.2",
  "pydantic-settings==2.6.1",
  "sqlalchemy==2.0.36",
  "asyncpg==0.29.0",
  "alembic==1.13.2",
  "passlib[bcrypt]==1.7.4",
  "python-jose[cryptography]==3.3.0",
  "redis==5.0.8",
  "rq==1.16.2",
  "prometheus-fastapi-instrumentator==7.0.0"
]

[project.optional-dependencies]
dev = [
  "pytest==8.3.3",
  "pytest-asyncio==0.24.0",
  "httpx==0.27.2",
  "ruff==0.6.9",
  "mypy==1.11.2",
  "types-redis",
  "pytest-cov",
]

[tool.ruff]
line-length = 100
select = ["E","F","I","B","UP","N"]
ignore = ["E501"]

3. .env.example
DATABASE_URL=postgresql+asyncpg://app:app@db:5432/app
REDIS_URL=redis://redis:6379/0
JWT_SECRET=super_secret_key_change_me
JWT_ALG=HS256
JWT_EXPIRE_MINUTES=60
ENV=dev

4. Structure du backend
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   └── deps.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routes_health.py
│   │   │   ├── routes_auth.py
│   │   │   ├── routes_users.py
│   │   │   ├── routes_people.py
│   │   │   └── routes_projects.py
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── person.py
│   │   │   └── project.py
│   │   └── migrations/
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── person.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── person_service.py
│   ├── tasks/
│   │   └── worker.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_people.py
│       └── test_health.py
├── alembic.ini
└── pyproject.toml

5. Configuration principale
app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()

6. Logging structuré
app/core/logging.py
import logging, sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger("planner")

7. Sécurité (JWT + hash)
app/core/security.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

8. Base de données
app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app/core/deps.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

9. Exemple modèle + schéma
app/db/models/user.py
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import String, Integer, Boolean
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

app/schemas/user.py
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    email: str

class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool

10. Routes
app/api/v1/routes_health.py
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok"}

app/api/v1/routes_auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.core.security import create_access_token, verify_password
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

11. Service utilisateur
app/services/user_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.core.security import hash_password

class UserService:
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str):
        res = await db.execute(select(User).where(User.username == username))
        return res.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, username: str, email: str, password: str):
        user = User(username=username, email=email, password_hash=hash_password(password))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

12. Entrypoint principal
app/main.py
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.v1 import routes_health, routes_auth
from app.core.logging import logger

app = FastAPI(title="Planner API v3", version="0.3.0")

app.include_router(routes_health.router, prefix="/api/v1")
app.include_router(routes_auth.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    logger.info("Starting Planner API...")
    Instrumentator().instrument(app).expose(app)

13. Alembic Migrations
Commandes
cd backend
alembic init app/db/migrations
alembic revision --autogenerate -m "init db"
alembic upgrade head

alembic.ini (extrait)
[alembic]
script_location = app/db/migrations
sqlalchemy.url = postgresql+asyncpg://app:app@db:5432/app

14. Test d’intégration async
app/tests/test_auth.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

15. Observabilité

Endpoint /metrics exposé automatiquement (Prometheus FastAPI Instrumentator).

Ajoute des métriques : latence, nombre de requêtes, erreurs HTTP.

Exemple de métriques collectées :

http_requests_total{method="GET", path="/api/v1/health"}

http_request_duration_seconds_bucket{...}

Compatible avec Grafana via le service prometheus (port 9090).

16. Sécurité & Production

Activer HTTPS (nginx reverse proxy recommandé).

Changer JWT_SECRET avant le déploiement.

Utiliser gunicorn ou uvicorn --workers 4.

Configurer une politique CORS stricte.

Ajouter rate limiting via middleware ou proxy.