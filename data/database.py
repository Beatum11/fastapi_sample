from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine('postgresql+asyncpg://postgres:root@localhost/Blog_Db')

async_local_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = async_local_session()
    try:
        yield db
    finally:
        await db.close()