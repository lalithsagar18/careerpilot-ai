import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.models.base import Base

logger = logging.getLogger("careerpilot.db")

# Setup Async Engine
db_url = settings.get_database_url()

def create_engine_for_url(url: str):
    if "sqlite" in url:
        return create_async_engine(
            url,
            echo=False,
            connect_args={"check_same_thread": False}
        )
    return create_async_engine(
        url,
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

engine = create_engine_for_url(db_url)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def init_db():
    """Initializes database schema, falling back to SQLite if PostgreSQL is unavailable."""
    global engine, AsyncSessionLocal
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"Database schema initialized successfully with {engine.url.drivername}.")
    except Exception as e:
        if "sqlite" not in str(engine.url):
            logger.warning(
                f"PostgreSQL connection failed ({e}). Falling back to local SQLite database (careerpilot.db)."
            )
            fallback_url = "sqlite+aiosqlite:///./careerpilot.db"
            engine = create_engine_for_url(fallback_url)
            AsyncSessionLocal = async_sessionmaker(
                bind=engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Local SQLite database initialized successfully.")
        else:
            raise e

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

