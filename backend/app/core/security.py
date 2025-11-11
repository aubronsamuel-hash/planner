"""Security helpers used by the generated FastAPI routes."""
from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

from .config import get_settings

_PASSWORD_SALT = "planner-demo-salt"
_TOKEN_STORE: Dict[str, Tuple[str, datetime]] = {}


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    """Return a deterministic hash for the provided password."""

    return _hash(f"{_PASSWORD_SALT}:{password}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Constant-time verification used during login."""

    candidate = hash_password(plain_password)
    return hmac.compare_digest(candidate, hashed_password)


def create_token(subject: str, *, expiry_minutes: int) -> Tuple[str, datetime]:
    """Generate a pseudo JWT token and its expiration date."""

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    _TOKEN_STORE[token] = (subject, expires_at)
    return token, expires_at


def revoke_token(token: str) -> None:
    _TOKEN_STORE.pop(token, None)


def resolve_token(token: str) -> str | None:
    """Return the subject associated with a token if it is still valid."""

    if token not in _TOKEN_STORE:
        return None
    subject, expires_at = _TOKEN_STORE[token]
    if datetime.now(timezone.utc) >= expires_at:
        _TOKEN_STORE.pop(token, None)
        return None
    return subject


def issue_access_refresh_pair(subject: str) -> tuple[str, str]:
    settings = get_settings()
    access_token, _ = create_token(subject, expiry_minutes=settings.access_token_expiry_minutes)
    refresh_token, _ = create_token(subject, expiry_minutes=settings.refresh_token_expiry_minutes)
    return access_token, refresh_token


__all__ = [
    "hash_password",
    "verify_password",
    "issue_access_refresh_pair",
    "resolve_token",
    "revoke_token",
]
