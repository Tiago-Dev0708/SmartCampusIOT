"""Concrete adapter for ``ClassroomRepositoryInterface`` using SQLAlchemy."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.classroom import ClassroomEntity
from src.domain.interfaces.repositories import ClassroomRepositoryInterface
from src.infrastructure.database.models.classroom import ClassroomModel


class ClassroomRepositoryImpl(ClassroomRepositoryInterface):
    """Persists classroom state to PostgreSQL via an async session.

    The session is injected through the constructor.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Mappers ────────────────────────────────────────────────────

    @staticmethod
    def _entity_to_model(entity: ClassroomEntity) -> ClassroomModel:
        """Map a domain entity to an ORM model for persistence."""
        return ClassroomModel(
            id=entity.id,
            name=entity.name,
            is_occupied=entity.is_occupied,
            light_status=entity.light_status,
            last_updated=entity.last_updated,
        )

    @staticmethod
    def _model_to_entity(model: ClassroomModel) -> ClassroomEntity:
        """Map an ORM model back to a domain entity."""
        return ClassroomEntity(
            id=model.id,
            name=model.name,
            is_occupied=model.is_occupied,
            light_status=model.light_status,
            last_updated=model.last_updated,
        )

    # ── Interface implementation ───────────────────────────────────

    async def get_by_id(self, id: UUID) -> ClassroomEntity | None:
        """Retrieve a classroom by its unique id."""
        stmt = select(ClassroomModel).where(ClassroomModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._model_to_entity(model)

    async def update(self, classroom: ClassroomEntity) -> None:
        """Persist changes to an existing classroom."""
        stmt = select(ClassroomModel).where(ClassroomModel.id == classroom.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is not None:
            model.name = classroom.name
            model.is_occupied = classroom.is_occupied
            model.light_status = classroom.light_status
            model.last_updated = classroom.last_updated
            await self._session.commit()
