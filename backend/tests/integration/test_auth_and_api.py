import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app as fastapi_app
from app.db.session import Base, get_db
import app.models

TEST_DB_FILE = "./test_careerpilot.db"
TEST_DB_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}"

test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

fastapi_app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    if os.path.exists(TEST_DB_FILE):
        try:
            os.remove(TEST_DB_FILE)
        except Exception:
            pass

@pytest.mark.asyncio
async def test_health_endpoints():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "CareerPilot AI"

@pytest.mark.asyncio
async def test_auth_registration_and_login_flow():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Register User A
        reg_payload = {
            "email": "user_a@example.com",
            "password": "Password123!",
            "full_name": "User Alpha"
        }
        reg_res = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert reg_res.status_code == 201
        token_data = reg_res.json()
        assert "access_token" in token_data
        token = token_data["access_token"]

        # 2. Get User A Profile with Bearer token
        headers = {"Authorization": f"Bearer {token}"}
        me_res = await ac.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == "user_a@example.com"

        # 3. Check Dashboard metrics
        dash_res = await ac.get("/api/v1/dashboard/metrics", headers=headers)
        assert dash_res.status_code == 200
        assert "career_score" in dash_res.json()

        # 4. Check MCP tool listing
        mcp_res = await ac.get("/api/v1/mcp/tools")
        assert mcp_res.status_code == 200
        tools = mcp_res.json()
        assert len(tools) >= 4
