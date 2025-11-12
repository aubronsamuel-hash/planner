"""User service backed by SQLAlchemy and Redis."""
from __future__ import annotations

import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import get_settings
from ..core.redis import delete_key, ensure_redis, set_with_ttl
from ..core.security import (
    create_access_token,
    decode_access_token,
    generate_refresh_token,
    hash_password,
    revoke_jti,
    verify_password,
)
from ..db.models import RefreshToken, Role, User
from ..db.session import get_session_maker
from ..models.user import RefreshRequest, TokenPair, UserCreate, UserLogin, UserRead

_REQUIRED_ROLES = ("admin", "manager", "collaborator", "observer")


def _hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


async def _ensure_roles(session: AsyncSession) -> None:
    existing = await session.execute(select(Role.name))
    present = {name for (name,) in existing.all()}
    for role_name in _REQUIRED_ROLES:
        if role_name not in present:
            session.add(Role(name=role_name))
    await session.flush()


def _to_user_read(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name,
        is_active=user.is_active,
        created_at=user.created_at,
    )


async def create_user(session: AsyncSession, payload: UserCreate) -> UserRead:
    await _ensure_roles(session)
    existing = await session.execute(
        select(User).options(selectinload(User.role)).where(User.email == payload.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    role = await session.execute(select(Role).where(Role.name == payload.role))
    role_obj = role.scalar_one_or_none()
    if role_obj is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown role")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=role_obj,
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:  # pragma: no cover - double safeguard
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists") from exc
    await session.refresh(user, attribute_names=["role"])
    return _to_user_read(user)


async def _persist_refresh_token(
    session: AsyncSession,
    user: User,
    token_hash: str,
    expires_at: datetime,
    access_jti: str,
) -> None:
    record = RefreshToken(
        user=user, token_hash=token_hash, expires_at=expires_at, access_jti=access_jti
    )
    session.add(record)
    await session.flush()
    ttl = max(int((expires_at - datetime.now(timezone.utc)).total_seconds()), 1)
    await set_with_ttl(
        f"refresh:{token_hash}", f"{user.id}:{access_jti}".encode("utf-8"), ttl
    )


async def authenticate_user(session: AsyncSession, payload: UserLogin) -> TokenPair:
    settings = get_settings()
    result = await session.execute(
        select(User).options(selectinload(User.role)).where(User.email == payload.email)
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User disabled")

    access_token, access_jti = await create_access_token(
        str(user.id), user.role.name, expires_minutes=settings.access_token_expiry_minutes
    )
    refresh_token, refresh_hash, expires_at = generate_refresh_token(
        expires_minutes=settings.refresh_token_expiry_minutes
    )
    await _persist_refresh_token(session, user, refresh_hash, expires_at, access_jti)
    await session.commit()
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


async def refresh_tokens(session: AsyncSession, payload: RefreshRequest) -> TokenPair:
    refresh_hash = _hash_refresh_token(payload.refresh_token)
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.token_hash == refresh_hash, RefreshToken.revoked.is_(False))
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    expires_at = record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    redis_client = await ensure_redis()
    redis_owner = await redis_client.get(f"refresh:{refresh_hash}")
    if redis_owner is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")
    owner_str = redis_owner.decode("utf-8") if isinstance(redis_owner, bytes) else str(redis_owner)
    owner_id_str, _, owner_jti = owner_str.partition(":")
    if not owner_id_str or int(owner_id_str) != record.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")
    if record.access_jti and owner_jti and owner_jti != record.access_jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

    user = await session.get(User, record.user_id, options=(selectinload(User.role),))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown token owner")

    record.revoked = True
    if record.access_jti:
        await revoke_jti(record.access_jti)
    await delete_key(f"refresh:{refresh_hash}")

    settings = get_settings()
    access_token, access_jti = await create_access_token(
        str(user.id), user.role.name, expires_minutes=settings.access_token_expiry_minutes
    )
    new_refresh, new_hash, expires_at = generate_refresh_token(
        expires_minutes=settings.refresh_token_expiry_minutes
    )
    await _persist_refresh_token(session, user, new_hash, expires_at, access_jti)
    await session.commit()
    return TokenPair(access_token=access_token, refresh_token=new_refresh)


async def logout(session: AsyncSession, refresh_token: str, access_token: str | None = None) -> None:
    refresh_hash = _hash_refresh_token(refresh_token)
    result = await session.execute(select(RefreshToken).where(RefreshToken.token_hash == refresh_hash))
    record = result.scalar_one_or_none()
    if not record:
        return
    record.revoked = True
    if record.access_jti:
        await revoke_jti(record.access_jti)
    if access_token:
        try:
            payload = await decode_access_token(access_token)
            jti = payload.get("jti")
            if jti:
                await revoke_jti(jti)
        except Exception:  # pragma: no cover - invalid token during logout
            pass
    await session.commit()
    await delete_key(f"refresh:{refresh_hash}")


async def get_user_from_token(session: AsyncSession, token: str) -> Optional[UserRead]:
    try:
        payload = await decode_access_token(token)
    except Exception as exc:  # pragma: no cover - jwt raises multiple error types
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user_id = int(payload.get("sub", 0))
    user = await session.get(User, user_id, options=(selectinload(User.role),))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return _to_user_read(user)


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[UserRead]:
    result = await session.execute(
        select(User).options(selectinload(User.role)).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if not user:
        return None
    return _to_user_read(user)


async def _reset_state_async() -> None:
    session_maker = get_session_maker()
    async with session_maker() as session:
        await session.execute(delete(RefreshToken))
        await session.execute(delete(User))
        await session.commit()
    redis_client = await ensure_redis()
    await redis_client.flushdb()


async def reset_state_async() -> None:
    await _reset_state_async()


def reset_state() -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(_reset_state_async())
        return
    raise RuntimeError(
        "reset_state cannot run inside an active event loop; use reset_state_async instead"
    )


__all__ = [
    "authenticate_user",
    "create_user",
    "get_user_by_email",
    "get_user_from_token",
    "logout",
    "refresh_tokens",
    "reset_state",
    "reset_state_async",
]
