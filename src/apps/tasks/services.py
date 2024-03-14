from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.models import Task as TaskModel


class BaseTaskService(ABC):
    @abstractmethod
    async def get_task_list(self, session: AsyncSession) -> Iterable[TaskEntity]:
        ...

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, task_id: int) -> TaskEntity:
        ...

    @abstractmethod
    async def create(self, session: AsyncSession, entity: TaskEntity) -> TaskEntity:
        ...


class ORMTaskService(BaseTaskService):

    async def get_task_list(self, session: AsyncSession) -> Iterable[TaskEntity]:
        stmt = select(TaskModel)
        tasks = await session.scalars(stmt)
        return [task.to_entity() for task in tasks]

    async def get_by_id(self, session: AsyncSession, task_id: int) -> TaskEntity | None:
        stmt = select(TaskModel).where(id=task_id)
        task: TaskModel | None = await session.scalar(stmt)
        if task:
            return task.to_entity()

    async def create(self, session: AsyncSession, task_in: TaskEntity) -> TaskEntity:
        task = task_in.to_dict()
        task_dto = TaskModel(**task)
        session.add(task_dto)
        await session.commit()
        return task_dto.to_entity()

