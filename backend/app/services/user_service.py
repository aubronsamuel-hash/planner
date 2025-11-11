"""In-memory user service used for the build phase."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import HTTPException, status

from ..core.security import hash_password, issue_access_refresh_pair, resolve_token, revoke_token, verify_password
from ..models.user import RefreshRequest, TokenPair, UserCreate, UserInDB, UserLogin, UserRead

_USERS: Dict[str, UserInDB] = {}
_USER_ID_SEQ = 1
_REFRESH_TO_USER: Dict[str, str] = {}


def _next_id() -> int:
    global _USER_ID_SEQ
    current = _USER_ID_SEQ
    _USER_ID_SEQ += 1
    return current


def create_user(payload: UserCreate) -> UserRead:
    if payload.email in _USERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user = UserInDB(
        id=_next_id(),
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        created_at=datetime.now(timezone.utc),
    )
    _USERS[payload.email] = user
    return UserRead(id=user.id, email=user.email, full_name=user.full_name, is_active=user.is_active)


def authenticate_user(payload: UserLogin) -> TokenPair:
    user = _USERS.get(payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access, refresh = issue_access_refresh_pair(payload.email)
    _REFRESH_TO_USER[refresh] = payload.email
    return TokenPair(access_token=access, refresh_token=refresh)


def refresh_tokens(payload: RefreshRequest) -> TokenPair:
    email = _REFRESH_TO_USER.get(payload.refresh_token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access, refresh = issue_access_refresh_pair(email)
    _REFRESH_TO_USER.pop(payload.refresh_token, None)
    _REFRESH_TO_USER[refresh] = email
    return TokenPair(access_token=access, refresh_token=refresh)


def logout(refresh_token: str) -> None:
    email = _REFRESH_TO_USER.pop(refresh_token, None)
    if not email:
        return
    revoke_token(refresh_token)


def get_user_by_email(email: str) -> Optional[UserRead]:
    user = _USERS.get(email)
    if not user:
        return None
    return UserRead(id=user.id, email=user.email, full_name=user.full_name, is_active=user.is_active)


def get_user_from_token(token: str) -> Optional[UserRead]:
    email = resolve_token(token)
    if not email:
        return None
    return get_user_by_email(email)


def reset_state() -> None:
    """Utility used by tests to reset the in-memory store."""

    global _USER_ID_SEQ
    _USERS.clear()
    _REFRESH_TO_USER.clear()
    _USER_ID_SEQ = 1


__all__ = [
    "create_user",
    "authenticate_user",
    "refresh_tokens",
    "logout",
    "get_user_from_token",
    "get_user_by_email",
    "reset_state",
]
