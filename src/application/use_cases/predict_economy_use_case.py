"""Use Case: Predict economy metrics via the LightGBM Singleton.

Takes the current room state and sensor features, runs inference
through the ``PredictionServiceInterface`` and returns projected
cost / efficiency data for the analytics screen.
"""

import logging

from src.domain.interfaces.prediction_service import PredictionServiceInterface
from src.domain.interfaces.repositories import RoomRepositoryInterface
from src.domain.entities.room import RoomStatus

logger = logging.getLogger(__name__)


class PredictEconomyUseCase:
    """Produce economy projections for the mobile Analytics view."""

    def __init__(
        self,
        room_repo: RoomRepositoryInterface,
        prediction_service: PredictionServiceInterface,
    ) -> None:
        self._room_repo = room_repo
        self._prediction_service = prediction_service

    async def execute(
        self,
        temperature: float | None = None,
        humidity: float | None = None,
    ) -> dict:
        """Run prediction based on current room state.

        Args:
            temperature: Optional override for external temperature.
            humidity: Optional override for humidity reading.

        Returns:
            Dict with ``projected_cost``, ``projected_cost_baseline``,
            ``efficiency_percent`` and input features.
        """
        rooms = await self._room_repo.get_all()
        active_rooms = sum(1 for r in rooms if r.status == RoomStatus.ACTIVE)
        total_rooms = len(rooms) or 1

        features = {
            "temperature": temperature if temperature is not None else 25.0,
            "humidity": humidity if humidity is not None else 60.0,
            "active_rooms": float(active_rooms),
            "total_rooms": float(total_rooms),
        }

        prediction = self._prediction_service.predict(features)

        logger.info(
            "Economy prediction — active=%d/%d → cost=R$%.2f",
            active_rooms,
            total_rooms,
            prediction.get("projected_cost", 0),
        )

        return {
            **prediction,
            "features": features,
        }
