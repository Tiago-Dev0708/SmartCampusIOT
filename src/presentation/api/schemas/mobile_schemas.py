"""Pydantic V2 schemas for the mobile API responses.

All schemas inherit from ``BaseSchema`` which applies automatic
snake_case → camelCase aliasing so the React Native frontend receives
its expected key names without manual mapping.
"""

from typing import List, Literal, Optional

from pydantic import Field

from .base import BaseSchema


# ── Room Schemas ───────────────────────────────────────────────────


class RoomResponse(BaseSchema):
    """Serialises a ``RoomEntity`` for the mobile ``Room`` TS interface."""

    id: str
    name: str
    block: str
    floor: str
    status: Literal["active", "inactive"]
    temperature: float
    energy_usage: float


class ToggleRoomRequest(BaseSchema):
    """Body of ``POST /api/rooms/{id}/toggle``."""

    status: Literal["active", "inactive"]


# ── External Sensors ───────────────────────────────────────────────


class ExternalSensorsResponse(BaseSchema):
    """Maps to the React Native ``ExternalSensors`` TS interface."""

    temperature: float
    humidity: float
    co2: float
    wind_speed: float
    status: Literal["active", "inactive"]


# ── Weekly Data Point ──────────────────────────────────────────────


class WeeklyDataPointSchema(BaseSchema):
    """Single chart data-point for line / bar charts."""

    day: str
    value: float
    is_current: Optional[bool] = False
    is_future: Optional[bool] = False


# ── Dashboard ──────────────────────────────────────────────────────


class DashboardResponse(BaseSchema):
    """Maps to the React Native ``DashboardData`` TS interface."""

    current_consumption: float
    consumption_unit: str = "kWh"
    consumption_max: float
    avg_temperature: float
    monthly_savings: float
    savings_percent: float
    system_status: Literal["optimal", "warning", "critical"]
    zone_count: int
    savings_chart: List[WeeklyDataPointSchema]
    realtime_chart: List[WeeklyDataPointSchema]


# ── Analytics ──────────────────────────────────────────────────────


class AnalyticsResponse(BaseSchema):
    """Maps to the React Native ``AnalyticsData`` TS interface."""

    total_consumption: float
    consumption_unit: str = "kWh"
    efficiency_percent: float
    co2_reduction: float
    projected_cost: float
    projected_cost_baseline: float
    predicted_goal_days: int
    chart: List[WeeklyDataPointSchema]
    forecast_chart: List[WeeklyDataPointSchema]


# ── Auth ───────────────────────────────────────────────────────────


class LoginRequest(BaseSchema):
    """Body of ``POST /api/auth/login``."""

    email: str = Field(..., description="User e-mail address")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")


class UserResponse(BaseSchema):
    """Public user profile returned after login."""

    id: str
    name: str
    email: str
    role: Literal["admin", "user"]


class AuthResponse(BaseSchema):
    """Response of ``POST /api/auth/login``."""

    user: UserResponse
    access_token: str
    refresh_token: str


class RegisterRequest(BaseSchema):
    """Body of ``POST /api/auth/register``."""

    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User e-mail address")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")


class RefreshRequest(BaseSchema):
    """Body of ``POST /api/auth/refresh``."""

    refresh_token: str


class TokenResponse(BaseSchema):
    """Response for refresh token endpoint."""

    access_token: str
