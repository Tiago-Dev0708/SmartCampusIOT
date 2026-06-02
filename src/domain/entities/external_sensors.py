"""Domain entity for the campus weather / environmental sensor station."""

from dataclasses import dataclass

from .room import RoomStatus


@dataclass
class ExternalSensorsEntity:
    """Pure domain entity representing external (meteorological) sensor readings.

    Maps to the React Native ``ExternalSensors`` TypeScript interface.

    Attributes:
        temperature: Outside temperature in °C.
        humidity: Relative humidity percentage.
        co2: CO₂ concentration in ppm.
        wind_speed: Wind speed in km/h.
        status: Station operational status — ``'active'`` or ``'inactive'``.
    """

    temperature: float
    humidity: float
    co2: float
    wind_speed: float
    status: RoomStatus
