"""Domain entity representing a campus room exposed to the mobile app.

This entity maps 1-to-1 to the React Native ``Room`` TypeScript interface.
"""

from dataclasses import dataclass
from enum import Enum


class RoomStatus(str, Enum):
    """Strict literal values accepted by the mobile front-end."""

    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class RoomEntity:
    """Pure domain entity for a controllable campus room.

    Attributes:
        id: Unique string identifier (UUID or hardware-generated incremental).
        name: Display name shown on the mobile card (e.g. "Sala de Aula 01").
        block: Building block identifier (e.g. "A", "B").
        floor: Floor label (e.g. "Piso 1", "Térreo").
        status: Current power state — ``'active'`` or ``'inactive'``.
        temperature: Current temperature reading in °C.
        energy_usage: Individual energy consumption in kWh.
    """

    id: str
    name: str
    block: str
    floor: str
    status: RoomStatus
    temperature: float
    energy_usage: float

    # ── Behaviour ──────────────────────────────────────────────────

    def toggle(self, new_status: RoomStatus) -> None:
        """Switch the room between *active* and *inactive*."""
        self.status = new_status

    def is_active(self) -> bool:
        """Return ``True`` when the room is powered on."""
        return self.status == RoomStatus.ACTIVE
