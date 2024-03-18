from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.filters import PaginationIn
from src.api.v1.tasks.filters import TaskFilter
from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.exceptions import TaskNotFound
from src.apps.common.exceptions import ObjNotFoundException
from src.apps.tasks.models import Task as TaskModel
from src.apps.common.unitofwork import IUnitOfWork



class BaseTaskService(ABC):

    @abstractmethod
    async def get_task_list(self, uow: IUnitOfWork, pagination: PaginationIn) -> Iterable[TaskEntity]:
        ...

    @abstractmethod
    async def get_task_by_id(self, uow: IUnitOfWork, task_id: int) -> TaskEntity:
        ...

    @abstractmethod
    async def create_task(self, uow: IUnitOfWork, task_in: TaskEntity) -> TaskEntity:
        ...

    @abstractmethod
    async def update_task(self, uow: IUnitOfWork, task_in: TaskEntity, task_id: int) -> TaskEntity:
        ...

    @abstractmethod
    async def delete_task(self, uow: IUnitOfWork, task_id: int) -> None:
        ...


class ORMTaskService(BaseTaskService):
    async def create_task(self, uow: IUnitOfWork, task_in: TaskEntity) -> TaskEntity:
        async with uow:
            task = task_in.to_dict()
            task_dto = await uow.tasks.add_one(data=task)
            return task_dto.to_entity()


    async def update_task(self, uow: IUnitOfWork, task_id: int, task_in: TaskEntity) -> TaskEntity:
        async with uow:
            task = task_in.to_dict()
            try:
                task_dto = await uow.tasks.edit_one(obj_id=task_id, data=task)
            except ObjNotFoundException:
                raise TaskNotFound(task_id=task_id)
            return task_dto.to_entity()


    async def delete_task(self, uow: IUnitOfWork, task_id: int):
        async with uow:
            await uow.tasks.delete_one(obj_id=task_id)


    async def get_task_by_id(self, uow: IUnitOfWork, task_id: int) -> TaskEntity:
        async with uow:
            try:
                task: TaskModel = await uow.tasks.find_one(id=task_id)
            except ObjNotFoundException:
                raise TaskNotFound(task_id=task_id)
            return task.to_entity()

    async def get_task_list(self, uow: IUnitOfWork, pagination: PaginationIn) -> Iterable[TaskEntity]:
        async with uow:
            tasks: Iterable[TaskModel] = await uow.tasks.find_all()
            paginated_tasks = list(tasks)[
                              pagination.offset:pagination.offset + pagination.limit
                              ]
            return [task.to_entity() for task in paginated_tasks]
