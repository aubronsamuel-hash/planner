"""Timesheet routes."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status

from ...models.timesheet import TimesheetCreate, TimesheetEntry, TimesheetUpdate
from ...models.user import UserRead
from ...services import timesheet_service
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/timesheets", tags=["timesheets"])


@router.post("/", response_model=TimesheetEntry, status_code=status.HTTP_201_CREATED)
def submit_timesheet(payload: TimesheetCreate, current_user: UserRead = Depends(get_current_user)) -> TimesheetEntry:
    return timesheet_service.submit_timesheet(current_user.email, payload)


@router.patch("/{entry_id}", response_model=TimesheetEntry)
def patch_timesheet(entry_id: int, payload: TimesheetUpdate, _: UserRead = Depends(get_current_user)) -> TimesheetEntry:
    return timesheet_service.update_timesheet(entry_id, payload)


@router.get("/", response_model=List[TimesheetEntry])
def list_my_timesheets(current_user: UserRead = Depends(get_current_user)) -> List[TimesheetEntry]:
    return timesheet_service.list_timesheets(current_user.email)


__all__ = ["router"]
