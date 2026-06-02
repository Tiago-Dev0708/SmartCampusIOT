"""Abstract repository interfaces (Ports) for the Smart Campus domain.

All concrete implementations (Adapters) live in ``src/infrastructure/``
and are injected at runtime via the dependency-injection layer.
"""

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from ..entities.sensor_data import SensorDataEntity
from ..entities.classroom import ClassroomEntity
from ..entities.room import RoomEntity
from ..entities.external_sensors import ExternalSensorsEntity
from ..entities.dashboard import AnalyticsDataEntity
from ..entities.user import UserEntity


# ── Sensor Repository ──────────────────────────────────────────────


class SensorRepositoryInterface(ABC):
    """Port for persisting raw IoT sensor readings."""

    @abstractmethod
    async def save(self, sensor_data: SensorDataEntity) -> None:
        """Persist a single sensor reading."""
        ...

    @abstractmethod
    async def get_all(self) -> List[SensorDataEntity]:
        """Retrieve all stored sensor readings."""
        ...

    @abstractmethod
    async def get_latest_value(self, device_id: str, sensor_type: str) -> float | None:
        """Retrieve the latest value of a sensor reading."""
        ...


# ── Classroom Repository ──────────────────────────────────────────


class ClassroomRepositoryInterface(ABC):
    """Port for managing classroom entities."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> ClassroomEntity | None:
        """Retrieve a classroom by its unique id."""
        ...

    @abstractmethod
    async def update(self, classroom: ClassroomEntity) -> None:
        """Persist changes to an existing classroom."""
        ...


# ── Room Repository ────────────────────────────────────────────────


class RoomRepositoryInterface(ABC):
    """Port for managing rooms exposed to the mobile dashboard."""

    @abstractmethod
    async def get_all(self) -> List[RoomEntity]:
        """Return every room registered in the system."""
        ...

    @abstractmethod
    async def get_by_id(self, room_id: str) -> RoomEntity | None:
        """Look up a single room by its string id."""
        ...

    @abstractmethod
    async def update(self, room: RoomEntity) -> None:
        """Persist the updated state of a room."""
        ...


# ── External Sensors Repository ───────────────────────────────────


class ExternalSensorsRepositoryInterface(ABC):
    """Port for the campus weather / environmental station."""

    @abstractmethod
    async def get_latest(self) -> ExternalSensorsEntity:
        """Return the most recent external sensor snapshot."""
        ...


# ── Analytics Repository ──────────────────────────────────────────


class AnalyticsRepositoryInterface(ABC):
    """Port for analytics and prediction data access."""

    @abstractmethod
    async def get_analytics(self) -> AnalyticsDataEntity:
        """Return the current analytics and forecast payload."""
        ...


# ── User Repository ──────────────────────────────────────────────

class UserRepositoryInterface(ABC):
    """Port for managing user entities."""

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        """Retrieve a user by their email address."""
        ...

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Retrieve a user by their string ID."""
        ...

    @abstractmethod
    async def save(self, user: UserEntity) -> None:
        """Persist a new user."""
        ...
