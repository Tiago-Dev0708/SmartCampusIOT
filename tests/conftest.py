import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.presentation.api.main import app
from src.infrastructure.database.models.base import Base

@pytest_asyncio.fixture
async def mock_db_session():
    """Provides an in-memory SQLite async database session for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    TestingSessionLocal = async_sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    
    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
def mock_mqtt_client(mocker):
    """Mocks the aiomqtt client to prevent real broker connections."""
    return mocker.patch("src.infrastructure.mqtt.client.aiomqtt.Client", autospec=True)

@pytest.fixture
def mock_hdfs_client(mocker):
    """Mocks the HDFS client to prevent real Hadoop connections."""
    return mocker.patch("src.infrastructure.hadoop.hdfs_client.HdfsClient", autospec=True)

@pytest_asyncio.fixture
async def client():
    """Provides an httpx AsyncClient mounted on the FastAPI application."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
