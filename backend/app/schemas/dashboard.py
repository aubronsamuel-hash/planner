"""Dashboard response schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class KpiSummary(BaseModel):
    active_missions: int = Field(..., ge=0)
    submitted_hours: float = Field(..., ge=0)
    pending_timesheets: int = Field(..., ge=0)


class DashboardResponse(BaseModel):
    kpis: KpiSummary


__all__ = ["KpiSummary", "DashboardResponse"]
