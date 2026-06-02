"""Use Case: Export sensor data from PostgreSQL to the HDFS Data Lake.

Extracts the previous month's sensor readings from the relational DB,
transforms them into a CSV payload (tabular format) and pushes the
result to the Hadoop HDFS cluster via the injected Data Lake client.
"""

import csv
import io
import logging
from datetime import datetime, timezone

from src.domain.interfaces.datalake import DataLakeClientInterface
from src.domain.interfaces.repositories import SensorRepositoryInterface

logger = logging.getLogger(__name__)


class ExportToDataLakeUseCase:
    """ETL pipeline: PostgreSQL → CSV → HDFS."""

    def __init__(
        self,
        sensor_repo: SensorRepositoryInterface,
        datalake_client: DataLakeClientInterface,
    ) -> None:
        self._sensor_repo = sensor_repo
        self._datalake_client = datalake_client

    async def execute(self) -> dict:
        """Run the full ETL cycle and return a summary.

        Returns:
            A dict with ``rows_exported``, ``hdfs_path`` and ``timestamp``.
        """
        # 1. EXTRACT — fetch all sensor readings
        readings = await self._sensor_repo.get_all()

        if not readings:
            logger.warning("No sensor readings to export — aborting ETL")
            return {"rows_exported": 0, "hdfs_path": None, "timestamp": None}

        # 2. TRANSFORM — build a CSV in-memory
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "device_id", "sensor_type", "value", "timestamp"])
        for r in readings:
            writer.writerow([
                str(r.id),
                r.device_id,
                r.sensor_type.value,
                r.value,
                r.timestamp.isoformat(),
            ])
        csv_content = buf.getvalue()

        # 3. LOAD — push to HDFS
        now = datetime.now(tz=timezone.utc)
        hdfs_path = f"/data/smartcampus/sensors/{now.strftime('%Y-%m')}.csv"

        await self._datalake_client.upload_csv(hdfs_path, csv_content)

        logger.info(
            "ETL complete: %d rows → %s",
            len(readings),
            hdfs_path,
        )

        return {
            "rows_exported": len(readings),
            "hdfs_path": hdfs_path,
            "timestamp": now.isoformat(),
        }
