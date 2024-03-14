from datetime import datetime

from pydantic import BaseModel

from src.api.v1.users.schemas import UserSchema
from src.apps.tasks.entities import TaskEntity


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str | None
    is_visible: bool = True
    # user: UserSchema
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: TaskEntity) -> 'TaskSchema':
        return TaskSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            is_visible=entity.is_visible,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )



