"""HDFS client adapter using the ``hdfs`` library (InsecureClient).

Because the ``hdfs`` library is **synchronous / blocking**, every I/O
call is wrapped in ``asyncio.to_thread`` so it never stalls the FastAPI
event loop.
"""

import asyncio
import io
import logging
from typing import Optional

from src.domain.interfaces.datalake import DataLakeClientInterface
from src.core.config.settings import settings

logger = logging.getLogger(__name__)

# Default Namenode WebHDFS URL (overridable via env in production)
_DEFAULT_NAMENODE_URL = "http://localhost:9870"
_DEFAULT_HDFS_USER = "hadoop"


class HdfsClient(DataLakeClientInterface):
    """Concrete adapter that pushes data to Apache Hadoop HDFS.

    The underlying ``hdfs.InsecureClient`` is lazily initialised the
    first time an upload is requested, so importing this module never
    triggers a network call.
    """

    def __init__(
        self,
        namenode_url: Optional[str] = None,
        hdfs_user: Optional[str] = None,
    ) -> None:
        self._namenode_url = namenode_url or settings.HDFS_URL
        self._hdfs_user = hdfs_user or settings.HDFS_USER
        self._client: Optional[object] = None

    def _get_client(self) -> object:
        """Lazily create the ``InsecureClient``."""
        if self._client is None:
            try:
                from hdfs import InsecureClient  # type: ignore[import-untyped]

                self._client = InsecureClient(
                    self._namenode_url,
                    user=self._hdfs_user,
                )
                logger.info(
                    "HDFS client initialised — namenode=%s user=%s",
                    self._namenode_url,
                    self._hdfs_user,
                )
            except ImportError:
                logger.warning(
                    "hdfs library not installed — uploads will be simulated (no-op)"
                )
                self._client = None
        return self._client  # type: ignore[return-value]

    # ── Blocking helpers (run in thread) ───────────────────────────

    def _sync_upload(self, hdfs_path: str, csv_content: str) -> None:
        """Synchronous upload — executed inside ``asyncio.to_thread``."""
        client = self._get_client()
        if client is None:
            logger.warning("HDFS upload skipped (no client): %s", hdfs_path)
            return

        buf = io.BytesIO(csv_content.encode("utf-8"))
        client.write(hdfs_path, buf, overwrite=True)  # type: ignore[union-attr]
        logger.info("HDFS upload complete: %s (%d bytes)", hdfs_path, len(csv_content))

    # ── Async interface implementation ─────────────────────────────

    async def upload_csv(self, hdfs_path: str, csv_content: str) -> None:
        """Upload CSV to HDFS without blocking the event loop."""
        await asyncio.to_thread(self._sync_upload, hdfs_path, csv_content)
