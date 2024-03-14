from typing import Iterable

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth import utils
from src.api.v1.users.schemas import UserCreateSchema
from src.core.db import User


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_list(session: AsyncSession) -> Iterable[User]:
    stmt = select(User)
    users = await session.scalars(stmt)
    return users


async def create_user(session: AsyncSession, user_in: UserCreateSchema) -> JSONResponse:
    user = user_in.model_dump()
    user["password"] = utils.hash_password(user["password"])
    user_model = User(**user)
    try:
        session.add(user_model)
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={"message": f"User with username {user_model.username} already exists!"})
    return JSONResponse(content={"message": f"User {user_model.username} created successfully!"},
                        status_code=status.HTTP_201_CREATED)
