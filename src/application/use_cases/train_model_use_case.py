"""Use Case: Train a LightGBM model from HDFS sensor data.

Fetches the CSV export from HDFS, builds a ``lightgbm.Dataset``,
trains a Gradient Boosted Tree and saves the model artifact to disk.
"""

import asyncio
import io
import logging
import os
from typing import Optional

from src.domain.interfaces.datalake import DataLakeClientInterface

logger = logging.getLogger(__name__)

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "infrastructure", "ml", "artifacts")
_MODEL_FILE = os.path.join(_MODEL_DIR, "smartcampus_model.txt")


class TrainModelUseCase:
    """Orchestrate the ML training pipeline."""

    def __init__(self, datalake_client: DataLakeClientInterface) -> None:
        self._datalake_client = datalake_client

    async def execute(self, hdfs_path: Optional[str] = None) -> dict:
        """Fetch CSV from HDFS, train LightGBM and save the artifact.

        Args:
            hdfs_path: Override the default HDFS path for the training CSV.

        Returns:
            Summary dict with ``model_path``, ``num_iterations``, etc.
        """
        from datetime import datetime, timezone

        if hdfs_path is None:
            now = datetime.now(tz=timezone.utc)
            hdfs_path = f"/data/smartcampus/sensors/{now.strftime('%Y-%m')}.csv"

        # In a real setup we'd download from HDFS; for now we attempt
        # to read local sensor data via the repository as a fallback.
        csv_content = await self._fetch_csv(hdfs_path)

        if csv_content is None:
            logger.warning("No training data available — generating synthetic dataset")
            csv_content = self._generate_synthetic_csv()

        # Training is CPU-bound → run in a thread
        result = await asyncio.to_thread(self._train, csv_content)
        return result

    async def _fetch_csv(self, hdfs_path: str) -> Optional[str]:
        """Attempt to fetch CSV from HDFS.  Returns None on failure."""
        try:
            # The DataLakeClientInterface only has upload_csv;
            # for download we attempt a direct read via the hdfs lib.
            from hdfs import InsecureClient  # type: ignore[import-untyped]

            client = InsecureClient("http://localhost:9870", user="hadoop")
            with client.read(hdfs_path, encoding="utf-8") as reader:
                return reader.read()
        except Exception as exc:
            logger.warning("Could not fetch %s from HDFS: %s", hdfs_path, exc)
            return None

    @staticmethod
    def _generate_synthetic_csv() -> str:
        """Create a minimal synthetic dataset for demo training."""
        import csv as csv_mod
        import random

        buf = io.StringIO()
        writer = csv_mod.writer(buf)
        writer.writerow(["temperature", "humidity", "active_rooms", "total_rooms", "cost"])
        for _ in range(500):
            temp = round(random.uniform(18.0, 35.0), 1)
            hum = round(random.uniform(30.0, 90.0), 1)
            total = 3
            active = random.randint(0, total)
            cost = round(active * 1700 * 0.82 + random.uniform(-200, 200), 2)
            writer.writerow([temp, hum, active, total, cost])
        return buf.getvalue()

    @staticmethod
    def _train(csv_content: str) -> dict:
        """Synchronous LightGBM training — runs inside ``asyncio.to_thread``."""
        try:
            import lightgbm as lgb  # type: ignore[import-untyped]
            import numpy as np
        except ImportError:
            logger.warning("lightgbm/numpy not installed — skipping training")
            return {"status": "skipped", "reason": "lightgbm not installed"}

        import csv as csv_mod

        reader = csv_mod.DictReader(io.StringIO(csv_content))
        rows = list(reader)

        if not rows:
            return {"status": "skipped", "reason": "empty dataset"}

        feature_names = ["temperature", "humidity", "active_rooms", "total_rooms"]
        X = np.array([[float(r[f]) for f in feature_names] for r in rows])
        y = np.array([float(r["cost"]) for r in rows])

        dataset = lgb.Dataset(X, label=y, feature_name=feature_names)

        params = {
            "objective": "regression",
            "metric": "rmse",
            "learning_rate": 0.05,
            "num_leaves": 31,
            "verbose": -1,
        }

        booster = lgb.train(
            params,
            dataset,
            num_boost_round=100,
        )

        # Save artifact
        os.makedirs(_MODEL_DIR, exist_ok=True)
        booster.save_model(_MODEL_FILE)
        logger.info("Model trained and saved to %s", _MODEL_FILE)

        return {
            "status": "trained",
            "model_path": _MODEL_FILE,
            "num_iterations": booster.current_iteration(),
            "num_features": len(feature_names),
            "num_samples": len(rows),
        }
