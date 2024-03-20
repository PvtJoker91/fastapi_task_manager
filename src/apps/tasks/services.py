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
from src.apps.tasks.repositories import TaskRepository



class BaseTaskService(ABC):

    @abstractmethod
    async def get_task_list(self, pagination: PaginationIn) -> Iterable[TaskEntity]:
        ...

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> TaskEntity:
        ...

    @abstractmethod
    async def create_task(self, task_in: TaskEntity) -> TaskEntity:
        ...

    @abstractmethod
    async def update_task(self, task_in: TaskEntity, task_id: int) -> TaskEntity:
        ...

    @abstractmethod
    async def delete_task(self, task_id: int) -> None:
        ...


class ORMTaskService(BaseTaskService):
    repository = TaskRepository()

    async def create_task(self, task_in: TaskEntity) -> TaskEntity:
        task = task_in.to_dict()
        task_dto = await self.repository.add_one(data=task)
        return task_dto.to_entity()

    async def update_task(self, task_id: int, task_in: TaskEntity) -> TaskEntity:
        task = task_in.to_dict()
        try:
            task_dto = await self.repository.edit_one(obj_id=task_id, data=task)
        except ObjNotFoundException:
            raise TaskNotFound(task_id=task_id)
        return task_dto.to_entity()


    async def delete_task(self, task_id: int):
        await self.repository.delete_one(obj_id=task_id)


    async def get_task_by_id(self, task_id: int) -> TaskEntity:
        try:
            task: TaskModel = await self.repository.find_one(id=task_id)
        except ObjNotFoundException:
            raise TaskNotFound(task_id=task_id)
        return task.to_entity()

    async def get_task_list(self, pagination: PaginationIn) -> Iterable[TaskEntity]:
        tasks: Iterable[TaskModel] = await self.repository.find_all()
        paginated_tasks = list(tasks)[
                          pagination.offset:pagination.offset + pagination.limit
                          ]
        return [task.to_entity() for task in paginated_tasks]
