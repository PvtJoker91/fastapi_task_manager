from datetime import datetime

from pydantic import BaseModel

from src.apps.tasks.entities import TaskEntity


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str | None
    is_visible: bool = True
    author_id: int
    assignee_id: int
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: TaskEntity) -> 'TaskSchema':
        return TaskSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            is_visible=entity.is_visible,
            author_id=entity.author_id,
            assignee_id=entity.assignee_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None
    # author_id: int
    assignee_id: int

    def to_entity(self):
        return TaskEntity(
            title=self.title,
            description=self.description,
            # author_id=self.author_id,
            assignee_id=self.assignee_id,
        )


class TaskUpdateSchema(BaseModel):
    assignee_id: int
    is_visible: bool

    def to_entity(self):
        return TaskEntity(
            assignee_id=self.assignee_id,
            is_visible=self.is_visible,
            updated_at=datetime.utcnow(),
        )
