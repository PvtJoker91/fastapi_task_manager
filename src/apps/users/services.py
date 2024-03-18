from abc import abstractmethod, ABC
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.filters import PaginationIn
from src.apps.auth import utils
from src.apps.common.exceptions import ObjNotFoundException, ObjAlreadyExistsException
from src.apps.common.unitofwork import IUnitOfWork
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions import UserAlreadyExists, UserNotFound
from src.core.db import User as UserModel


class BaseUserService(ABC):

    @abstractmethod
    async def get_user_list(self, uow: IUnitOfWork, pagination: PaginationIn) -> Iterable[UserEntity]:
        ...

    @abstractmethod
    async def get_user_by_username(self, uow: IUnitOfWork, username: str) -> UserEntity:
        ...

    @abstractmethod
    async def create_user(self, uow: IUnitOfWork, user_in: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    async def update_user(self, uow: IUnitOfWork, user_in: UserEntity, user_id: int) -> UserEntity:
        ...

    @abstractmethod
    async def delete_user(self, uow: IUnitOfWork, user_id: int) -> None:
        ...



class ORMUserService(BaseUserService):

    async def create_user(self, uow: IUnitOfWork, user_in: UserEntity) -> UserEntity:
        async with uow:
            user_dict = user_in.to_dict()
            user_dict["password"] = utils.hash_password(user_dict["password"])
            try:
                user_dto = await uow.users.add_one(data=user_dict)
            except ObjAlreadyExistsException:
                raise UserAlreadyExists(username=user_in.username)
            return user_dto.to_entity()


    async def update_user(self, uow: IUnitOfWork, user_id: int, user_in: UserEntity) -> UserEntity:
        async with uow:
            user_dict = user_in.to_dict()
            try:
                user_dto = await uow.users.edit_one(obj_id=user_in, data=user_dict)
            except ObjNotFoundException:
                raise UserNotFound(user_id=user_id)
            return user_dto.to_entity()


    async def delete_user(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            await uow.users.delete_one(obj_id=user_id)


    async def get_user_by_username(self, uow: IUnitOfWork, username: str) -> UserEntity:
        async with uow:
            try:
                user_dto: UserModel = await uow.users.find_one(username=username)
            except ObjNotFoundException:
                raise UserNotFound(username=username)
            return user_dto.to_entity()

    async def get_user_list(self, uow: IUnitOfWork, pagination: PaginationIn) -> Iterable[UserEntity]:
        async with uow:
            users: Iterable[UserModel] = await uow.users.find_all()
            paginated_users = list(users)[
                              pagination.offset:pagination.offset + pagination.limit
                              ]
            return [user.to_entity() for user in paginated_users]
