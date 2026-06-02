"""ML router — training and prediction endpoints."""

import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from src.application.use_cases.predict_economy_use_case import PredictEconomyUseCase
from src.application.use_cases.train_model_use_case import TrainModelUseCase
from src.infrastructure.hadoop.hdfs_client import HdfsClient
from src.infrastructure.ml.lightgbm_service import ModelManager, get_model_manager
from src.presentation.api.dependencies import RoomRepoDep, SensorRepoDep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


# ── DI factories ───────────────────────────────────────────────────


def get_train_use_case(sensor_repo: SensorRepoDep) -> TrainModelUseCase:
    hdfs = HdfsClient()
    return TrainModelUseCase(datalake_client=hdfs)


def get_predict_use_case(room_repo: RoomRepoDep) -> PredictEconomyUseCase:
    mm = get_model_manager()
    return PredictEconomyUseCase(room_repo=room_repo, prediction_service=mm)


TrainUseCaseDep = Annotated[TrainModelUseCase, Depends(get_train_use_case)]
PredictUseCaseDep = Annotated[PredictEconomyUseCase, Depends(get_predict_use_case)]


# ── Endpoints ──────────────────────────────────────────────────────


@router.post(
    "/train",
    summary="Train the LightGBM model",
    description=(
        "Fetches sensor data from HDFS (or generates synthetic data), "
        "trains a LightGBM regression model and saves the artifact."
    ),
)
async def train_model(use_case: TrainUseCaseDep) -> dict:
    """Trigger a training run."""
    result = await use_case.execute()
    # Reload the Singleton so predictions use the new model
    mm = get_model_manager()
    mm.load_model()
    return result


@router.get(
    "/predict",
    summary="Predict economy metrics",
    description=(
        "Runs inference on the trained LightGBM model (or linear fallback) "
        "using current room states and optional sensor overrides."
    ),
)
async def predict_economy(
    use_case: PredictUseCaseDep,
    temperature: Optional[float] = Query(None, description="External temperature override (°C)"),
    humidity: Optional[float] = Query(None, description="Humidity override (%)"),
) -> dict:
    """Return economy projections."""
    return await use_case.execute(temperature=temperature, humidity=humidity)
