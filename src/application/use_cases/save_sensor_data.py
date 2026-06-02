"""Use Case: Persist a validated sensor reading to the repository.

This is the single entry-point the MQTT listener and the simulation
endpoint use to store IoT data.  It receives a presentation-layer DTO,
converts it into a pure domain entity and delegates persistence to the
injected repository — keeping the domain free of Pydantic dependencies.
"""

from datetime import datetime, timezone

from src.domain.entities.sensor_data import SensorDataEntity, SensorType
from src.domain.interfaces.repositories import SensorRepositoryInterface
from src.presentation.api.schemas.mqtt_schemas import SensorPayloadDTO


class SaveSensorDataUseCase:
    """Orchestrate the storage of a single IoT sensor reading."""

    def __init__(self, sensor_repo: SensorRepositoryInterface) -> None:
        self._sensor_repo = sensor_repo

    async def execute(self, dto: SensorPayloadDTO) -> None:
        """Validate, map and persist the sensor payload.

        Args:
            dto: A validated ``SensorPayloadDTO`` coming from the MQTT
                 listener or the REST simulation endpoint.
        """
        entity = SensorDataEntity(
            device_id=dto.device_id,
            sensor_type=SensorType(dto.sensor_type),
            value=dto.value,
            timestamp=dto.timestamp or datetime.now(tz=timezone.utc),
        )
        await self._sensor_repo.save(entity)
