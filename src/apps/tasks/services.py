from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.common.exceptions import ObjNotFoundException
from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.exceptions import TaskNotFound
from src.apps.tasks.models import Task as TaskModel
from src.apps.tasks.repositories import TaskRepository


class BaseTaskService(ABC):

    @abstractmethod
    async def get_task_list(self, pagination, session: AsyncSession) -> Iterable[TaskEntity]:
        ...

    @abstractmethod
    async def get_task_by_id(self, task_id: int, session: AsyncSession) -> TaskEntity:
        ...

    @abstractmethod
    async def create_task(self, task_in: TaskEntity, session: AsyncSession) -> TaskEntity:
        ...

    @abstractmethod
    async def update_task(self, task_in: TaskEntity, task_id: int, session: AsyncSession) -> TaskEntity:
        ...

    @abstractmethod
    async def delete_task(self, task_id: int, session: AsyncSession) -> None:
        ...

    @abstractmethod
    async def count_tasks(self, session: AsyncSession) -> int:
        ...


class ORMTaskService(BaseTaskService):
    repository = TaskRepository()

    async def create_task(self, task_in: TaskEntity, session: AsyncSession) -> TaskEntity:
        task = task_in.to_dict()
        task_dto = await self.repository.add_one(data=task, session=session)
        return task_dto.to_entity()

    async def update_task(self, task_id: int, task_in: TaskEntity, session: AsyncSession) -> TaskEntity:
        task = task_in.to_dict()
        try:
            task_dto = await self.repository.edit_one(obj_id=task_id, data=task, session=session)
        except ObjNotFoundException:
            raise TaskNotFound(task_id=task_id)
        return task_dto.to_entity()

    async def delete_task(self, task_id: int, session: AsyncSession):
        await self.repository.delete_one(obj_id=task_id, session=session)

    async def get_task_by_id(self, task_id: int, session: AsyncSession) -> TaskEntity:
        try:
            task: TaskModel = await self.repository.find_one(id=task_id, session=session)
        except ObjNotFoundException:
            raise TaskNotFound(task_id=task_id)
        return task.to_entity()

    async def get_task_list(self, pagination, session: AsyncSession) -> Iterable[TaskEntity]:
        tasks: Iterable[TaskModel] = await self.repository.find_all(session=session)
        paginated_tasks = list(tasks)[
                          pagination.offset:pagination.offset + pagination.limit
                          ]
        return [task.to_entity() for task in paginated_tasks]

    async def count_tasks(self, session: AsyncSession) -> int:
        return await self.repository.count(session=session)
