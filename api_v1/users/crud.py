import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth import utils
from api_v1.users.schemas import UserSchema
from core.models import User, db_helper


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_list(session: AsyncSession):
    stmt = select(User)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)


async def create_user(session: AsyncSession, user_in: UserSchema) -> User:
    user = user_in.model_dump()
    user["password"] = utils.hash_password(user["password"])
    user_model = User(**user)
    session.add(user_model)
    await session.commit()
    # await session.refresh(user_model)
    return user_model
