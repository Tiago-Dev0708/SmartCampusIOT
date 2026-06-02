"""LightGBM model manager — Singleton loaded once at application startup.

If the trained model file is not found on disk the manager falls back to
a simple **linear contingency model** so that ``GET /api/analytics``
never breaks for the mobile app.

Skill 03 compliance:
- Model loaded ONCE via Singleton pattern (no per-request latency).
- Input validated via Pydantic schema before ``predict()``.
"""

import logging
import os
from typing import Dict, Optional

from src.domain.interfaces.prediction_service import PredictionServiceInterface

logger = logging.getLogger(__name__)

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
_MODEL_FILE = os.path.join(_MODEL_DIR, "smartcampus_model.txt")


class ModelManager(PredictionServiceInterface):
    """Singleton wrapper around LightGBM / contingency model.

    Call ``load_model()`` once during the FastAPI ``lifespan`` startup.
    After that, ``predict()`` is safe to call from any async route.
    """

    _instance: Optional["ModelManager"] = None

    def __new__(cls) -> "ModelManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None  # type: ignore[attr-defined]
            cls._instance._using_fallback = False  # type: ignore[attr-defined]
        return cls._instance

    # ── Lifecycle ──────────────────────────────────────────────────

    def load_model(self) -> None:
        """Load the LightGBM model from disk or activate the fallback."""
        try:
            import lightgbm as lgb  # type: ignore[import-untyped]

            if os.path.isfile(_MODEL_FILE):
                self._model = lgb.Booster(model_file=_MODEL_FILE)
                self._using_fallback = False
                logger.info("LightGBM model loaded from %s", _MODEL_FILE)
            else:
                logger.warning(
                    "Model file not found at %s — activating linear fallback",
                    _MODEL_FILE,
                )
                self._model = None
                self._using_fallback = True
        except ImportError:
            logger.warning("lightgbm not installed — activating linear fallback")
            self._model = None
            self._using_fallback = True

    # ── Interface ──────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return self._model is not None or self._using_fallback

    def predict(self, features: Dict[str, float]) -> Dict[str, float]:
        """Run inference or use the contingency linear model.

        Expected feature keys: ``temperature``, ``humidity``,
        ``active_rooms``, ``total_rooms``.
        """
        if self._model is not None:
            return self._predict_lgb(features)
        return self._predict_fallback(features)

    # ── Private helpers ────────────────────────────────────────────

    def _predict_lgb(self, features: Dict[str, float]) -> Dict[str, float]:
        """Inference via the trained LightGBM Booster."""
        import lightgbm as lgb  # type: ignore[import-untyped]
        import numpy as np

        feature_values = [
            features.get("temperature", 25.0),
            features.get("humidity", 60.0),
            features.get("active_rooms", 0.0),
            features.get("total_rooms", 3.0),
        ]
        prediction = self._model.predict([feature_values])[0]

        # The model predicts the projected monthly cost in BRL
        projected_cost = float(prediction) if not hasattr(prediction, "__len__") else float(prediction[0])
        baseline = features.get("total_rooms", 3) * 1700.0
        efficiency = max(0.0, round((1 - projected_cost / baseline) * 100, 1)) if baseline else 0.0

        return {
            "projected_cost": round(projected_cost, 2),
            "projected_cost_baseline": round(baseline, 2),
            "efficiency_percent": efficiency,
        }

    @staticmethod
    def _predict_fallback(features: Dict[str, float]) -> Dict[str, float]:
        """Simple linear contingency model — always available."""
        active = features.get("active_rooms", 0.0)
        total = features.get("total_rooms", 3.0)

        # Heuristic: each active room costs ~1700 BRL/month
        baseline = total * 1700.0
        projected_cost = active * 1700.0 * 0.82  # 18% savings from IoT
        efficiency = max(0.0, round((1 - projected_cost / baseline) * 100, 1)) if baseline else 0.0

        return {
            "projected_cost": round(projected_cost, 2),
            "projected_cost_baseline": round(baseline, 2),
            "efficiency_percent": efficiency,
        }


def get_model_manager() -> ModelManager:
    """Return the global Singleton instance."""
    return ModelManager()
