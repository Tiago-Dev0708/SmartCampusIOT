"""FastAPI application entry-point.

Bootstraps the application with:
- ``lifespan`` context manager (MQTT background task, DB init)
- All API routers mounted under the ``/api`` prefix
- CORS middleware
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import uuid

from src.infrastructure.database.config import get_engine
from src.infrastructure.database.models import Base
from src.infrastructure.mqtt.client import start_mqtt_listener
from src.presentation.api.routers.analytics_router import router as analytics_router
from src.presentation.api.routers.auth_router import router as auth_router
from src.presentation.api.routers.classroom_router import router as classroom_router
from src.presentation.api.routers.dashboard_router import router as dashboard_router
from src.presentation.api.routers.rooms_router import router as rooms_router
from src.presentation.api.routers.simulation_router import router as simulation_router
from src.presentation.api.routers.etl_router import router as etl_router
from src.presentation.api.routers.ml_router import router as ml_router
from src.presentation.api.middlewares.security_headers import SecurityHeadersMiddleware
from src.infrastructure.ml.lightgbm_service import get_model_manager
from src.presentation.api.dependencies import get_current_user

from src.core.config.logger import setup_logging, correlation_id
from src.core.config.cors import setup_cors
from src.core.config.settings import settings

setup_logging()
logger = logging.getLogger(__name__)


# ── Database seeding ───────────────────────────────────────────────

async def _seed_initial_data() -> None:
    """Insert default rooms and a demo user if the DB is empty."""
    from sqlalchemy import select, func
    from src.infrastructure.database.config import get_session_factory
    from src.infrastructure.database.models.room import RoomModel
    from src.infrastructure.database.models.user import UserModel

    factory = get_session_factory()
    async with factory() as session:
        # Seed rooms
        count = await session.scalar(select(func.count()).select_from(RoomModel))
        if count == 0:
            rooms = [
                RoomModel(id="1", name="Sala de Aula 01", block="A", floor="Piso 1", status="active", temperature=22.5, energy_usage=0.8),
                RoomModel(id="2", name="Laboratório", block="B", floor="Piso 2", status="inactive", temperature=25.0, energy_usage=0.0),
                RoomModel(id="3", name="Auditório", block="C", floor="Térreo", status="active", temperature=21.0, energy_usage=1.2),
            ]
            session.add_all(rooms)
            await session.commit()
            logger.info("Seeded %d default rooms", len(rooms))

        # Seed demo user
        user_count = await session.scalar(select(func.count()).select_from(UserModel))
        if user_count == 0:
            demo_user = UserModel(
                name="Prof. Mariano",
                email="usuario@estacio.br",
                password_hash="placeholder-hash",  # Will be bcrypt in Spec 009
                role="admin",
            )
            session.add(demo_user)
            await session.commit()
            logger.info("Seeded demo user: %s", demo_user.email)


# ── Lifespan ───────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifecycle — startup and shutdown hooks.

    **Startup:**
    1. Create database tables (dev convenience — use Alembic in prod).
    2. Seed initial data if tables are empty.
    3. Launch the MQTT listener as a background task.

    **Shutdown:**
    1. Cancel the MQTT task gracefully.
    2. Dispose the async engine connection pool.
    """
    try:
        logger.info("Starting Smart Campus IoT backend …")

        # 1. DB tables
        engine = get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables ensured")

        # 2. Seed
        await _seed_initial_data()

        # 3. Load LightGBM Singleton (or fallback)
        model_manager = get_model_manager()
        model_manager.load_model()
        logger.info("ML model loaded (fallback=%s)", model_manager._using_fallback)

        # 4. MQTT background task
        mqtt_task = asyncio.create_task(start_mqtt_listener())
        logger.info("MQTT listener task started")

        yield
    except Exception as exc:
        logger.critical("Application failed to start: %s", exc, exc_info=True)
        raise
    finally:
        # ── Shutdown ───────────────────────────────────────────────────
        logger.info("Shutting down application gracefully …")
        if 'mqtt_task' in locals():
            mqtt_task.cancel()
            try:
                await mqtt_task
            except asyncio.CancelledError:
                logger.info("MQTT listener task cancelled")

        if 'engine' in locals():
            await engine.dispose()
            logger.info("Database engine disposed — goodbye")


# ── App factory ────────────────────────────────────────────────────

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend REST API for the Smart Campus IoT mobile dashboard.",
    version=settings.VERSION,
    lifespan=lifespan,
)

setup_cors(app)
app.add_middleware(SecurityHeadersMiddleware)

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    correlation_id.set(corr_id)
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = corr_id
    return response

# Mount routers under /api prefix
app.include_router(auth_router, prefix="/api")
app.include_router(rooms_router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(dashboard_router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(analytics_router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(classroom_router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(simulation_router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(etl_router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(ml_router, prefix="/api", dependencies=[Depends(get_current_user)])


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Simple liveness probe."""
    return {"status": "ok", "service": "smart-campus-iot"}
