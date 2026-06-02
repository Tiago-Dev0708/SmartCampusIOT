"""SQLAlchemy ORM model for rooms exposed to the mobile dashboard."""

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RoomModel(Base):
    """Physical table ``rooms`` — controllable campus rooms.

    Maps to the React Native ``Room`` TypeScript interface.
    """

    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    block: Mapped[str] = mapped_column(String(16), nullable=False)
    floor: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="inactive")
    temperature: Mapped[float] = mapped_column(Float, nullable=False, default=25.5)
    energy_usage: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
