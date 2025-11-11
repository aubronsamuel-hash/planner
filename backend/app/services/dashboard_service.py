"""Dashboard aggregation service."""
from __future__ import annotations

from ..models.mission import MissionStatus
from ..models.timesheet import TimesheetStatus
from ..schemas.dashboard import DashboardResponse, KpiSummary
from . import mission_service, timesheet_service


def get_dashboard_summary() -> DashboardResponse:
    active_missions = sum(1 for mission in mission_service.list_missions() if mission.status == MissionStatus.active)
    submitted_hours = sum(entry.hours for entry in timesheet_service.list_timesheets())
    pending_timesheets = sum(
        1 for entry in timesheet_service.list_timesheets() if entry.status != TimesheetStatus.approved
    )
    return DashboardResponse(
        kpis=KpiSummary(
            active_missions=active_missions,
            submitted_hours=submitted_hours,
            pending_timesheets=pending_timesheets,
        )
    )


__all__ = ["get_dashboard_summary"]
