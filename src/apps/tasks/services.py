from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.filters import PaginationIn
from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.exceptions import TaskNotFound
from src.apps.tasks.models import Task as TaskModel


class BaseTaskService(ABC):
    @abstractmethod
    async def get_task_list(self, session: AsyncSession, pagination: PaginationIn) -> Iterable[TaskEntity]:
        ...

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, task_id: int) -> TaskEntity:
        ...

    @abstractmethod
    async def create(self, session: AsyncSession, entity: TaskEntity) -> TaskEntity:
        ...


class ORMTaskService(BaseTaskService):
    async def get_task_list(self, session: AsyncSession, pagination: PaginationIn) -> Iterable[TaskEntity]:
        stmt = select(TaskModel)
        tasks = await session.scalars(stmt)
        paginated_tasks = list(tasks)[
                          pagination.offset:pagination.offset + pagination.limit
                          ]
        return [task.to_entity() for task in paginated_tasks]

    async def get_by_id(self, session: AsyncSession, task_id: int) -> TaskEntity:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        task: TaskModel | None = await session.scalar(stmt)
        if task:
            return task.to_entity()
        raise TaskNotFound(task_id=task_id)

    async def create(self, session: AsyncSession, task_in: TaskEntity) -> TaskEntity:
        task = task_in.to_dict()
        task_dto = TaskModel(**task)
        session.add(task_dto)
        await session.commit()
        return task_dto.to_entity()
