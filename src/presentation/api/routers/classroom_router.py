"""Classroom router — IoT classroom management endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.domain.exceptions import ClassroomNotFoundError
from src.presentation.api.dependencies import ToggleClassroomUseCaseDep, CurrentUserDep

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


@router.get(
    "/{classroom_id}",
    summary="Get classroom status",
    description="Retrieve the current state of a specific classroom.",
)
async def get_classroom(classroom_id: UUID, use_case: ToggleClassroomUseCaseDep) -> dict:
    """Return the classroom entity or 404."""
    classroom = await use_case._classroom_repo.get_by_id(classroom_id)
    if classroom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")
    return {
        "id": str(classroom.id),
        "name": classroom.name,
        "is_occupied": classroom.is_occupied,
        "light_status": classroom.light_status,
        "last_updated": classroom.last_updated.isoformat(),
    }


@router.post(
    "/{classroom_id}/toggle_light",
    status_code=status.HTTP_200_OK,
    summary="Toggle classroom light",
    description="Turn the classroom lights on or off.",
)
async def toggle_light(
    classroom_id: UUID,
    light_on: bool,
    use_case: ToggleClassroomUseCaseDep,
    user: CurrentUserDep,
) -> dict:
    """Toggle the light and return the updated classroom."""
    try:
        classroom = await use_case.execute(classroom_id, light_on)
    except ClassroomNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")

    return {
        "id": str(classroom.id),
        "name": classroom.name,
        "is_occupied": classroom.is_occupied,
        "light_status": classroom.light_status,
        "last_updated": classroom.last_updated.isoformat(),
    }
