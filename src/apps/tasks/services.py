import asyncio
from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.filters import PaginationIn
from src.api.v1.tasks.filters import TaskFilter
from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.exceptions import TaskNotFound
from src.apps.tasks.models import Task as TaskModel
from src.apps.common.unitofwork import IUnitOfWork



class BaseTaskService(ABC):
    @abstractmethod
    async def get_tasks_count(self, session: AsyncSession, filters: TaskFilter) -> int:
        ...

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

    @staticmethod
    def _make_filters(filters: TaskFilter):
        model = TaskModel
        if filters.search:
            task_filter = and_(or_(model.title == filters.search,
                                   model.description.like(f"%{filters.search}%")),
                               model.is_visible == True)
        else:
            task_filter = (model.is_visible == True)
        return task_filter

    async def get_tasks_count(self, session: AsyncSession, filters: TaskFilter):
        # filter_condition = or_(TaskModel.title.like(f"%{filters.search}%"),
        #                        TaskModel.description == filters.search,)
        filter_condition = self._make_filters(filters=filters)
        query = select(TaskModel).filter(filter_condition)
        count = await session.scalars(query)

        return len(list(count))

    async def get_task_list(self, session: AsyncSession, pagination: PaginationIn) -> Iterable[TaskEntity]:
        query = select(TaskModel)
        tasks = await session.scalars(query)
        paginated_tasks = list(tasks)[
                          pagination.offset:pagination.offset + pagination.limit
                          ]
        return [task.to_entity() for task in paginated_tasks]

    async def get_by_id(self, session: AsyncSession, task_id: int) -> TaskEntity:
        query = select(TaskModel).where(TaskModel.id == task_id)
        task: TaskModel | None = await session.scalar(query)
        if task:
            return task.to_entity()
        raise TaskNotFound(task_id=task_id)

    async def create(self, session: AsyncSession, task_in: TaskEntity) -> TaskEntity:
        task = task_in.to_dict()
        task_dto = TaskModel(**task)
        session.add(task_dto)
        await session.commit()
        return task_dto.to_entity()



    async def get_tasks(self, uow: IUnitOfWork, pagination: PaginationIn) -> Iterable[TaskEntity]:
        async with uow:
            tasks = await uow.tasks.find_all()
            paginated_tasks = list(tasks)[
                              pagination.offset:pagination.offset + pagination.limit
                              ]
            return paginated_tasks
