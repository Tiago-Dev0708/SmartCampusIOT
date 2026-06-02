"""Use Case: Toggle a classroom's light status."""

from uuid import UUID

from src.domain.entities.classroom import ClassroomEntity
from src.domain.exceptions import ClassroomNotFoundError
from src.domain.interfaces.repositories import ClassroomRepositoryInterface


class ToggleClassroomLightUseCase:
    """Toggle the light of a specific classroom on or off."""

    def __init__(self, classroom_repo: ClassroomRepositoryInterface) -> None:
        self._classroom_repo = classroom_repo

    async def execute(self, classroom_id: UUID, light_on: bool) -> ClassroomEntity:
        """Look up the classroom, flip the light, persist and return.

        Raises:
            ClassroomNotFoundError: If no classroom matches the given id.
        """
        classroom = await self._classroom_repo.get_by_id(classroom_id)
        if classroom is None:
            raise ClassroomNotFoundError(f"Classroom {classroom_id} not found")
        classroom.toggle_light(light_on)
        await self._classroom_repo.update(classroom)
        return classroom
