from datetime import date

from backend.app.models.mission import MissionCreate, MissionStatus, MissionUpdate
from backend.app.services import mission_service


def setup_function() -> None:
    mission_service.reset_state()


def test_create_list_mission() -> None:
    payload = MissionCreate(
        name="Mission A",
        client="Client X",
        start_date=date.today(),
        end_date=date.today(),
        status=MissionStatus.planned,
    )
    created = mission_service.create_mission(payload)
    assert created.name == "Mission A"

    missions = mission_service.list_missions()
    assert len(missions) == 1


def test_update_mission_dates() -> None:
    payload = MissionCreate(
        name="Mission B",
        client="Client X",
        start_date=date.today(),
        end_date=date.today(),
        status=MissionStatus.active,
    )
    created = mission_service.create_mission(payload)
    updated = mission_service.update_mission(created.id, MissionUpdate(status=MissionStatus.completed))
    assert updated.status == MissionStatus.completed
