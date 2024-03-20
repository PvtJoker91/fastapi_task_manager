import pytest
import pytest_asyncio

from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.services import ORMTaskService
from src.apps.users.entities import UserEntity
from src.apps.users.services import ORMUserService


user_service = ORMUserService()
task_service = ORMTaskService()


@pytest_asyncio.fixture(autouse=True)
async def create_user():
    await user_service.create_user(UserEntity(username="test", password="test"))


@pytest.mark.asyncio
async def test_count():
    assert await task_service.count_tasks() == 0
    await task_service.create_task(TaskEntity(title="Task1", author_id=1, assignee_id=1))
    assert await task_service.count_tasks() == 1


@pytest.mark.asyncio
async def test_get():
    created_task = await task_service.create_task(TaskEntity(title="Task2", author_id=1, assignee_id=1))
    fetched_task = await task_service.get_task_by_id(created_task.id)
    assert created_task.title == fetched_task.title
