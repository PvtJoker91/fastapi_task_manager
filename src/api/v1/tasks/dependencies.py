from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.services import ORMTaskService


def task_service_dependency():
    return ORMTaskService(TaskRepository)
