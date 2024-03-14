from sqlalchemy.orm import Mapped, relationship

from src.apps.tasks.entities import TaskEntity
from src.apps.users.models import User
from src.core.db import TimedBaseModel


class Task(TimedBaseModel):
    title: Mapped[str]
    description: Mapped[str]
    user: Mapped[User] = relationship(back_populates="tasks")
    is_visible: Mapped[bool]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title!r})"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> TaskEntity:
        return TaskEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            user=User.to_entity(self.user),
            is_visible=self.is_visible,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
