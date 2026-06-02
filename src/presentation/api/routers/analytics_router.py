"""Analytics router — AI-driven insights and projections."""

from fastapi import APIRouter

from src.presentation.api.dependencies import AnalyticsUseCaseDep
from src.presentation.api.schemas.mobile_schemas import (
    AnalyticsResponse,
    WeeklyDataPointSchema,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "",
    response_model=AnalyticsResponse,
    summary="Analytics and AI insights",
    description=(
        "Returns consumption analytics, CO₂ reduction metrics, cost "
        "projections and forecast charts based on current room states."
    ),
)
async def get_analytics(use_case: AnalyticsUseCaseDep) -> AnalyticsResponse:
    """Compute and return analytics data."""
    data = await use_case.execute()
    return AnalyticsResponse(
        total_consumption=data.total_consumption,
        consumption_unit=data.consumption_unit,
        efficiency_percent=data.efficiency_percent,
        co2_reduction=data.co2_reduction,
        projected_cost=data.projected_cost,
        projected_cost_baseline=data.projected_cost_baseline,
        predicted_goal_days=data.predicted_goal_days,
        chart=[
            WeeklyDataPointSchema(
                day=pt.day,
                value=pt.value,
                is_current=pt.is_current,
                is_future=pt.is_future,
            )
            for pt in data.chart
        ],
        forecast_chart=[
            WeeklyDataPointSchema(
                day=pt.day,
                value=pt.value,
                is_current=pt.is_current,
                is_future=pt.is_future,
            )
            for pt in data.forecast_chart
        ],
    )
