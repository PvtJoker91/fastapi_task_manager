from dataclasses import dataclass

from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.services import BaseTaskService
from src.apps.users.services import BaseUserService


@dataclass
class CreateTaskUseCase:
    task_service: BaseTaskService
    user_service: BaseUserService

    def execute(self, task: TaskEntity):
        new_task = self.task_service.create_task(task)
