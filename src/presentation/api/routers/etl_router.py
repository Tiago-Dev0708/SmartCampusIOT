"""ETL router — trigger the monthly Data Lake export."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.use_cases.export_to_datalake import ExportToDataLakeUseCase
from src.infrastructure.hadoop.hdfs_client import HdfsClient
from src.presentation.api.dependencies import SensorRepoDep, CurrentUserDep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/etl", tags=["ETL / Big Data"])


# ── DI factory ─────────────────────────────────────────────────────

def get_export_use_case(sensor_repo: SensorRepoDep) -> ExportToDataLakeUseCase:
    """Build the ETL use case with the HDFS adapter."""
    hdfs = HdfsClient()
    return ExportToDataLakeUseCase(sensor_repo=sensor_repo, datalake_client=hdfs)


ExportUseCaseDep = Annotated[ExportToDataLakeUseCase, Depends(get_export_use_case)]


@router.post(
    "/trigger_monthly_export",
    summary="Trigger monthly ETL export",
    description=(
        "Extracts all sensor readings from PostgreSQL, transforms them "
        "into CSV format and uploads to the Hadoop HDFS Data Lake."
    ),
)
async def trigger_monthly_export(use_case: ExportUseCaseDep, user: CurrentUserDep) -> dict:
    """Run the ETL pipeline and return the export summary."""
    result = await use_case.execute()
    logger.info("ETL triggered — result: %s", result)
    return result
