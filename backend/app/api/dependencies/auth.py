"""FastAPI dependencies for authentication."""
from __future__ import annotations

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ...services import user_service
from ...db.session import get_session

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_token(token: str = Depends(_oauth2_scheme)) -> str:
    """Return the bearer token provided by the caller."""

    return token


async def get_current_user(
    token: str = Depends(_oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    return await user_service.get_user_from_token(session, token)


__all__ = ["get_current_token", "get_current_user"]
