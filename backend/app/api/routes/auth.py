"""Authentication routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.user import RefreshRequest, TokenPair, UserCreate, UserLogin, UserRead
from ...services import user_service
from ..dependencies.auth import get_current_token, get_current_user
from ...db.session import get_session

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
async def register_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    return await user_service.create_user(session, payload)


@router.post("/login", response_model=TokenPair)
async def login(
    payload: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> TokenPair:
    return await user_service.authenticate_user(session, payload)


@router.post("/refresh", response_model=TokenPair)
async def refresh(
    payload: RefreshRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenPair:
    return await user_service.refresh_tokens(session, payload)


@router.post("/logout")
async def logout(
    payload: RefreshRequest,
    session: AsyncSession = Depends(get_session),
    _: UserRead = Depends(get_current_user),
    token: str = Depends(get_current_token),
) -> dict[str, str]:
    await user_service.logout(session, payload.refresh_token, token)
    return {"status": "logged_out"}


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: UserRead = Depends(get_current_user),
) -> UserRead:
    return current_user


__all__ = ["router"]
