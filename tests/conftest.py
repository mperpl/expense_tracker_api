from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import StaticPool, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database import get_async_db
from main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
async_test_engine = create_async_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)
TestSessionLocal = async_sessionmaker(bind=async_test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_async_db():
    async with TestSessionLocal() as session:
        yield session
app.dependency_overrides[get_async_db] = override_get_async_db

@pytest.fixture(scope="session", autouse=True)
async def create_db():
    async with async_test_engine.begin() as con:
        from database import Base
        await con.run_sync(Base.metadata.create_all)
    yield
    await async_test_engine.dispose()

@pytest.fixture(autouse=True)
async def reset_db():
    async with async_test_engine.begin() as con:
        await con.execute(text("DELETE FROM expenses"))
    yield

@pytest.fixture
async def client():
    async with LifespanManager(app) as manager:
        async with AsyncClient(transport=ASGITransport(app=manager.app), base_url='http://test') as ac:
            yield ac