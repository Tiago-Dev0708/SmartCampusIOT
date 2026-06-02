"""Abstract interface for ML prediction services.

Defined in the domain so use-cases never depend on LightGBM directly.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class PredictionServiceInterface(ABC):
    """Port for any ML model that produces economy/cost predictions."""

    @abstractmethod
    def predict(self, features: Dict[str, float]) -> Dict[str, float]:
        """Run inference on the provided feature dict.

        Args:
            features: Key-value pairs such as ``temperature``,
                      ``humidity``, ``active_rooms``, etc.

        Returns:
            A dict with prediction outputs (e.g. ``projected_cost``,
            ``efficiency_percent``).
        """
        ...

    @abstractmethod
    def is_loaded(self) -> bool:
        """Return ``True`` when a trained model is ready for inference."""
        ...
