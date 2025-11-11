"""Mission service with in-memory storage."""
from __future__ import annotations

from datetime import date
from typing import Dict, List

from fastapi import HTTPException, status

from ..models.mission import Assignment, AssignmentRead, MissionCreate, MissionRead, MissionUpdate

_MISSIONS: Dict[int, MissionRead] = {}
_ASSIGNMENTS: Dict[int, AssignmentRead] = {}
_MISSION_SEQ = 1
_ASSIGNMENT_SEQ = 1


def _next_mission_id() -> int:
    global _MISSION_SEQ
    current = _MISSION_SEQ
    _MISSION_SEQ += 1
    return current


def _next_assignment_id() -> int:
    global _ASSIGNMENT_SEQ
    current = _ASSIGNMENT_SEQ
    _ASSIGNMENT_SEQ += 1
    return current


def _validate_dates(start: date, end: date) -> None:
    if end < start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End date must be after start date")


def create_mission(payload: MissionCreate) -> MissionRead:
    _validate_dates(payload.start_date, payload.end_date)
    mission = MissionRead(id=_next_mission_id(), **payload.model_dump())
    _MISSIONS[mission.id] = mission
    return mission


def list_missions() -> List[MissionRead]:
    return list(_MISSIONS.values())


def update_mission(mission_id: int, payload: MissionUpdate) -> MissionRead:
    mission = _MISSIONS.get(mission_id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    data = mission.model_dump()
    for key, value in payload.model_dump(exclude_unset=True).items():
        data[key] = value
    _validate_dates(data["start_date"], data["end_date"])
    updated = MissionRead(**data)
    _MISSIONS[mission_id] = updated
    return updated


def delete_mission(mission_id: int) -> None:
    if mission_id in _MISSIONS:
        _MISSIONS.pop(mission_id)
        for assignment_id, assignment in list(_ASSIGNMENTS.items()):
            if assignment.mission_id == mission_id:
                _ASSIGNMENTS.pop(assignment_id)


def assign_user(payload: Assignment) -> AssignmentRead:
    if payload.mission_id not in _MISSIONS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    assignment = AssignmentRead(id=_next_assignment_id(), **payload.model_dump())
    _ASSIGNMENTS[assignment.id] = assignment
    return assignment


def list_assignments(mission_id: int | None = None) -> List[AssignmentRead]:
    if mission_id is None:
        return list(_ASSIGNMENTS.values())
    return [assignment for assignment in _ASSIGNMENTS.values() if assignment.mission_id == mission_id]


def reset_state() -> None:
    global _MISSION_SEQ, _ASSIGNMENT_SEQ
    _MISSIONS.clear()
    _ASSIGNMENTS.clear()
    _MISSION_SEQ = 1
    _ASSIGNMENT_SEQ = 1


__all__ = [
    "create_mission",
    "list_missions",
    "update_mission",
    "delete_mission",
    "assign_user",
    "list_assignments",
    "reset_state",
]
