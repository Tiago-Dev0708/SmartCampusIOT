"""Dashboard router — consolidated campus metrics endpoint."""

from fastapi import APIRouter

from src.presentation.api.dependencies import DashboardUseCaseDep
from src.presentation.api.schemas.mobile_schemas import (
    DashboardResponse,
    WeeklyDataPointSchema,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Executive dashboard",
    description=(
        "Returns consolidated campus metrics computed in real-time "
        "by the IoT simulation engine based on current room states."
    ),
)
async def get_dashboard(use_case: DashboardUseCaseDep) -> DashboardResponse:
    """Aggregate and return dashboard metrics."""
    data = await use_case.execute()
    return DashboardResponse(
        current_consumption=data.current_consumption,
        consumption_unit=data.consumption_unit,
        consumption_max=data.consumption_max,
        avg_temperature=data.avg_temperature,
        monthly_savings=data.monthly_savings,
        savings_percent=data.savings_percent,
        system_status=data.system_status.value,
        zone_count=data.zone_count,
        savings_chart=[
            WeeklyDataPointSchema(
                day=pt.day,
                value=pt.value,
                is_current=pt.is_current,
                is_future=pt.is_future,
            )
            for pt in data.savings_chart
        ],
        realtime_chart=[
            WeeklyDataPointSchema(
                day=pt.day,
                value=pt.value,
                is_current=pt.is_current,
                is_future=pt.is_future,
            )
            for pt in data.realtime_chart
        ],
    )
