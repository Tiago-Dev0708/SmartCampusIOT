"""User repository concrete implementation."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import UserEntity
from src.domain.interfaces.repositories import UserRepositoryInterface
from src.infrastructure.database.models.user import UserModel

class UserRepositoryImpl(UserRepositoryInterface):
    """Adapter for database operations on the User entity."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return UserEntity(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            role=model.role,
            created_at=model.created_at,
        )

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return UserEntity(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            role=model.role,
            created_at=model.created_at,
        )

    async def save(self, user: UserEntity) -> None:
        model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            created_at=user.created_at,
        )
        self.session.add(model)
        await self.session.commit()
