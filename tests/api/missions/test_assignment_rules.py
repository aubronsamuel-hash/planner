from datetime import date, timedelta

import pytest

from backend.app.models.mission import Assignment, MissionCreate, MissionStatus
from backend.app.services import mission_service


def setup_function() -> None:
    mission_service.reset_state()


def test_assignment_requires_valid_mission() -> None:
    payload = Assignment(mission_id=999, user_email="member@example.com", role="dev", capacity=50)
    with pytest.raises(Exception):
        mission_service.assign_user(payload)


def test_assignment_successful_for_existing_mission() -> None:
    mission = mission_service.create_mission(
        MissionCreate(
            name="Mission B",
            client="Client Y",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            status=MissionStatus.active,
        )
    )
    assignment = mission_service.assign_user(
        Assignment(mission_id=mission.id, user_email="member@example.com", role="designer", capacity=40)
    )
    assert assignment.mission_id == mission.id
