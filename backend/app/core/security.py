"""Security helpers used by the Planner services."""
from __future__ import annotations

import base64
import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from .config import get_settings


def _normalize_password(password: str) -> bytes:
    """Return a bcrypt-safe byte string for ``password``.

    Native ``bcrypt`` hashes silently truncate passwords longer than 72 bytes.
    The Planner specs require resistance against that limitation, so passwords
    are first hashed with SHA-256 and the digest is base64-encoded to keep a
    consistent and short length before being passed to ``bcrypt``. The
    base64-encoding ensures we only feed ASCII bytes to the bcrypt library while
    still covering arbitrary-length user passwords.
    """

    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with SHA-256 preprocessing."""

    normalized = _normalize_password(password)
    hashed = bcrypt.hashpw(normalized, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that ``plain_password`` matches ``hashed_password``."""

    normalized = _normalize_password(plain_password)
    return bcrypt.checkpw(normalized, hashed_password.encode("utf-8"))


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(subject: str, role: str, *, expires_minutes: int) -> str:
    """Create a signed JWT access token."""

    settings = get_settings()
    expire = _now() + timedelta(minutes=expires_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "iat": int(_now().timestamp()),
        "exp": int(expire.timestamp()),
        "jti": secrets.token_hex(8),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate an access token."""

    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def generate_refresh_token(*, expires_minutes: int) -> tuple[str, str, datetime]:
    """Return the refresh token, its SHA256 hash and expiry timestamp."""

    token = secrets.token_urlsafe(48)
    expires_at = _now() + timedelta(minutes=expires_minutes)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return token, token_hash, expires_at


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_at: datetime


__all__ = [
    "TokenPair",
    "create_access_token",
    "decode_access_token",
    "generate_refresh_token",
    "hash_password",
    "verify_password",
]
