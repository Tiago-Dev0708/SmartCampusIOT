"""Rooms router — mobile dashboard room management endpoints.

Handles ``GET /api/rooms``, ``POST /api/rooms/{id}/toggle``
and ``GET /api/rooms/sensors/external``.
"""

import random
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.domain.entities.room import RoomStatus
from src.domain.exceptions import RoomNotFoundError
from src.presentation.api.dependencies import RoomRepoDep, ToggleRoomUseCaseDep, CurrentUserDep, SensorRepoDep
from src.presentation.api.schemas.mobile_schemas import (
    ExternalSensorsResponse,
    RoomResponse,
    ToggleRoomRequest,
)

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get(
    "",
    response_model=List[RoomResponse],
    summary="List all campus rooms",
    description="Returns every room with dynamically computed temperatures.",
)
async def get_rooms(repo: RoomRepoDep, sensor_repo: SensorRepoDep) -> List[RoomResponse]:
    """Return all rooms with engine-computed values and real telemetry mapping."""
    rooms = await repo.get_all()
    
    # Map ESP32 sensor values to Room 1 (Sala de Aula 01)
    real_temp = await sensor_repo.get_latest_value("esp32_s3_campus_1", "temperature")
    
    response = []
    for r in rooms:
        temp = r.temperature
        if r.id == "1" and real_temp is not None:
            temp = real_temp
            
        response.append(
            RoomResponse(
                id=r.id,
                name=r.name,
                block=r.block,
                floor=r.floor,
                status=r.status.value,
                temperature=temp,
                energy_usage=r.energy_usage,
            )
        )
    return response


@router.post(
    "/{room_id}/toggle",
    response_model=RoomResponse,
    summary="Toggle room active/inactive",
    description=(
        "Switches a room between active and inactive.  "
        "The simulation engine immediately recomputes its temperature."
    ),
)
async def toggle_room(
    room_id: str,
    body: ToggleRoomRequest,
    use_case: ToggleRoomUseCaseDep,
    user: CurrentUserDep,
) -> RoomResponse:
    """Toggle and return the updated room."""
    try:
        room = await use_case.execute(room_id, RoomStatus(body.status))
    except RoomNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room {room_id} not found",
        )
    return RoomResponse(
        id=room.id,
        name=room.name,
        block=room.block,
        floor=room.floor,
        status=room.status.value,
        temperature=room.temperature,
        energy_usage=room.energy_usage,
    )


@router.get(
    "/sensors/external",
    response_model=ExternalSensorsResponse,
    summary="External weather station",
    description="Returns simulated meteorological data from the campus station.",
)
async def get_external_sensors(sensor_repo: SensorRepoDep) -> ExternalSensorsResponse:
    """Return weather station readings backed by real-time ESP32 sensors where available."""
    real_temp = await sensor_repo.get_latest_value("esp32_s3_campus_1", "temperature")
    real_humid = await sensor_repo.get_latest_value("esp32_s3_campus_1", "humidity")
    
    temperature = real_temp if real_temp is not None else round(random.uniform(22.0, 32.0), 1)
    humidity = real_humid if real_humid is not None else round(random.uniform(45.0, 85.0), 0)
    
    return ExternalSensorsResponse(
        temperature=temperature,
        humidity=humidity,
        co2=round(random.uniform(380.0, 450.0), 0),
        wind_speed=round(random.uniform(5.0, 25.0), 1),
        status="active",
    )
