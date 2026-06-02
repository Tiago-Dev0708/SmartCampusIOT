"""Use Case: Build the consolidated dashboard metrics."""

import random
from typing import List

from src.domain.entities.dashboard import (
    DashboardDataEntity,
    SystemStatus,
    WeeklyDataPoint,
)
from src.domain.entities.room import RoomStatus
from src.domain.interfaces.repositories import RoomRepositoryInterface, SensorRepositoryInterface

# ── Engine constants ───────────────────────────────────────────────
CONSUMO_BASE: float = 25.0  # kWh — campus baseline consumption
CONSUMPTION_MAX: float = 65.0  # kWh — campus max capacity
ZONE_COUNT: int = 12

_DAYS = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]


class GetDashboardUseCase:
    """Aggregate room data into the consolidated dashboard payload."""

    def __init__(self, room_repo: RoomRepositoryInterface, sensor_repo: SensorRepositoryInterface) -> None:
        self._room_repo = room_repo
        self._sensor_repo = sensor_repo

    async def execute(self) -> DashboardDataEntity:
        rooms = await self._room_repo.get_all()
        
        # Try fetching real DHT22 temperature from Wokwi
        real_temp = await self._sensor_repo.get_latest_value("esp32_s3_campus_1", "temperature")

        # ── Consumption ────────────────────────────────────────────
        active_usage = sum(r.energy_usage for r in rooms if r.status == RoomStatus.ACTIVE)
        current_consumption = CONSUMO_BASE + active_usage

        # ── Temperature ────────────────────────────────────────────
        if rooms:
            total_temp = 0.0
            for r in rooms:
                if r.id == "1" and real_temp is not None:
                    total_temp += real_temp
                else:
                    total_temp += r.temperature
            avg_temperature = total_temp / len(rooms)
        else:
            avg_temperature = 25.5

        # ── System status ──────────────────────────────────────────
        ratio = current_consumption / CONSUMPTION_MAX
        if ratio > 0.95 or avg_temperature > 26.0:
            system_status = SystemStatus.CRITICAL
        elif ratio >= 0.75:
            system_status = SystemStatus.WARNING
        else:
            system_status = SystemStatus.OPTIMAL

        # ── Simulated chart data ───────────────────────────────────
        savings_chart = _build_weekly_chart(base=50, volatility=25)
        realtime_chart = _build_weekly_chart(base=45, volatility=20)

        # ── Savings estimate (simple heuristic) ────────────────────
        inactive_count = sum(1 for r in rooms if r.status == RoomStatus.INACTIVE)
        monthly_savings = round(inactive_count * 320.0, 2)
        savings_percent = round(
            (monthly_savings / (CONSUMPTION_MAX * 30 * 0.85)) * 100, 1
        ) if CONSUMPTION_MAX else 0.0

        return DashboardDataEntity(
            current_consumption=round(current_consumption, 1),
            consumption_unit="kWh",
            consumption_max=CONSUMPTION_MAX,
            avg_temperature=round(avg_temperature, 1),
            monthly_savings=monthly_savings,
            savings_percent=savings_percent,
            system_status=system_status,
            zone_count=ZONE_COUNT,
            savings_chart=savings_chart,
            realtime_chart=realtime_chart,
        )


def _build_weekly_chart(base: int, volatility: int) -> List[WeeklyDataPoint]:
    """Generate a realistic-looking weekly chart with today highlighted."""
    from datetime import datetime

    today_idx = datetime.now().weekday()  # 0=Mon … 6=Sun
    points: List[WeeklyDataPoint] = []
    for i, day_label in enumerate(_DAYS):
        value = base + random.randint(-volatility, volatility)
        is_current = i == today_idx
        is_future = i > today_idx
        label = "HOJE" if is_current else day_label
        points.append(
            WeeklyDataPoint(
                day=label,
                value=float(max(value, 5)),
                is_current=is_current,
                is_future=is_future,
            )
        )
    return points
