"""Simulation router — bulk ingest simulated sensor data."""

from typing import List

from fastapi import APIRouter, status

from src.presentation.api.dependencies import SaveSensorUseCaseDep
from src.presentation.api.schemas.mqtt_schemas import SensorPayloadDTO

router = APIRouter(prefix="/simulate", tags=["Simulation"])


@router.post(
    "/month",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Simulate one month of sensor data",
    description=(
        "Accepts a list of ``SensorPayloadDTO`` objects representing "
        "one month of IoT readings and persists them in batch."
    ),
)
async def simulate_month(
    payloads: List[SensorPayloadDTO],
    use_case: SaveSensorUseCaseDep,
) -> dict:
    """Process a batch of sensor readings."""
    for dto in payloads:
        await use_case.execute(dto)
    return {"processed": len(payloads)}
