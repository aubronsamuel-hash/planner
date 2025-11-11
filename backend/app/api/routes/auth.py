"""Authentication routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ...models.user import RefreshRequest, TokenPair, UserCreate, UserLogin, UserRead
from ...services import user_service
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register_user(payload: UserCreate) -> UserRead:
    return user_service.create_user(payload)


@router.post("/login", response_model=TokenPair)
def login(payload: UserLogin) -> TokenPair:
    return user_service.authenticate_user(payload)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest) -> TokenPair:
    return user_service.refresh_tokens(payload)


@router.post("/logout")
def logout(payload: RefreshRequest) -> dict[str, str]:
    user_service.logout(payload.refresh_token)
    return {"status": "logged_out"}


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    return current_user


__all__ = ["router"]
