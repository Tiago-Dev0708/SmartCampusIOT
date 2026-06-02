"""Async database engine and session configuration.

Reads the PostgreSQL connection URL from environment variables via
``pydantic_settings`` and exposes lazy-initialised helpers so that
importing the module never triggers a network call.
"""

from collections.abc import AsyncGenerator
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseSettings(BaseSettings):
    """Settings loaded from environment / ``.env`` file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/smartcampus"


# ── Lazy singletons ───────────────────────────────────────────────

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def _get_settings() -> DatabaseSettings:
    return DatabaseSettings()


def get_engine() -> AsyncEngine:
    """Return (and lazily create) the shared ``AsyncEngine``."""
    global _engine
    if _engine is None:
        settings = _get_settings()
        _engine = create_async_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return (and lazily create) the ``async_sessionmaker``."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an ``AsyncSession`` and closes it afterward."""
    factory = get_session_factory()
    async with factory() as session:
        yield session
