"""Pydantic V2 schemas for MQTT payload validation.

Every JSON message received from the ESP32-S3 microcontroller is
deserialised into a ``SensorPayloadDTO`` before being forwarded to
the application layer.  Invalid payloads are rejected with a
``ValidationError`` that the MQTT listener catches and logs.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SensorPayloadDTO(BaseModel):
    """Data-transfer object representing a raw IoT sensor reading.

    Attributes:
        device_id: Hardware identifier of the ESP32-S3 board.
        sensor_type: One of the four supported sensor categories.
        value: The numeric measurement captured by the sensor.
        timestamp: ISO-8601 timestamp of the reading (optional — defaults to now).
    """

    device_id: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Hardware identifier of the ESP32-S3 board.",
    )
    sensor_type: Literal["presence", "light", "soil_moisture", "temperature"] = Field(
        ...,
        description="Category of sensor that produced this reading.",
    )
    value: float = Field(
        ...,
        description="Numeric measurement captured by the sensor.",
    )
    timestamp: datetime | None = Field(
        default=None,
        description="ISO-8601 reading timestamp.  Defaults to server time when absent.",
    )
