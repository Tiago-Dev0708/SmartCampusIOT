"""Asynchronous MQTT listener for ESP32-S3 sensor data ingestion.

This module is started as a background ``asyncio.Task`` by the FastAPI
``lifespan`` manager.  It subscribes to the campus IoT topics, validates
every incoming JSON payload via the ``SensorPayloadDTO`` schema and
delegates persistence to ``SaveSensorDataUseCase``.

**Resilience contract (Skill 05):**
- Invalid JSON payloads are logged and **discarded** — the listener
  never stops because of a single bad message.
- Network disconnections trigger automatic reconnection via the
  ``aiomqtt`` client's built-in retry loop.
"""

import json
import logging
from typing import Optional

import aiomqtt
from pydantic import ValidationError

from src.application.use_cases.save_sensor_data import SaveSensorDataUseCase
from src.infrastructure.database.config import get_session_factory
from src.infrastructure.repositories.sensor_repository import SensorRepositoryImpl
from src.presentation.api.schemas.mqtt_schemas import SensorPayloadDTO
from src.core.config.settings import settings

logger = logging.getLogger(__name__)

# ── Configuration constants ────────────────────────────────────────
_MQTT_QOS: int = 1  # At-least-once delivery


async def _handle_message(payload_bytes: bytes, use_case: SaveSensorDataUseCase) -> None:
    """Parse, validate and persist a single MQTT message.

    Any ``json.JSONDecodeError`` or Pydantic ``ValidationError`` is
    caught here so that the outer listener loop is never interrupted.
    """
    try:
        raw: dict = json.loads(payload_bytes)
        dto = SensorPayloadDTO(**raw)
        await use_case.execute(dto)
        logger.info("Sensor reading persisted: device=%s type=%s value=%s", dto.device_id, dto.sensor_type, dto.value)
    except json.JSONDecodeError as exc:
        logger.warning("MQTT payload is not valid JSON — discarded: %s", exc)
    except ValidationError as exc:
        logger.warning("MQTT payload failed schema validation — discarded: %s", exc)
    except Exception as exc:  # noqa: BLE001 — defensive catch-all
        logger.error("Unexpected error processing MQTT message: %s", exc, exc_info=True)


async def start_mqtt_listener() -> None:
    """Connect to the MQTT broker and consume messages indefinitely.

    This coroutine is designed to be wrapped in ``asyncio.create_task()``
    inside the FastAPI ``lifespan`` context manager.  It will keep
    retrying the connection on transient network failures.
    """
    session_factory = get_session_factory()

    while True:
        try:
            async with aiomqtt.Client(
                hostname=settings.MQTT_BROKER,
                port=settings.MQTT_PORT,
            ) as client:
                await client.subscribe(settings.MQTT_TOPIC, qos=_MQTT_QOS)
                logger.info(
                    "MQTT listener connected — broker=%s:%d topic=%s qos=%d",
                    settings.MQTT_BROKER,
                    settings.MQTT_PORT,
                    settings.MQTT_TOPIC,
                    _MQTT_QOS,
                )

                async for message in client.messages:
                    logger.info("Received MQTT message: topic=%s payload=%s", message.topic, message.payload)
                    # Each message gets its own short-lived DB session
                    async with session_factory() as session:
                        repo = SensorRepositoryImpl(session)
                        use_case = SaveSensorDataUseCase(sensor_repo=repo)
                        payload: bytes = (
                            message.payload
                            if isinstance(message.payload, bytes)
                            else message.payload.encode()
                        )
                        await _handle_message(payload, use_case)

        except aiomqtt.MqttError as exc:
            logger.warning("MQTT connection lost (%s) — reconnecting in 5 s …", exc)
            import asyncio
            await asyncio.sleep(5)
        except Exception as exc:  # noqa: BLE001
            logger.error("Fatal MQTT listener error: %s", exc, exc_info=True)
            import asyncio
            await asyncio.sleep(5)
