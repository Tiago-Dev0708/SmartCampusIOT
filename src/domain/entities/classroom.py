"""Domain entity representing a classroom with IoT-controlled lighting and occupancy."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class ClassroomEntity:
    """Pure domain entity for a campus classroom.

    Attributes:
        id: Unique identifier.
        name: Human-readable room label (e.g. "Lab 101").
        is_occupied: Whether motion/presence sensors detect activity.
        light_status: Whether the lighting system is currently on.
        last_updated: Timestamp of the most recent state change.
    """

    name: str
    is_occupied: bool = False
    light_status: bool = False
    last_updated: datetime = field(default_factory=datetime.utcnow)
    id: UUID = field(default_factory=uuid4)

    # ── Behaviour methods ──────────────────────────────────────────

    def update_occupancy(self, status: bool) -> None:
        """Update the occupancy state and refresh the timestamp."""
        self.is_occupied = status
        self.last_updated = datetime.utcnow()

    def toggle_light(self, status: bool) -> None:
        """Turn the lighting system on or off."""
        self.light_status = status
        self.last_updated = datetime.utcnow()
