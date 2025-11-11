"""Dashboard routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ...models.user import UserRead
from ...schemas.dashboard import DashboardResponse
from ...services import dashboard_service
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardResponse)
def get_summary(_: UserRead = Depends(get_current_user)) -> DashboardResponse:
    return dashboard_service.get_dashboard_summary()


__all__ = ["router"]
