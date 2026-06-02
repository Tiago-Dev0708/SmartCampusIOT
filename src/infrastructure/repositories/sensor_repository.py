"""Concrete adapter for ``SensorRepositoryInterface`` using SQLAlchemy."""

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.sensor_data import SensorDataEntity, SensorType
from src.domain.interfaces.repositories import SensorRepositoryInterface
from src.infrastructure.database.models.sensor_data import SensorDataModel


class SensorRepositoryImpl(SensorRepositoryInterface):
    """Persists sensor readings to PostgreSQL via an async session.

    The session is injected through the constructor, keeping the repository
    decoupled from session lifecycle management.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Mappers ────────────────────────────────────────────────────

    @staticmethod
    def _entity_to_model(entity: SensorDataEntity) -> SensorDataModel:
        """Map a domain entity to an ORM model for persistence."""
        return SensorDataModel(
            id=entity.id,
            device_id=entity.device_id,
            sensor_type=entity.sensor_type.value,
            value=entity.value,
            timestamp=entity.timestamp,
        )

    @staticmethod
    def _model_to_entity(model: SensorDataModel) -> SensorDataEntity:
        """Map an ORM model back to a domain entity."""
        return SensorDataEntity(
            id=model.id,
            device_id=model.device_id,
            sensor_type=SensorType(model.sensor_type),
            value=model.value,
            timestamp=model.timestamp,
        )

    # ── Interface implementation ───────────────────────────────────

    async def save(self, sensor_data: SensorDataEntity) -> None:
        """Persist a single sensor reading."""
        model = self._entity_to_model(sensor_data)
        self._session.add(model)
        await self._session.commit()

    async def get_all(self) -> List[SensorDataEntity]:
        """Retrieve all stored sensor readings."""
        stmt = select(SensorDataModel).order_by(SensorDataModel.timestamp.desc())
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        return [self._model_to_entity(row) for row in rows]

    async def get_latest_value(self, device_id: str, sensor_type: str) -> float | None:
        """Retrieve the latest value of a sensor reading."""
        stmt = (
            select(SensorDataModel.value)
            .where(SensorDataModel.device_id == device_id)
            .where(SensorDataModel.sensor_type == sensor_type)
            .order_by(SensorDataModel.timestamp.desc())
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
