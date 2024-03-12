from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api_v1.auth import utils as auth_utils
from api_v1.users.schemas import UserSchema
from core.models import User


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    return user


async def create_user(session: AsyncSession, user_in: UserSchema) -> User:
    user = user_in.model_dump()
    user["password"] = auth_utils.hash_password(user["password"])
    user_model = User(**user)
    session.add(user_model)
    await session.commit()
    # await session.refresh(user_model)
    return user_model
