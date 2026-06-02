"""Abstract interface for the Data Lake export adapter.

Defined in the domain layer so the application use-case never depends
directly on the HDFS implementation.
"""

from abc import ABC, abstractmethod


class DataLakeClientInterface(ABC):
    """Port for pushing processed data to an external Data Lake (e.g. HDFS)."""

    @abstractmethod
    async def upload_csv(self, hdfs_path: str, csv_content: str) -> None:
        """Upload a CSV string to the specified path in the Data Lake.

        Args:
            hdfs_path: Destination path inside HDFS (e.g. ``/data/sensors/2026-04.csv``).
            csv_content: The full CSV payload as a UTF-8 string.
        """
        ...
