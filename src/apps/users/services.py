from abc import abstractmethod, ABC
from typing import Iterable

# from src.api.filters import PaginationIn
from src.api.v1.auth import utils
from src.apps.common.exceptions import ObjNotFoundException, ObjAlreadyExistsException
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions import UserAlreadyExists, UserNotFound
from src.apps.users.repositories import UserRepository
from src.apps.users.models import User as UserModel


class BaseUserService(ABC):

    @abstractmethod
    async def get_user_list(self, pagination) -> Iterable[UserEntity]:
        ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserEntity:
        ...

    @abstractmethod
    async def create_user(self, user_in: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    async def update_user(self, user_in: UserEntity, user_id: int) -> UserEntity:
        ...

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        ...


class ORMUserService(BaseUserService):
    def __init__(self, user_repository: type[UserRepository]):
        self.repository: UserRepository = user_repository()

    async def create_user(self, user_in: UserEntity) -> UserEntity:
        user_dict = user_in.to_dict()
        user_dict["password"] = utils.hash_password(user_dict["password"])
        try:
            user_dto = await self.repository.add_one(data=user_dict)
        except ObjAlreadyExistsException:
            raise UserAlreadyExists(username=user_in.username)
        return user_dto.to_entity()

    async def update_user(self, user_id: int, user_in: UserEntity) -> UserEntity:
        user_dict = user_in.to_dict()
        try:
            user_dto = await self.repository.edit_one(obj_id=user_id, data=user_dict)
        except ObjNotFoundException:
            raise UserNotFound(user_id=user_id)
        return user_dto.to_entity()

    async def delete_user(self, user_id: int):
        await self.repository.delete_one(obj_id=user_id)

    async def get_user_by_username(self, username: str) -> UserEntity:
        try:
            user_dto: UserModel = await self.repository.find_one(username=username)
        except ObjNotFoundException:
            raise UserNotFound(username=username)
        return user_dto.to_entity()

    async def get_user_list(self, pagination) -> Iterable[UserEntity]:
        users: Iterable[UserModel] = await self.repository.find_all()
        paginated_users = list(users)[
                          pagination.offset:pagination.offset + pagination.limit
                          ]
        return [user.to_entity() for user in paginated_users]
