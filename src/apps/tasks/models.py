from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.core.db.base import TimedBaseModel
from src.apps.tasks.entities import TaskEntity

if TYPE_CHECKING:
    from src.apps.users.models import User


class Task(TimedBaseModel):
    title: Mapped[str]
    description: Mapped[str | None]
    is_visible: Mapped[bool]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="created_tasks", foreign_keys=[author_id])
    assignee: Mapped["User"] = relationship(back_populates="assigned_tasks", foreign_keys=[assignee_id])

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title!r})"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> TaskEntity:
        return TaskEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            author_id=self.author_id,
            assignee_id=self.assignee_id,
            is_visible=self.is_visible,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
