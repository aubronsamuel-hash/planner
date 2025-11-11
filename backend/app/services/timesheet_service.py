"""Timesheet service relying on an in-memory store."""
from __future__ import annotations

from typing import Dict, List

from fastapi import HTTPException, status

from ..models.timesheet import TimesheetCreate, TimesheetEntry, TimesheetStatus, TimesheetUpdate

_TIMESHEETS: Dict[int, TimesheetEntry] = {}
_TIMESHEET_SEQ = 1


def _next_timesheet_id() -> int:
    global _TIMESHEET_SEQ
    current = _TIMESHEET_SEQ
    _TIMESHEET_SEQ += 1
    return current


def submit_timesheet(user_email: str, payload: TimesheetCreate) -> TimesheetEntry:
    entry = TimesheetEntry(
        id=_next_timesheet_id(),
        user_email=user_email,
        mission_id=payload.mission_id,
        entry_date=payload.entry_date,
        hours=payload.hours,
        status=TimesheetStatus.submitted,
    )
    _TIMESHEETS[entry.id] = entry
    return entry


def update_timesheet(entry_id: int, payload: TimesheetUpdate) -> TimesheetEntry:
    entry = _TIMESHEETS.get(entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timesheet not found")
    data = entry.dict()
    for key, value in payload.dict(exclude_unset=True).items():
        data[key] = value
    updated = TimesheetEntry(**data)
    _TIMESHEETS[entry_id] = updated
    return updated


def list_timesheets(user_email: str | None = None) -> List[TimesheetEntry]:
    if user_email is None:
        return list(_TIMESHEETS.values())
    return [entry for entry in _TIMESHEETS.values() if entry.user_email == user_email]


def reset_state() -> None:
    global _TIMESHEET_SEQ
    _TIMESHEETS.clear()
    _TIMESHEET_SEQ = 1


__all__ = [
    "submit_timesheet",
    "update_timesheet",
    "list_timesheets",
    "reset_state",
]
