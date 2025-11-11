"""Timesheet models."""
from __future__ import annotations

from datetime import date
from enum import Enum
from pydantic import BaseModel, Field


class TimesheetStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    approved = "approved"


class TimesheetEntry(BaseModel):
    id: int
    user_email: str
    mission_id: int
    entry_date: date
    hours: float = Field(..., ge=0, le=24)
    status: TimesheetStatus = TimesheetStatus.draft


class TimesheetCreate(BaseModel):
    mission_id: int
    entry_date: date
    hours: float = Field(..., ge=0, le=24)


class TimesheetUpdate(BaseModel):
    hours: float | None = Field(default=None, ge=0, le=24)
    status: TimesheetStatus | None = None


__all__ = [
    "TimesheetStatus",
    "TimesheetEntry",
    "TimesheetCreate",
    "TimesheetUpdate",
]
