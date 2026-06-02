"""Use Case: Toggle a room's active/inactive status for the mobile dashboard."""

from src.domain.entities.room import RoomEntity, RoomStatus
from src.domain.exceptions import RoomNotFoundError
from src.domain.interfaces.repositories import RoomRepositoryInterface


class ToggleRoomUseCase:
    """Switch a campus room between *active* and *inactive*."""

    def __init__(self, room_repo: RoomRepositoryInterface) -> None:
        self._room_repo = room_repo

    async def execute(self, room_id: str, new_status: RoomStatus) -> RoomEntity:
        """Toggle the room and recompute its temperature.

        When a room becomes **active**, its temperature converges to 21.0 °C
        (cooling system on).  When **inactive**, it rises to 25.5 °C.

        Raises:
            RoomNotFoundError: If the room does not exist.
        """
        room = await self._room_repo.get_by_id(room_id)
        if room is None:
            raise RoomNotFoundError(f"Room {room_id} not found")

        room.toggle(new_status)

        # Temperature convergence per simulation engine rules
        if room.is_active():
            room.temperature = 21.0
        else:
            room.temperature = 25.5
            room.energy_usage = 0.0

        await self._room_repo.update(room)
        return room
