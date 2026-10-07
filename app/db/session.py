from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

async_db_url = settings.get_async_db_url()
sync_db_url = settings.get_sync_db_url()

engine_kwargs = {}
if "sqlite" in async_db_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

async_engine = create_async_engine(
    async_db_url,
    echo=False,
    future=True,
    **engine_kwargs
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync Engine (for Alembic migrations)
sync_engine_kwargs = {}
if "sqlite" in sync_db_url:
    sync_engine_kwargs["connect_args"] = {"check_same_thread": False}

sync_engine = create_engine(sync_db_url, echo=False, **sync_engine_kwargs)
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Dependency for providing DB session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
