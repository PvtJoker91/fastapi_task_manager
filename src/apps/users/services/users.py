from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.common.exceptions import ObjNotFoundException, ObjAlreadyExistsException
from src.apps.users import utils
from src.apps.users.entities.users import UserEntity
from src.apps.users.exceptions.users import UserAlreadyExists, UserNotFound
from src.apps.users.models import User as UserModel
from src.apps.users.repositories import UserRepository


class BaseUserService(ABC):

    @abstractmethod
    async def get_user_list(self, pagination, session: AsyncSession) -> Iterable[UserEntity]:
        ...

    @abstractmethod
    async def get_by_username(self, username: str, session: AsyncSession) -> UserEntity:
        ...

    @abstractmethod
    async def create_user(self, user_in: UserEntity, session: AsyncSession) -> UserEntity:
        ...

    @abstractmethod
    async def update_user(self, user_in: UserEntity, user_id: int, session: AsyncSession) -> UserEntity:
        ...

    @abstractmethod
    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        ...


@dataclass
class ORMUserService(BaseUserService):
    repository = UserRepository()

    async def create_user(self, user_in: UserEntity, session: AsyncSession) -> UserEntity:
        user_dict = user_in.to_dict()
        user_dict["password"] = utils.hash_password(user_dict["password"])
        try:
            user_dto = await self.repository.add_one(data=user_dict, session=session)
        except ObjAlreadyExistsException:
            raise UserAlreadyExists(username=user_in.username)
        return user_dto.to_entity()

    async def update_user(self, user_id: int, user_in: UserEntity, session: AsyncSession) -> UserEntity:
        user_dict = user_in.to_dict()
        try:
            user_dto = await self.repository.edit_one(obj_id=user_id, data=user_dict)
        except ObjNotFoundException:
            raise UserNotFound(user_id=user_id, session=session)
        return user_dto.to_entity()

    async def delete_user(self, user_id: int, session: AsyncSession):
        await self.repository.delete_one(obj_id=user_id, session=session)

    async def get_by_username(self, username: str, session: AsyncSession) -> UserEntity:
        try:
            user_dto: UserModel = await self.repository.find_one(username=username, session=session)
        except ObjNotFoundException:
            raise UserNotFound(username=username)
        return user_dto.to_entity()

    async def get_user_list(self, pagination, session: AsyncSession) -> Iterable[UserEntity]:
        users: Iterable[UserModel] = await self.repository.find_all(session=session)
        paginated_users = list(users)[
                          pagination.offset:pagination.offset + pagination.limit
                          ]
        return [user.to_entity() for user in paginated_users]
