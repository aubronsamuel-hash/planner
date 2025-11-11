from datetime import date

from backend.app.models.timesheet import TimesheetCreate
from backend.app.services import timesheet_service


def setup_function() -> None:
    timesheet_service.reset_state()


def test_submit_and_list_timesheets() -> None:
    payload = TimesheetCreate(mission_id=1, entry_date=date.today(), hours=6)
    created = timesheet_service.submit_timesheet("user@example.com", payload)
    assert created.hours == 6

    entries = timesheet_service.list_timesheets("user@example.com")
    assert len(entries) == 1
