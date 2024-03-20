import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.db.base import TimedBaseModel as Base
from src.db.db_helper import db_helper


# @pytest_asyncio.fixture(autouse=True)
# async def task_setup(event_loop):
#     assert settings.db.mode == "TEST"
#     engine = db_helper.engine
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def async_session() -> AsyncSession:
    session = sessionmaker(
        db_helper.engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db_helper.engine.dispose()
