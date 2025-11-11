"""Mission routes."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status

from ...models.mission import Assignment, AssignmentRead, MissionCreate, MissionRead, MissionUpdate
from ...models.user import UserRead
from ...services import mission_service
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/missions", tags=["missions"])


@router.get("/", response_model=List[MissionRead])
def list_missions(_: UserRead = Depends(get_current_user)) -> List[MissionRead]:
    return mission_service.list_missions()


@router.post("/", response_model=MissionRead, status_code=status.HTTP_201_CREATED)
def create_mission(payload: MissionCreate, _: UserRead = Depends(get_current_user)) -> MissionRead:
    return mission_service.create_mission(payload)


@router.put("/{mission_id}", response_model=MissionRead)
def update_mission(mission_id: int, payload: MissionUpdate, _: UserRead = Depends(get_current_user)) -> MissionRead:
    return mission_service.update_mission(mission_id, payload)


@router.delete("/{mission_id}")
def delete_mission(mission_id: int, _: UserRead = Depends(get_current_user)) -> dict[str, str]:
    mission_service.delete_mission(mission_id)
    return {"status": "deleted"}


@router.post("/assign", response_model=AssignmentRead, status_code=status.HTTP_201_CREATED)
def create_assignment(payload: Assignment, _: UserRead = Depends(get_current_user)) -> AssignmentRead:
    return mission_service.assign_user(payload)


@router.get("/{mission_id}/assignments", response_model=List[AssignmentRead])
def list_mission_assignments(mission_id: int, _: UserRead = Depends(get_current_user)) -> List[AssignmentRead]:
    return mission_service.list_assignments(mission_id)


__all__ = ["router"]
