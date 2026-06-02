"""Use Case: Generate analytics and AI-driven projection data."""

import random
from typing import List

from src.domain.entities.dashboard import (
    AnalyticsDataEntity,
    WeeklyDataPoint,
)
from src.domain.entities.room import RoomStatus
from src.domain.interfaces.repositories import RoomRepositoryInterface
from src.application.use_cases.get_dashboard import CONSUMO_BASE, CONSUMPTION_MAX, _DAYS


class GetAnalyticsUseCase:
    """Compute analytics metrics based on room state and projections."""

    def __init__(self, room_repo: RoomRepositoryInterface) -> None:
        self._room_repo = room_repo

    async def execute(self) -> AnalyticsDataEntity:
        rooms = await self._room_repo.get_all()

        active_usage = sum(r.energy_usage for r in rooms if r.status == RoomStatus.ACTIVE)
        total_consumption = round(CONSUMO_BASE * 30 + active_usage * 30, 1)

        inactive_count = sum(1 for r in rooms if r.status == RoomStatus.INACTIVE)
        efficiency_percent = round(
            (inactive_count / len(rooms) * 100) if rooms else 0, 1
        )

        co2_reduction = round(inactive_count * 0.28, 1)

        projected_cost_baseline = round(CONSUMPTION_MAX * 30 * 0.85 * 0.65, 2)
        projected_cost = round(total_consumption * 0.65, 2)

        predicted_goal_days = max(5, 30 - inactive_count * 3)

        chart = _build_analytics_chart(base=50, volatility=15)
        forecast_chart = _build_analytics_chart(base=52, volatility=10)

        return AnalyticsDataEntity(
            total_consumption=total_consumption,
            consumption_unit="kWh",
            efficiency_percent=efficiency_percent,
            co2_reduction=co2_reduction,
            projected_cost=projected_cost,
            projected_cost_baseline=projected_cost_baseline,
            predicted_goal_days=predicted_goal_days,
            chart=chart,
            forecast_chart=forecast_chart,
        )


def _build_analytics_chart(base: int, volatility: int) -> List[WeeklyDataPoint]:
    from datetime import datetime

    today_idx = datetime.now().weekday()
    points: List[WeeklyDataPoint] = []
    for i, day_label in enumerate(_DAYS):
        value = base + random.randint(-volatility, volatility)
        is_current = i == today_idx
        is_future = i > today_idx
        points.append(
            WeeklyDataPoint(
                day=day_label,
                value=float(max(value, 5)),
                is_current=is_current,
                is_future=is_future,
            )
        )
    return points
