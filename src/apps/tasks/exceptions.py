from dataclasses import dataclass

from src.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class TaskNotFound(ServiceException):
    task_id: int

    @property
    def message(self):
        return f"Task with id '{self.task_id}' not found"

