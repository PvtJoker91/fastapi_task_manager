from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from src.apps.tasks.entities import TaskEntity
from src.core.db import TimedBaseModel

if TYPE_CHECKING:
    from src.apps.users.models import User


class Task(TimedBaseModel):
    title: Mapped[str]
    description: Mapped[str | None]
    user: Mapped["User"] = relationship(back_populates="tasks")
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
