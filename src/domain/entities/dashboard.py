"""Domain entities for the executive dashboard and analytics views."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class SystemStatus(str, Enum):
    """Strict literal values for the campus-wide system health indicator."""

    OPTIMAL = "optimal"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class WeeklyDataPoint:
    """A single data-point used by the mobile chart components.

    Attributes:
        day: Abbreviated weekday label (e.g. "SEG", "TER", "HOJE").
        value: Numeric y-axis value.
        is_current: Highlight flag for the current day.
        is_future: Renders a dashed / projected style on the chart.
    """

    day: str
    value: float
    is_current: bool = False
    is_future: bool = False


@dataclass
class DashboardDataEntity:
    """Consolidated campus metrics consumed by the Dashboard screen.

    Maps to the React Native ``DashboardData`` TypeScript interface.
    """

    current_consumption: float
    consumption_unit: str  # Fixed to "kWh"
    consumption_max: float
    avg_temperature: float
    monthly_savings: float
    savings_percent: float
    system_status: SystemStatus
    zone_count: int
    savings_chart: List[WeeklyDataPoint] = field(default_factory=list)
    realtime_chart: List[WeeklyDataPoint] = field(default_factory=list)


@dataclass
class AnalyticsDataEntity:
    """Analytics and AI-driven projection data consumed by the Analytics screen.

    Maps to the React Native ``AnalyticsData`` TypeScript interface.
    """

    total_consumption: float
    consumption_unit: str  # Fixed to "kWh"
    efficiency_percent: float
    co2_reduction: float
    projected_cost: float
    projected_cost_baseline: float
    predicted_goal_days: int
    chart: List[WeeklyDataPoint] = field(default_factory=list)
    forecast_chart: List[WeeklyDataPoint] = field(default_factory=list)
