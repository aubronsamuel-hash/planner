"""Mission and assignment models."""
from __future__ import annotations

from datetime import date
from enum import Enum
from pydantic import BaseModel, Field


class MissionStatus(str, Enum):
    planned = "planned"
    active = "active"
    completed = "completed"


class MissionBase(BaseModel):
    name: str = Field(..., min_length=1)
    client: str = Field(..., min_length=1)
    start_date: date
    end_date: date
    status: MissionStatus = MissionStatus.planned


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    name: str | None = None
    client: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: MissionStatus | None = None


class MissionRead(MissionBase):
    id: int


class Assignment(BaseModel):
    mission_id: int
    user_email: str
    role: str = Field(..., min_length=1)
    capacity: int = Field(..., ge=1, le=100)


class AssignmentRead(Assignment):
    id: int


__all__ = [
    "MissionStatus",
    "MissionCreate",
    "MissionRead",
    "MissionUpdate",
    "Assignment",
    "AssignmentRead",
]
