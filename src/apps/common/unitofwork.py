from abc import ABC, abstractmethod
from typing import Type

from src.core.db import db_helper

from ..tasks.repositories import TaskRepository
from ..users.repositories import UserRepository



class IUnitOfWork(ABC):
    users: Type[UserRepository]
    tasks: Type[TaskRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = db_helper.session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.tasks = TaskRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
