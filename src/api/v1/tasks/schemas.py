from datetime import datetime

from pydantic import BaseModel

from src.apps.tasks.entities import TaskEntity


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None
    user_id: int

    def to_entity(self):
        return TaskEntity(
            title=self.title,
            description=self.description,
            user_id=self.user_id
        )


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str | None
    is_visible: bool = True
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: TaskEntity) -> 'TaskSchema':
        return TaskSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            is_visible=entity.is_visible,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
