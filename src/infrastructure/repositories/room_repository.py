"""Concrete adapter for ``RoomRepositoryInterface`` using SQLAlchemy."""

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.room import RoomEntity, RoomStatus
from src.domain.interfaces.repositories import RoomRepositoryInterface
from src.infrastructure.database.models.room import RoomModel


class RoomRepositoryImpl(RoomRepositoryInterface):
    """Persists mobile-facing room state to PostgreSQL.

    The async session is injected through the constructor.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Mappers ────────────────────────────────────────────────────

    @staticmethod
    def _model_to_entity(model: RoomModel) -> RoomEntity:
        """Map an ORM model to a domain entity."""
        return RoomEntity(
            id=model.id,
            name=model.name,
            block=model.block,
            floor=model.floor,
            status=RoomStatus(model.status),
            temperature=model.temperature,
            energy_usage=model.energy_usage,
        )

    @staticmethod
    def _entity_to_model(entity: RoomEntity) -> RoomModel:
        """Map a domain entity to an ORM model."""
        return RoomModel(
            id=entity.id,
            name=entity.name,
            block=entity.block,
            floor=entity.floor,
            status=entity.status.value,
            temperature=entity.temperature,
            energy_usage=entity.energy_usage,
        )

    # ── Interface implementation ───────────────────────────────────

    async def get_all(self) -> List[RoomEntity]:
        """Return every room registered in the system."""
        stmt = select(RoomModel).order_by(RoomModel.id)
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        return [self._model_to_entity(row) for row in rows]

    async def get_by_id(self, room_id: str) -> RoomEntity | None:
        """Look up a single room by its string id."""
        stmt = select(RoomModel).where(RoomModel.id == room_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._model_to_entity(model)

    async def update(self, room: RoomEntity) -> None:
        """Persist the updated state of a room."""
        stmt = select(RoomModel).where(RoomModel.id == room.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is not None:
            model.name = room.name
            model.block = room.block
            model.floor = room.floor
            model.status = room.status.value
            model.temperature = room.temperature
            model.energy_usage = room.energy_usage
            await self._session.commit()
