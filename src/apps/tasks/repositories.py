from sqlalchemy.orm import DeclarativeBase

from src.apps.common.repositories import SQLAlchemyRepository
from src.apps.tasks.models import Task


class TaskRepository(SQLAlchemyRepository):
    model: DeclarativeBase = Task
