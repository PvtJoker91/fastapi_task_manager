from typing import Iterable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.users.schemas import UserCreateSchema
from src.apps.auth import utils
from src.apps.users.exceptions import UserAlreadyExists, UserNotFound
from src.core.db import User


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    if user:
        return user
    else:
        raise UserNotFound(username=username)


async def get_user_list(session: AsyncSession) -> Iterable[User]:
    stmt = select(User)
    users = await session.scalars(stmt)
    return users


async def create_user(session: AsyncSession, user_in: UserCreateSchema) -> User:
    user = user_in.model_dump()
    user["password"] = utils.hash_password(user["password"])
    user_model = User(**user)
    try:
        session.add(user_model)
        await session.commit()
    except IntegrityError:
        raise UserAlreadyExists(username=user_in.username)
    return user_model
