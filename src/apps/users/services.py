from abc import abstractmethod, ABC
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.filters import PaginationIn
from src.apps.auth import utils
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions import UserAlreadyExists, UserNotFound
from src.core.db import User


class BaseUserService(ABC):
    @abstractmethod
    async def get_user_list(self, session: AsyncSession, pagination: PaginationIn) -> Iterable[UserEntity]:
        ...

    @abstractmethod
    async def get_user_by_username(self, session: AsyncSession, username: str = None) -> UserEntity:
        ...

    @abstractmethod
    async def create(self, session: AsyncSession, entity: UserEntity) -> UserEntity:
        ...


class ORMUserService(BaseUserService):

    async def get_user_list(self, session: AsyncSession, pagination: PaginationIn) -> Iterable[UserEntity]:
        stmt = select(User)
        users = await session.scalars(stmt)
        paginated_users = list(users)[
                          pagination.offset:pagination.offset + pagination.limit
                          ]
        return [user.to_entity() for user in paginated_users]

    async def get_user_by_username(self, session: AsyncSession, username: str = None) -> UserEntity:
        stmt = select(User).where(User.username == username)
        user: User | None = await session.scalar(stmt)
        if user:
            return user.to_entity()
        raise UserNotFound(username=username)

    async def create(self, session: AsyncSession, user_in: UserEntity) -> UserEntity:
        user = user_in.to_dict()
        user["password"] = utils.hash_password(user["password"])
        user_dto = User(**user)
        try:
            session.add(user_dto)
            await session.commit()
        except IntegrityError:
            raise UserAlreadyExists(username=user_in.username)
        return user_dto.to_entity()
