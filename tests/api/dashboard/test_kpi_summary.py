from datetime import date

from backend.app.models.mission import MissionCreate, MissionStatus
from backend.app.models.timesheet import TimesheetCreate
from backend.app.services import dashboard_service, mission_service, timesheet_service


def setup_function() -> None:
    mission_service.reset_state()
    timesheet_service.reset_state()


def test_dashboard_summary() -> None:
    mission_service.create_mission(
        MissionCreate(
            name="Active Mission",
            client="Client Z",
            start_date=date.today(),
            end_date=date.today(),
            status=MissionStatus.active,
        )
    )

    timesheet_service.submit_timesheet("exec@example.com", TimesheetCreate(mission_id=1, entry_date=date.today(), hours=8))

    summary = dashboard_service.get_dashboard_summary()
    assert summary.kpis.active_missions >= 1
    assert summary.kpis.submitted_hours >= 8
