from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings.settings import Settings

settings = Settings()

engine = create_async_engine(settings.DATABASE_URL, echo=True, connect_args={
        "command_timeout": 5,
        "timeout": 5,  # 5-second connection timeout instead of hanging
    },)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_= AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session