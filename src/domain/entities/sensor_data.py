"""Domain entity representing a single sensor data reading."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class SensorType(str, Enum):
    """Enumeration of supported sensor types."""

    PRESENCE = "presence"
    LIGHT = "light"
    SOIL_MOISTURE = "soil_moisture"
    TEMPERATURE = "temperature"


@dataclass
class SensorDataEntity:
    """Pure domain entity for an IoT sensor reading.

    Attributes:
        id: Unique identifier for this reading.
        device_id: Identifier of the physical device that produced this reading.
        sensor_type: Category of sensor (presence, light, soil_moisture, temperature).
        value: Numeric measurement captured by the sensor.
        timestamp: Moment at which the reading was taken.
    """

    device_id: str
    sensor_type: SensorType
    value: float
    timestamp: datetime
    id: UUID = field(default_factory=uuid4)
