from backend.app.services import dashboard_service, mission_service, timesheet_service


def test_dashboard_summary_requires_data_reset() -> None:
    mission_service.reset_state()
    timesheet_service.reset_state()
    summary = dashboard_service.get_dashboard_summary()
    assert summary.kpis.pending_timesheets == 0
