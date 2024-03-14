from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.apps.tasks.entities import TaskEntity
from src.core.db import TimedBaseModel

if TYPE_CHECKING:
    from src.apps.users.models import User


class Task(TimedBaseModel):
    title: Mapped[str]
    description: Mapped[str | None]
    is_visible: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title!r})"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> TaskEntity:
        return TaskEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            user_id=self.user.id,
            is_visible=self.is_visible,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
