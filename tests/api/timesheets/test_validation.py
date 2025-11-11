import pytest

from backend.app.models.timesheet import TimesheetCreate, TimesheetUpdate
from backend.app.services import timesheet_service


def setup_function() -> None:
    timesheet_service.reset_state()


def test_update_missing_entry_returns_404() -> None:
    with pytest.raises(Exception):
        timesheet_service.update_timesheet(999, TimesheetUpdate(hours=5))


def test_submit_with_invalid_hours() -> None:
    with pytest.raises(Exception):
        TimesheetCreate(mission_id=1, entry_date="2024-01-01", hours=30)
